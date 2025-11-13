"""Simple Bluetooth LE advertising relay using bleak for cross-platform BLE advertising.

This is a conceptual implementation: real-world advertising and scanning require platform-specific
APIs and appropriate permissions. This module demonstrates payload encryption (AES-GCM) and
packing for small advertisement payloads.

Note: bleak currently supports scanning/connecting; advertising support is limited and platform-specific.
"""

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import json
import uuid

# Compact advertise payload structure:
# { 'id': node_id, 'ts': ts, 'm': base64(metadata) }

DEFAULT_KEY = AESGCM.generate_key(bit_length=128)


def pack_adv_payload(node_id: str, metadata: dict, key: bytes = DEFAULT_KEY):
    aes = AESGCM(key)
    nonce = os.urandom(12)
    payload = json.dumps({'id': node_id, 'ts': __import__('time').time(), 'meta': metadata}).encode('utf-8')
    ct = aes.encrypt(nonce, payload, None)
    return nonce + ct  # small binary blob to put into advertisement service data


def unpack_adv_payload(blob: bytes, key: bytes = DEFAULT_KEY):
    aes = AESGCM(key)
    nonce = blob[:12]
    ct = blob[12:]
    pt = aes.decrypt(nonce, ct, None)
    return json.loads(pt.decode('utf-8'))


if __name__ == '__main__':
    # Demonstration
    node = str(uuid.uuid4())
    meta = {'name': 'node-ble'}
    b = pack_adv_payload(node, meta)
    print('Packed', len(b), 'bytes')
    print(unpack_adv_payload(b))
