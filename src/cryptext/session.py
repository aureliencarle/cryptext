#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import cryptography
from typing import Dict, List

from .password import PasswordData, PasswordDataIO
from .cryptpath import CRYPTPATH

from .utils import DisplayConfig, Io, Crypt, Format


class SessionEnvironment:
    def __init__(self):
        self.set_default()

    def set_default(
        self, crypt_path: str = CRYPTPATH, prompt: str = DisplayConfig.PROMPT
    ):
        self.name: str = None
        self.prompt: str = prompt
        self.passpath: str = crypt_path
        self.files: List[str] = os.listdir(crypt_path)
        self.key: bytes = None
        self.content: Dict[str, PasswordData] = {}

    def start_session(self, session_name: str = None) -> bool:
        """Start a new session."""
        if not self.ensure_session(session_name=session_name):
            Io.print('Nothing to start')
            return False
        self.name = session_name
        passwd = PasswordDataIO.input_password()
        return self.update(passwd)

    def close_session(self) -> bool:
        """Close current session"""
        self.save()
        self.set_default()

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

    def create_session(
        self, session_name: str, ask_confirmation: bool = True
    ) -> bool:
        """Create a new session"""
        file = os.path.join(self.passpath, session_name)
        if not os.path.exists(file):
            confirm = not ask_confirmation or Io.ask_user_confirmation(
                'File does not exist. Create it ?', default_str='y'
            )
            if confirm:
                with open(file, 'w'):
                    self.files.append(session_name)
                    return True
            Io.print('New file cannot be created')
            return False
        Io.print('File already exist')
        return False

    def print_content(self, key: str, is_secure: bool) -> None:
        """Print a content based on its key"""
        PasswordDataIO.print(self.content[key], is_secure=is_secure)

    def destroy(self, name: str) -> None:
        pathfile = self.passpath + '/' + name
        if os.path.exists(pathfile):
            self.files.remove(name)
            os.remove(pathfile)
            self.files = os.listdir(CRYPTPATH)
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
        return Crypt.generate_hash_key(password)

    def generate_path(self) -> str:
        return os.path.join(self.passpath, self.name)

    def add_password(self, password: PasswordData):
        if password.label not in self.content.keys():
            self.content[password.label] = password
        else:
            Io.print(' -- label already exist --')

    def recover_password_data(self):
        self.content.clear()
        for l in Crypt.read(self.generate_path()):
            args = Crypt.decrypt(self.key, l).split(DisplayConfig.SEPARATOR)
            if args:
                p = PasswordData(*args)
                self.content[p.label] = p

    def save(self):
        file = os.path.join(self.passpath, self.name)
        open(file, 'w').close()
        for k in self.content.keys():
            writable_pass = PasswordDataIO.convert(self.content[k])
            PasswordDataIO.write(self.generate_path(), self.key, writable_pass)

    def log(self):
        if self.name is None:
            message = '\nNo session is loaded !\n'
        else:
            message = (
                '#=======================================\n'
                '#\n'
                f'# Session loaded : {self.name}\n'
                '#'
                '#=======================================\n'
            )
        Io.print(message)
