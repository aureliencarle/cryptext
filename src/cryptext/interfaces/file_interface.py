"""File interface. Handles read/write, creation and deletion of files."""

from pathlib import Path
from .file_io import (
    create_file,
    join,
    list_dir,
    ensure_directory,
    exists,
    remove_file,
)


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


def password_exists(password_name: str) -> bool:
    """Tell if a password exist."""
    return exists(join(_CryptPathManager.pass_path(), password_name))


def get_plugin_path(plugin_name: str) -> str:
    """Return a plugin full path given its name."""
    return join(_CryptPathManager.plug_path(), f'plugin{plugin_name}.py')


def get_password_path(password_name: str) -> str:
    """Return a password full path given its name."""
    return join(_CryptPathManager.pass_path(), password_name)


def create_password(password_name: str) -> None:
    """Create a new password file."""
    create_file(join(_CryptPathManager.pass_path(), password_name))


def remove_password(password_name: str) -> None:
    """Remove a password file."""
    remove_file(join(_CryptPathManager.pass_path(), password_name))


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
