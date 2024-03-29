#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
from typing import Dict, List, Optional, Protocol

import pyperclip

from cryptext.interfaces.user_interface import UserInterface
from cryptext.interfaces.password_interface import (
    PasswordData,
    InvalidPassword,
    deserialize_password,
    generate_password_key,
    encrypt_password,
    decrypt_password,
    serialize_password,
)
from cryptext.interfaces.file_interface import (
    list_passwords,
    list_plugins,
    get_password_path,
    get_plugin_path,
    password_exists,
    create_password,
    remove_password,
    read_password_data,
    append_password_data,
)


class PluginProtocol(Protocol):
    """Plugin protocol to define what a plugin should provide as interface."""

    import_session: str
    import_pass: List[PasswordData]


class SessionEnvironment:
    def __init__(self, user_interface=UserInterface(), session_name=None):
        self.name: Optional[str] = None
        self.user_interface = user_interface
        self.prompt: str = user_interface.get_prompt(session_name)
        self.files: List[str] = list_passwords()
        self.plugins = list_plugins()
        self.key: bytes = None
        self.content: Dict[str, PasswordData] = {}

        if session_name is not None:
            self.start_session(session_name)

    def start_session(self, session_name: str = None) -> bool:
        """Start a new session."""
        if not self.ensure_session(session_name=session_name):
            return False
        self.name = session_name
        passwd = self.user_interface.input_password(confirm=False)
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
        self.user_interface.error('File not found')
        return self.create_session(
            session_name=session_name, ask_confirmation=True
        )

    def plug_external(self, script_name: str = '') -> None:
        """Take from external script one value for session name and list of PassordData"""
        specification = importlib.util.spec_from_file_location(
            script_name, get_plugin_path(script_name),
        )
        external_module = importlib.util.module_from_spec(specification)
        try:
            specification.loader.exec_module(external_module)
        except FileNotFoundError:
            self.user_interface.error(f'Plugin {script_name!r} not found.')
            return
        plugin: PluginProtocol = external_module

        self.start_session(plugin.import_session)
        for p in plugin.import_pass:
            self.add_password(p)
        self.close_session()

    def create_session(
        self, session_name: str, ask_confirmation: bool = True
    ) -> bool:
        """Create a new session"""
        file = get_password_path(session_name)
        if not password_exists(file):
            confirm = (
                not ask_confirmation
                or self.user_interface.ask_user_confirmation(
                    'File does not exist. Create it ?', default_str='y'
                )
            )
            if confirm:
                create_password(session_name)
                self.files.append(session_name)
                return True
            self.user_interface.info('New file cannot be created')
            return False
        self.user_interface.info('File already exists')
        return False

    def clipboard_copy(self, key: str) -> None:
        """Copy password to clipboard"""
        self.print_password_data(key, summary=True)
        pyperclip.copy(self.content[key].passwd)

    def print_content(self, key: str, is_secure: bool) -> None:
        """Print a content based on its key"""
        self.print_password_data(key, is_secure=is_secure)

    def input_password_data(self, label: str) -> PasswordData:
        """Input a password data from the user."""
        self.user_interface.print(f'Creating password: {label!r}')
        url, com, user = self.user_interface.input_attributes(
            ['url', 'com', 'user']
        )
        passwd = self.user_interface.input_password(confirm=True)
        return PasswordData(
            label=label, url=url, com=com, user=user, passwd=passwd
        )

    def print_password_data(
        self, label: str, summary: bool = False, is_secure: bool = True
    ) -> None:
        """Print password data in the terminal."""
        pass_data = self.content[label]
        if summary:
            attrs = [
                (pass_data.url, 'url', 'magenta'),
                (pass_data.com, 'comment', 'yellow'),
            ]
        else:
            attrs = [
                (pass_data.url, 'url', 'magenta'),
                (pass_data.com, 'comment', 'yellow'),
                (pass_data.user, 'user', 'cyan'),
                (pass_data.passwd, 'pass', 'red'),
            ]
        self.user_interface.print_attributes(
            title=f'Password data {label!r}:', attrs=attrs
        )
        if not summary and is_secure:
            self.user_interface.secure_line('--- Mischief Managed! ---')

    def destroy(self, name: str) -> None:
        if password_exists(name):
            self.files.remove(name)
            remove_password(name)
            self.files = list_passwords()
        else:
            self.user_interface.error('File does not exist')

    def update(self, password: str) -> bool:
        try:
            self.prompt = self.user_interface.get_prompt(session=self.name)
            self.key = self.get_key(password)
            self.recover_password_data()
            return True
        except InvalidPassword:
            self.name = None
            self.user_interface.error('Wrong file key')
            return False

    def get_key(self, password: str) -> bytes:
        return generate_password_key(password)

    def generate_path(self) -> str:
        return get_password_path(self.name)

    def add_password(self, password: PasswordData):
        if password.label not in self.content.keys():
            self.content[password.label] = password
        else:
            self.user_interface.error('Label already exists')

    def recover_password_data(self):
        self.content.clear()
        for passwd in SessionEnvironment.read_password(self.generate_path()):
            password_str = decrypt_password(self.key, passwd)
            if password_str:
                password = deserialize_password(password_str)
                self.content[password.label] = password

    def save(self):
        file = self.generate_path()
        for _, value in self.content.items():
            writable_pass = serialize_password(value)
            SessionEnvironment.write_password(file, self.key, writable_pass)

    def log(self):
        if self.name is None:
            message = 'No session is loaded !'
        else:
            message = f'# Session loaded : {self.name}\n'
        self.user_interface.info(message)

    @staticmethod
    def read_password(password_name: str) -> list[bytes]:
        """Read the content of a password file."""
        return read_password_data(password_name)

    @staticmethod
    def write_password(password_name: str, key: bytes, text: str) -> None:
        """Write a password into the corresponding file (append)."""
        byte_output = encrypt_password(key, text)
        byte_output += '\n'.encode('utf-8')
        append_password_data(
            password_name=password_name, password_data=byte_output
        )
