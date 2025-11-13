"""Asynchronous mesh discovery + sync prototype with security (ECDH + HMAC).

Integrated with mesh.discovery: on peer discovery initiate key exchange and hello to sync.
"""

import asyncio
import json
import base64
import time
import uuid
from typing import Dict, Tuple

from .crypto import generate_keypair, derive_keys, b64, ub64, encrypt_and_mac, verify_and_decrypt
from .discovery import DiscoveryService

CHUNK_SIZE = 1024


def now_ts():
    return int(time.time())


class SyncNodeProtocol(asyncio.DatagramProtocol):
    def __init__(self, node):
        self.node = node

    def connection_made(self, transport):
        self.transport = transport
        self.node._set_transport(transport)

    def datagram_received(self, data, addr):
        try:
            msg = json.loads(data.decode('utf-8'))
        except Exception as e:
            print(f"{self.node.node_id}: invalid message from {addr}: {e}")
            return
        asyncio.create_task(self.node.handle_message(msg, addr))


class SyncNode:
    def __init__(self, host: str, port: int, node_id: str = None):
        self.host = host
        self.port = port
        self.node_id = node_id or str(uuid.uuid4())
        # storage: object_id -> (bytes, version)
        self.storage: Dict[str, Tuple[bytes, int]] = {}
        self.transport = None
        self._endpoint = None
        self.peers = {}  # addr -> peer state: {id, session, sent_pub}
        self.pending = {}  # object_id -> bytearray for incoming
        # generate keypair
        self.pub, self.priv = generate_keypair()
        self.discovery = None

    async def start(self):
        loop = asyncio.get_running_loop()
        transport, protocol = await loop.create_datagram_endpoint(lambda: SyncNodeProtocol(self), local_addr=(self.host, self.port))
        self._endpoint = (transport, protocol)
        # transport will also be set via protocol.connection_made
        print(f"{self.node_id}: listening on {self.host}:{self.port}")

    def stop(self):
        try:
            if self._endpoint:
                transport, _ = self._endpoint
                transport.close()
                self._endpoint = None
        except Exception:
            pass
        try:
            if self.discovery:
                self.discovery.stop()
        except Exception:
            pass

    def start_with_discovery(self, metadata: dict = None):
        """Start discovery service and bind to discovery updates."""
        if self.discovery:
            return
        self.discovery = DiscoveryService(node_id=self.node_id, metadata=metadata or {'name': 'sync-node', 'sync_port': self.port}, on_update=self._on_discovered)
        self.discovery.start()

    def _on_discovered(self, msg, addr):
        # discovery provides (msg, (ip, port)); assume peer listens on same port if provided in meta
        peer_meta = msg.get('meta', {})
        peer_addr = addr[0]
        peer_port = peer_meta.get('sync_port') or self.port  # fallback to same port
        peer = (peer_addr, int(peer_port))
        print(f"{self.node_id}: discovered peer {msg.get('node_id')} at {peer}")
        # auto start key exchange and hello
        try:
            loop = asyncio.get_event_loop()
            loop.call_soon_threadsafe(self.send_key_exchange, peer)
            loop.call_later(0.2, lambda: loop.call_soon_threadsafe(self.send_hello, peer))
        except Exception as e:
            print('Error scheduling key exchange/hello:', e)

    def _set_transport(self, transport):
        self.transport = transport

    def add_object(self, object_id: str, data: bytes, version: int = 1):
        self.storage[object_id] = (data, version)

    def _send(self, msg: dict, addr):
        if not self.transport:
            raise RuntimeError('transport not ready')
        payload = json.dumps(msg).encode('utf-8')
        self.transport.sendto(payload, addr)

    async def handle_message(self, msg: dict, addr):
        mtype = msg.get('type')
        sender = msg.get('from')
        if sender:
            # initialize peer state if needed
            st = self.peers.get(addr, {'id': sender, 'session': None, 'sent_pub': False})
            st['id'] = sender
            self.peers[addr] = st
        # Dispatch
        if mtype == 'KEY_EXCHANGE':
            await self._on_key_exchange(msg, addr)
        elif mtype == 'HELLO' or mtype == 'ENCRYPTED':
            # ENCRYPTED envelope handled in lower-level handlers
            await self._on_hello(msg, addr)
        elif mtype == 'DIGESTS':
            await self._on_digests(msg, addr)
        elif mtype == 'REQUEST':
            await self._on_request(msg, addr)
        elif mtype == 'CHUNK':
            await self._on_chunk(msg, addr)
        elif mtype == 'ACK':
            await self._on_ack(msg, addr)
        else:
            print(f"{self.node_id}: unknown message type {mtype} from {addr}")

    async def _on_key_exchange(self, msg, addr):
        their_pub_b64 = msg.get('pub')
        if not their_pub_b64:
            return
        their_pub = ub64(their_pub_b64)
        enc_key, mac_key = derive_keys(self.priv, their_pub)
        st = self.peers.get(addr, {'id': msg.get('from'), 'session': None, 'sent_pub': False})
        st['session'] = {'enc': enc_key, 'mac': mac_key}
        self.peers[addr] = st
        # respond with our public key only if we haven't already sent ours
        if not st.get('sent_pub'):
            resp = {'type': 'KEY_EXCHANGE', 'from': self.node_id, 'pub': b64(self.pub)}
            st['sent_pub'] = True
            self.peers[addr] = st
            self._send(resp, addr)
        print(f"{self.node_id}: key exchange completed with {addr}")

    async def _on_hello(self, msg, addr):
        # handle encrypted envelope first
        if msg.get('type') == 'ENCRYPTED':
            session = self.peers.get(addr, {}).get('session')
            if session:
                enc = msg.get('enc', {})
                try:
                    n = ub64(enc.get('n'))
                    ct = ub64(enc.get('ct'))
                    mac = ub64(enc.get('mac'))
                    pt = verify_and_decrypt(n, ct, mac, session['enc'], session['mac'])
                    inner = json.loads(pt.decode('utf-8'))
                    # dispatch inner
                    await self.handle_message(inner, addr)
                    return
                except Exception as e:
                    print(f"{self.node_id}: failed to decrypt ENCRYPTED message from {addr}: {e}")
        # respond with DIGESTS (encrypted if session exists)
        digests = [{'id': oid, 'version': ver} for oid, (_, ver) in self.storage.items()]
        payload = {'type': 'DIGESTS', 'from': self.node_id, 'digests': digests}
        session = self.peers.get(addr, {}).get('session')
        if session:
            n, ct, mac = encrypt_and_mac(json.dumps(payload).encode('utf-8'), session['enc'], session['mac'])
            env = {'type': 'ENCRYPTED', 'from': self.node_id, 'enc': {'n': b64(n), 'ct': b64(ct), 'mac': b64(mac)}}
            self._send(env, addr)
            print(f"{self.node_id}: HELLO from {msg.get('from')} -> sent ENCRYPTED DIGESTS to {addr}")
        else:
            self._send(payload, addr)
            print(f"{self.node_id}: HELLO from {msg.get('from')} -> sent DIGESTS ({len(digests)}) to {addr}")

    async def _on_digests(self, msg, addr):
        # handle possibly encrypted message
        if msg.get('type') == 'ENCRYPTED':
            session = self.peers.get(addr, {}).get('session')
            if not session:
                print(f"{self.node_id}: received ENCRYPTED but no session with {addr}")
                return
            enc = msg.get('enc', {})
            n = ub64(enc.get('n'))
            ct = ub64(enc.get('ct'))
            mac = ub64(enc.get('mac'))
            try:
                pt = verify_and_decrypt(n, ct, mac, session['enc'], session['mac'])
                inner = json.loads(pt.decode('utf-8'))
                msg = inner
            except Exception as e:
                print(f"{self.node_id}: decryption failed from {addr}: {e}")
                return
        # now plain digests
        digests = msg.get('digests', [])
        for entry in digests:
            oid = entry.get('id')
            ver = entry.get('version', 0)
            local = self.storage.get(oid)
            if not local or local[1] < ver:
                req = {'type': 'REQUEST', 'from': self.node_id, 'id': oid, 'chunk': 0}
                session = self.peers.get(addr, {}).get('session')
                if session:
                    n, ct, mac = encrypt_and_mac(json.dumps(req).encode('utf-8'), session['enc'], session['mac'])
                    env = {'type': 'ENCRYPTED', 'from': self.node_id, 'enc': {'n': b64(n), 'ct': b64(ct), 'mac': b64(mac)}}
                    self._send(env, addr)
                else:
                    self._send(req, addr)
                print(f"{self.node_id}: requesting {oid} from {addr}")

    async def _on_request(self, msg, addr):
        # handle possibly encrypted
        if msg.get('type') == 'ENCRYPTED':
            session = self.peers.get(addr, {}).get('session')
            if not session:
                print(f"{self.node_id}: received ENCRYPTED request but no session with {addr}")
                return
            enc = msg.get('enc', {})
            n = ub64(enc.get('n'))
            ct = ub64(enc.get('ct'))
            mac = ub64(enc.get('mac'))
            try:
                pt = verify_and_decrypt(n, ct, mac, session['enc'], session['mac'])
                inner = json.loads(pt.decode('utf-8'))
                msg = inner
            except Exception as e:
                print(f"{self.node_id}: decryption failed from {addr}: {e}")
                return
        oid = msg.get('id')
        chunk_idx = int(msg.get('chunk', 0))
        entry = self.storage.get(oid)
        if not entry:
            print(f"{self.node_id}: received request for unknown object {oid}")
            return
        data, ver = entry
        start = chunk_idx * CHUNK_SIZE
        chunk = data[start:start + CHUNK_SIZE]
        b64data = base64.b64encode(chunk).decode('ascii')
        more = 1 if (start + CHUNK_SIZE) < len(data) else 0
        msg_out = {
            'type': 'CHUNK',
            'from': self.node_id,
            'id': oid,
            'chunk': chunk_idx,
            'data': b64data,
            'more': more,
            'version': ver,
        }
        session = self.peers.get(addr, {}).get('session')
        if session:
            n, ct, mac = encrypt_and_mac(json.dumps(msg_out).encode('utf-8'), session['enc'], session['mac'])
            env = {'type': 'ENCRYPTED', 'from': self.node_id, 'enc': {'n': b64(n), 'ct': b64(ct), 'mac': b64(mac)}}
            self._send(env, addr)
        else:
            self._send(msg_out, addr)
        print(f"{self.node_id}: sent CHUNK {chunk_idx} (more={more}) for {oid} to {addr}")

    async def _on_chunk(self, msg, addr):
        # handle encrypted
        if msg.get('type') == 'ENCRYPTED':
            session = self.peers.get(addr, {}).get('session')
            if not session:
                print(f"{self.node_id}: received ENCRYPTED chunk but no session with {addr}")
                return
            enc = msg.get('enc', {})
            n = ub64(enc.get('n'))
            ct = ub64(enc.get('ct'))
            mac = ub64(enc.get('mac'))
            try:
                pt = verify_and_decrypt(n, ct, mac, session['enc'], session['mac'])
                inner = json.loads(pt.decode('utf-8'))
                msg = inner
            except Exception as e:
                print(f"{self.node_id}: decryption failed from {addr}: {e}")
                return
        oid = msg.get('id')
        chunk_idx = int(msg.get('chunk', 0))
        b64data = msg.get('data', '')
        more = int(msg.get('more', 0))
        ver = int(msg.get('version', 0))
        chunk = base64.b64decode(b64data.encode('ascii'))
        buf = self.pending.setdefault(oid, bytearray())
        buf.extend(chunk)
        print(f"{self.node_id}: received CHUNK {chunk_idx} for {oid} (more={more}) from {addr}")
        if not more:
            self.storage[oid] = (bytes(buf), ver)
            self.pending.pop(oid, None)
            ack = {'type': 'ACK', 'from': self.node_id, 'id': oid, 'version': ver}
            session = self.peers.get(addr, {}).get('session')
            if session:
                n, ct, mac = encrypt_and_mac(json.dumps(ack).encode('utf-8'), session['enc'], session['mac'])
                env = {'type': 'ENCRYPTED', 'from': self.node_id, 'enc': {'n': b64(n), 'ct': b64(ct), 'mac': b64(mac)}}
                self._send(env, addr)
            else:
                self._send(ack, addr)
            print(f"{self.node_id}: assembled object {oid} (len={len(self.storage[oid][0])}), sent ACK to {addr}")

    async def _on_ack(self, msg, addr):
        # handle encrypted ack
        if msg.get('type') == 'ENCRYPTED':
            session = self.peers.get(addr, {}).get('session')
            if not session:
                print(f"{self.node_id}: received ENCRYPTED ack but no session with {addr}")
                return
            enc = msg.get('enc', {})
            n = ub64(enc.get('n'))
            ct = ub64(enc.get('ct'))
            mac = ub64(enc.get('mac'))
            try:
                pt = verify_and_decrypt(n, ct, mac, session['enc'], session['mac'])
                inner = json.loads(pt.decode('utf-8'))
                msg = inner
            except Exception as e:
                print(f"{self.node_id}: decryption failed from {addr}: {e}")
                return
        print(f"{self.node_id}: received ACK for {msg.get('id')} from {msg.get('from')} version={msg.get('version')}" )

    # Active operations
    def send_key_exchange(self, peer_addr):
        st = self.peers.get(peer_addr, {'id': None, 'session': None, 'sent_pub': False})
        st['sent_pub'] = True
        self.peers[peer_addr] = st
        msg = {'type': 'KEY_EXCHANGE', 'from': self.node_id, 'pub': b64(self.pub)}
        self._send(msg, peer_addr)
        print(f"{self.node_id}: sent KEY_EXCHANGE to {peer_addr}")

    def send_hello(self, peer_addr):
        msg = {'type': 'HELLO', 'from': self.node_id, 'ts': now_ts()}
        self._send(msg, peer_addr)
        print(f"{self.node_id}: sent HELLO to {peer_addr}")


async def demo_two_nodes():
    node_a = SyncNode('127.0.0.1', 10001, node_id='nodeA')
    node_b = SyncNode('127.0.0.1', 10002, node_id='nodeB')

    # node A has an object
    data = b'This is a sample payload that will be chunked and transferred between nodes.' * 20
    node_a.add_object('object1', data, version=1)

    await node_a.start()
    await node_b.start()

    # Perform key exchange first
    await asyncio.sleep(0.1)
    node_b.send_key_exchange(('127.0.0.1', 10001))

    # Wait a bit then say HELLO to initiate sync
    await asyncio.sleep(0.2)
    node_b.send_hello(('127.0.0.1', 10001))

    # wait for transfer to complete
    await asyncio.sleep(2)

    # Verify
    if 'object1' in node_b.storage:
        print('Secure sync successful: nodeB has object1, len=', len(node_b.storage['object1'][0]))
    else:
        print('Secure sync failed: nodeB missing object1')

    # Close transports
    await asyncio.sleep(0.1)


if __name__ == '__main__':
    asyncio.run(demo_two_nodes())
