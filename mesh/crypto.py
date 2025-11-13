"""Cryptographic helpers for mesh sync.

Provides ECDH (X25519) key agreement, HKDF key derivation, AES-GCM encryption and HMAC-SHA256.
Requires the `cryptography` package.
"""
from typing import Tuple
import base64

try:
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives import hashes, hmac
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.serialization import PublicFormat, Encoding
    from cryptography.hazmat.backends import default_backend
    import os
except Exception as e:
    raise ImportError("cryptography package required for mesh.crypto: " + str(e))


def generate_keypair() -> Tuple[bytes, X25519PrivateKey]:
    priv = X25519PrivateKey.generate()
    pub = priv.public_key()
    pub_bytes = pub.public_bytes(Encoding.Raw, PublicFormat.Raw)
    return pub_bytes, priv


def derive_keys(priv: X25519PrivateKey, peer_pub_bytes: bytes) -> Tuple[bytes, bytes]:
    peer_pub = X25519PublicKey.from_public_bytes(peer_pub_bytes)
    shared = priv.exchange(peer_pub)
    # derive two 32-byte keys: enc_key and mac_key
    hkdf = HKDF(algorithm=hashes.SHA256(), length=64, salt=None, info=b'rechain mesh v1', backend=default_backend())
    out = hkdf.derive(shared)
    enc_key = out[:32]
    mac_key = out[32:]
    return enc_key, mac_key


def encrypt_and_mac(plaintext: bytes, enc_key: bytes, mac_key: bytes) -> Tuple[bytes, bytes, bytes]:
    # AES-GCM for encryption
    aes = AESGCM(enc_key)
    nonce = os.urandom(12)
    ct = aes.encrypt(nonce, plaintext, None)
    # HMAC over nonce + ct
    h = hmac.HMAC(mac_key, hashes.SHA256(), backend=default_backend())
    h.update(nonce + ct)
    mac = h.finalize()
    return nonce, ct, mac


def verify_and_decrypt(nonce: bytes, ct: bytes, mac: bytes, enc_key: bytes, mac_key: bytes) -> bytes:
    h = hmac.HMAC(mac_key, hashes.SHA256(), backend=default_backend())
    h.update(nonce + ct)
    h.verify(mac)
    aes = AESGCM(enc_key)
    pt = aes.decrypt(nonce, ct, None)
    return pt


def b64(x: bytes) -> str:
    return base64.b64encode(x).decode('ascii')


def ub64(s: str) -> bytes:
    return base64.b64decode(s.encode('ascii'))
