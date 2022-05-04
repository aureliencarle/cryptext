"""
Password interface.

Password data container, encrypt and decrypt password data.
"""

from __future__ import annotations

from dataclasses import dataclass

import cryptography

from ..io.encrypter import Encrypter


class InvalidPassword(Exception):
    """Raised when an invalid password is given to decrypt a file."""


@dataclass
class PasswordData:
    """Password-related data stored in files,"""

    label: str = 'nyancat'
    url: str = 'https://www.nyan.cat/'
    com: str = 'sorry for this'
    user: str = 'captain madness'
    passwd: str = '1234'


def generate_password_key(password: str) -> bytes:
    """Generate a new key for a password."""
    return Encrypter.generate_hash_key(password)


def encrypt_password(key: bytes, password_data: str) -> bytes:
    """Encrypt text to bytes using a key."""
    return Encrypter.encrypt(key, password_data)


def decrypt_password(key: bytes, encoded_password_data: bytes) -> str:
    """Decrypt bytes using a key."""
    try:
        return Encrypter.decrypt(key, encoded_password_data)
    except cryptography.fernet.InvalidToken:
        raise InvalidPassword("The password given is invalid.")
