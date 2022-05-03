"""File interface. Handles read/write, creation and deletion of files."""

import os
from pathlib import Path
from typing import Callable, Optional


PathFilterFunction = Callable[[str], bool]


# Read-only interface


def is_dir(path: str) -> bool:
    """Tell if a file is a directory."""
    return os.path.isdir(path)


def is_file(path: str) -> bool:
    """Tell if a path corresponds to an existing file."""
    return os.path.isfile(path)


def exists(path: str) -> bool:
    """Tell if a path exists."""
    return os.path.exists(path)


def join(*args: str) -> str:
    """Join path elemnts to give a full valid path."""
    return os.path.join(*args)


def list_dir(
    path: str,
    file_filter: Optional[PathFilterFunction] = None,
    base_name: bool = True,
) -> list[str]:
    """List files using an optional filter."""
    return [
        dir if base_name else os.path.join(path, dir)
        for dir in os.listdir(path)
        if not file_filter or file_filter(os.path.join(path, dir))
    ]


def get_file_base_name(file: str) -> str:
    """Return a file base name (without path)."""
    return os.path.basename(file)


# File modification interface


class InvalidFileError(Exception):
    """Raised when a file is not found."""


def create_file(file_name: str):
    """Creates an empty file."""
    with open(file_name, 'w') as file:
        if not file:
            raise InvalidFileError(f'File {file_name!r} not found.')


def create_directory(dir_name: str) -> None:
    """Create a new directory."""
    os.mkdir(dir_name)


def ensure_directory(dir_name: str) -> None:
    """Ensure a directory exist, create it otherwise."""
    if not exists(dir_name):
        create_directory(dir_name)


def remove_file(file_name: str) -> None:
    """Remove a file."""
    if not is_file(file_name):
        raise (FileNotFoundError(f'File {file_name!r} does not exist.'))
    os.remove(file_name)


def read_binary_file(file_name: str) -> bytes:
    """Read a binary file."""
    with open(file_name, 'rb') as file:
        if not file:
            raise InvalidFileError(f'File {file_name!r} not found.')
        return file.read()


def write_to_binary_file(file_name: str, content: bytes, append: bool) -> None:
    """Write bytes to a binary file."""
    mode = 'a' if append else 'w'
    mode += 'b'
    with open(file_name, mode) as file:
        if not file:
            raise InvalidFileError(f'File {file_name!r} not found.')
        file.write(content)


# Ensure cryptpath directories


class _CryptPathManager:
    """Contain cryptext paths."""

    path_ensured = False
    CRYPT_ROOT = str(Path.home())
    CRYPT_PATH = '.cryptext'
    PLUG_PATH = 'plugin'
    PASS_PATH = 'core'

    @staticmethod
    def crypt_path() -> str:
        """Return base cryptpath"""
        return join(_CryptPathManager.CRYPT_ROOT, _CryptPathManager.CRYPT_PATH)

    @staticmethod
    def plug_path() -> str:
        """Return path to plugins"""
        return join(
            _CryptPathManager.crypt_path(), _CryptPathManager.PLUG_PATH
        )

    @staticmethod
    def pass_path() -> str:
        """Return path to passwords"""
        return join(
            _CryptPathManager.crypt_path(), _CryptPathManager.PASS_PATH
        )

    @staticmethod
    def ensure_cryptpath_setup() -> None:
        """Ensure all cryptext directories exist."""
        if _CryptPathManager.path_ensured:
            return
        ensure_directory(_CryptPathManager.crypt_path())
        ensure_directory(_CryptPathManager.plug_path())
        ensure_directory(_CryptPathManager.pass_path())
        _CryptPathManager.path_ensured = True


def get_plugin_path(plugin_name: str) -> str:
    """Return a plugin full path given its name."""
    return join(_CryptPathManager.plug_path(), f'plugin{plugin_name}.py')


def get_password_path(password_name: str) -> str:
    """Return a password full path given its name."""
    return join(_CryptPathManager.pass_path(), password_name)


def list_plugins() -> list[str]:
    """List the plugins in the plugin directory."""
    _CryptPathManager.ensure_cryptpath_setup()
    return list_dir(
        _CryptPathManager.plug_path(),
        file_filter=lambda dir: dir != '__pycache__',
    )


def list_passwords() -> list[str]:
    """List the password files in the password directory."""
    _CryptPathManager.ensure_cryptpath_setup()
    return list_dir(_CryptPathManager.pass_path())
