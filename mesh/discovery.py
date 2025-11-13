"""UDP multicast discovery service for local mesh node discovery.

Usage:
  - Run `python -m mesh.discovery` to start announcer+listener.
  - Uses UDP multicast address 224.0.0.251:9999 (local scope) by default.

Notes:
  - Designed to work offline on local networks and Wi-Fi Direct groups that support multicast.
  - Announcements are JSON payloads containing node id, timestamp, and optional metadata.
"""

import socket
import struct
import threading
import time
import json
import uuid
from typing import Callable

MCAST_GRP = '224.0.0.251'
MCAST_PORT = 9999
ANNOUNCE_INTERVAL = 5.0
BUFFER_SIZE = 4096


class DiscoveryService:
    def __init__(self, node_id: str = None, metadata: dict = None, on_update: Callable = None):
        self.node_id = node_id or str(uuid.uuid4())
        self.metadata = metadata or {}
        self.on_update = on_update
        self.running = False
        self._sock = None

    def _build_packet(self):
        packet = {
            'node_id': self.node_id,
            'ts': time.time(),
            'meta': self.metadata,
        }
        return json.dumps(packet).encode('utf-8')

    def _create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(('', MCAST_PORT))
        except OSError:
            # try bind to loopback if port already in use on other interface
            sock.bind(('0.0.0.0', MCAST_PORT))
        mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        return sock

    def _listen_loop(self):
        sock = self._sock
        while self.running:
            try:
                data, addr = sock.recvfrom(BUFFER_SIZE)
                try:
                    msg = json.loads(data.decode('utf-8'))
                except Exception:
                    continue
                # ignore our own announcements
                if msg.get('node_id') == self.node_id:
                    continue
                if self.on_update:
                    self.on_update(msg, addr)
            except Exception:
                time.sleep(0.1)

    def _announce_loop(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        ttl = struct.pack('b', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        packet = self._build_packet()
        while self.running:
            try:
                sock.sendto(packet, (MCAST_GRP, MCAST_PORT))
            except Exception:
                pass
            time.sleep(ANNOUNCE_INTERVAL)

    def start(self):
        if self.running:
            return
        self.running = True
        self._sock = self._create_socket()
        self._listener = threading.Thread(target=self._listen_loop, daemon=True)
        self._announcer = threading.Thread(target=self._announce_loop, daemon=True)
        self._listener.start()
        self._announcer.start()

    def stop(self):
        self.running = False
        try:
            if self._sock:
                self._sock.close()
        except Exception:
            pass


if __name__ == '__main__':
    import sys

    nodes = {}

    def on_update(msg, addr):
        node_id = msg.get('node_id')
        nodes[node_id] = {'addr': addr, 'meta': msg.get('meta'), 'ts': msg.get('ts')}
        print(f"Discovered {node_id} at {addr} meta={msg.get('meta')}")

    svc = DiscoveryService(metadata={'name': 'node-local'}, on_update=on_update)
    svc.start()
    print('Discovery service started. Press Ctrl+C to stop.')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        svc.stop()
        print('Stopped')
