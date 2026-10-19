"""
AES Encryption/Decryption utility for GetStego.
Wraps messages with AES-CBC encryption before LSB embedding.
"""

import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os


def _derive_key(key_str: str) -> bytes:
    """Derive a 32-byte AES key from any string via SHA-256."""
    return hashlib.sha256(key_str.encode('utf-8')).digest()


def aes_encrypt(message: str, key_str: str) -> str:
    """
    Encrypt a plaintext message with AES-CBC using a string key.
    Returns a base64-encoded ciphertext string.
    """
    key = _derive_key(key_str)
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    # Prefix IV to ciphertext, then base64 encode
    encrypted = base64.b64encode(iv + ct_bytes).decode('utf-8')
    return encrypted


def aes_decrypt(encrypted_b64: str, key_str: str) -> str:
    """
    Decrypt a base64-encoded AES-CBC ciphertext using a string key.
    Returns the original plaintext message.
    """
    key = _derive_key(key_str)
    raw = base64.b64decode(encrypted_b64.encode('utf-8'))
    iv = raw[:16]
    ct = raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ct), AES.block_size)
    return plaintext.decode('utf-8')
