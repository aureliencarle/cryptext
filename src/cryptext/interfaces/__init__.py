"""Interfaces defined to decouple different parts of cryptext."""

from .password_interface import (
    PasswordData,
    encrypt_password,
    decrypt_password,
)

__all__ = ['PasswordData', 'encrypt_password', 'decrypt_password']
