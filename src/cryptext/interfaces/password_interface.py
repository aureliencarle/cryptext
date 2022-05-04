"""
Password interface.

Password data container, encrypt and decrypt password data.
"""

from __future__ import annotations

from dataclasses import dataclass

import cryptography

from ..utils.hashing import Crypt


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

    @staticmethod
    def compactify_to_str(pass_data: PasswordData, separator: str) -> str:
        compact = separator.join(
            [
                pass_data.label,
                pass_data.url,
                pass_data.com,
                pass_data.user,
                pass_data.passwd,
            ]
        )
        return compact


def encrypt_password(key: bytes, password_data: str) -> bytes:
    Crypt.encrypt(key, password_data)


def decrypt_password(key: bytes, encoded_password_data: bytes) -> str:
    try:
        return Crypt.decrypt(key, encoded_password_data)
    except cryptography.fernet.InvalidToken:
        raise InvalidPassword("The password given is invalid.")
