#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
from typing import Dict, List, Optional, Protocol

import cryptography
import pyperclip

from cryptext.password import PasswordDataIO
from cryptext.interfaces import (
    file_interface,
    password_interface,
    PasswordData,
)
from cryptext.utils import DisplayConfig, Io, Format
from cryptext.io import file_io


class PluginProtocol(Protocol):
    """Plugin protocol to define what a plugin should provide as interface."""

    import_session: str
    import_pass: List[PasswordData]


class SessionEnvironment:
    def __init__(self, session_name=None):
        self.name: Optional[str] = None
        self.prompt: str = DisplayConfig.PROMPT
        self.files: List[str] = file_interface.list_passwords()
        self.plugins = file_interface.list_plugins()
        self.key: bytes = None
        self.content: Dict[str, PasswordData] = {}

        if session_name is not None:
            self.start_session(session_name)

    def start_session(self, session_name: str = None) -> bool:
        """Start a new session."""
        if not self.ensure_session(session_name=session_name):
            return False
        self.name = session_name
        passwd = PasswordDataIO.input_password()
        return self.update(passwd)

    def close_session(self) -> bool:
        """Close current session"""
        self.save()
        self.__init__()

    def ensure_session(self, session_name: str) -> bool:
        """Ensure a new session is created if it does not exist"""
        if not session_name:
            return False
        if session_name in self.files:
            return True
        Io.print(' -- file not found --')
        return self.create_session(
            session_name=session_name, ask_confirmation=True
        )

    def plug_external(self, script_name: str = '') -> None:
        """Take from external script one value for session name and list of PassordData"""
        specification = importlib.util.spec_from_file_location(
            script_name, file_interface.get_plugin_path(script_name),
        )
        external_module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(external_module)
        plugin: PluginProtocol = external_module

        self.start_session(plugin.import_session)
        for p in plugin.import_pass:
            self.add_password(p)
        self.close_session()

    def create_session(
        self, session_name: str, ask_confirmation: bool = True
    ) -> bool:
        """Create a new session"""
        file = file_interface.get_password_path(session_name)
        if not file_interface.exists(file):
            confirm = not ask_confirmation or Io.ask_user_confirmation(
                'File does not exist. Create it ?', default_str='y'
            )
            if confirm:
                file_interface.create_password(session_name)
                self.files.append(session_name)
                return True
            Io.print('New file cannot be created')
            return False
        Io.print('File already exist')
        return False

    def clipboard_copy(self, key: str) -> None:
        """Copy password to clipboard"""
        PasswordDataIO.summary(self.content[key])
        pyperclip.copy(self.content[key].passwd)

    def print_content(self, key: str, is_secure: bool) -> None:
        """Print a content based on its key"""
        PasswordDataIO.print(self.content[key], is_secure=is_secure)

    def destroy(self, name: str) -> None:
        if file_interface.password_exists(name):
            self.files.remove(name)
            file_interface.remove_password(name)
            self.files = file_interface.list_passwords()
        else:
            Io.print('File does not exist')

    def update(self, password: str) -> bool:
        try:
            self.prompt = f'({Format.styled(self.name, "cyan", "bright")}) {DisplayConfig.PROMPT}'
            self.key = self.get_key(password)
            self.recover_password_data()
            return True
        except cryptography.fernet.InvalidToken:
            self.name = None
            Io.print(' -- wrong file key --')
            return False

    def get_key(self, password: str) -> bytes:
        return password_interface.generate_password_key(password)

    def generate_path(self) -> str:
        return file_interface.get_password_path(self.name)

    def add_password(self, password: PasswordData):
        if password.label not in self.content.keys():
            self.content[password.label] = password
        else:
            Io.print(' -- label already exist --')

    def recover_password_data(self):
        self.content.clear()
        for l in SessionEnvironment.read_password(self.generate_path()):
            args = password_interface.decrypt_password(self.key, l).split(
                DisplayConfig.SEPARATOR
            )
            if args:
                p = PasswordData(*args)
                self.content[p.label] = p

    def save(self):
        file = self.generate_path()
        for k in self.content.keys():
            writable_pass = PasswordDataIO.convert(self.content[k])
            SessionEnvironment.write_password(file, self.key, writable_pass)

    def log(self):
        if self.name is None:
            message = 'No session is loaded !'
        else:
            message = f'# Session loaded : {self.name}\n'
        Io.print(message)

    @staticmethod
    def read_password(file_name: str) -> list[bytes]:
        """Read the content of a password file."""
        return file_io.read_binary_file(file_name).split()

    @staticmethod
    def write_password(file_name: str, key: bytes, text: str) -> None:
        """Write a password into the corresponding file (append)."""
        byte_output = password_interface.encrypt_password(key, text)
        byte_output += '\n'.encode('utf-8')
        file_io.write_to_binary_file(
            file_name=file_name, content=byte_output, append=True,
        )
