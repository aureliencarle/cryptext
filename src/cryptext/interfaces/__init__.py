"""Interfaces for cryptext."""

from .password_interface import (
    PasswordData,
    encrypt_password,
    decrypt_password,
)
from .file_interface import PathFilterFunction, InvalidFileError
from .file_interface import (
    is_dir,
    is_file,
    exists,
    join,
    list_dir,
    get_file_base_name,
    create_file,
    remove_file,
    read_binary_file,
    write_to_binary_file,
    get_password_path,
    get_plugin_path,
    list_plugins,
    list_passwords,
)

__all__ = [
    'PathFilterFunction',
    'InvalidFileError',
    'is_dir',
    'is_file',
    'exists',
    'join',
    'list_dir',
    'get_file_base_name',
    'create_file',
    'remove_file',
    'read_binary_file',
    'write_to_binary_file',
    'list_plugins',
    'list_passwords',
    'get_password_path',
    'get_plugin_path',
    'PasswordData',
    'encrypt_password',
    'decrypt_password',
]
