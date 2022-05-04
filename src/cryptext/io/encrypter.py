"""Encrypter class."""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import hashlib
from cryptography.fernet import Fernet


class Encrypter:
    """Encrypt and decrypt data from password keys."""

    @staticmethod
    def generate_hash_key(clear_pass: str) -> bytes:
        """Generate a new hash key from a password string."""
        encoded_pass = clear_pass.encode('utf-8')
        hash_key = hashlib.md5(encoded_pass).hexdigest()
        return base64.urlsafe_b64encode(hash_key.encode('utf-8'))

    @staticmethod
    def encrypt(key: bytes, clear_text: str) -> bytes:
        """Encrypt a text using a hash key."""
        fernet = Fernet(key)
        encrypted = fernet.encrypt(clear_text.encode('utf-8'))
        return encrypted

    @staticmethod
    def decrypt(key: bytes, encoded_text: bytes) -> str:
        """Decrypt a text using a hash key."""
        fernet = Fernet(key)
        clear_text = fernet.decrypt(encoded_text)
        return clear_text.decode('utf-8')
