"""Interfaces for cryptext."""

from .password_interface import (
    PasswordData,
    encrypt_password,
    decrypt_password,
)
from .file_interface import (
    get_password_path,
    get_plugin_path,
    list_plugins,
    list_passwords,
    create_password,
    remove_password,
    read_password_data,
    append_password_data,
)

__all__ = [
    'list_plugins',
    'list_passwords',
    'create_password',
    'remove_password',
    'get_password_path',
    'get_plugin_path',
    'PasswordData',
    'encrypt_password',
    'decrypt_password',
    'read_password_data',
    'append_password_data',
]
