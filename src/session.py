#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from getpass import getpass
import os

import cryptography
from regex import W

from src.password import PasswordData, PasswordDataIO
from src.cryptpath import CRYPTPATH

from src.utils import DisplayConfig, Io, Crypt


class SessionEnvironment:
    def __init__(
        self, crypt_path: str = CRYPTPATH, prompt: str = DisplayConfig.PROMPT
    ):
        self.name = None
        self.prompt = DisplayConfig.PROMPT
        self.passpath = crypt_path
        self.files = os.listdir(crypt_path)
        self.key = None
        self.content = {}

    def start(self, session_name: str = None) -> bool:
        if session_name != '':
            if session_name in self.files:
                self.name = session_name
            else:
                Io.print(' -- file not found --')
                creation = Io.input('Do you want to create it ? [yes] : ')
                if creation == 'yes':
                    self.create(session_name)
                    self.start(session_name)
                return False
            passwd = PasswordDataIO.input_password()
            try:
                self.update(passwd)
            except cryptography.fernet.InvalidToken:
                self.name = None
                Io.print(' -- wrong file key --')
                return False
            return True
        else:
            Io.print('Nothing to start')
            return False

    def print_content(self, key: str, is_secure: bool) -> None:
        """Print a content based on its key"""
        PasswordDataIO.print(self.content[key], is_secure=is_secure)

    def create(self, name):
        file = os.path.join(self.passpath, name)
        if not os.path.exists(file):
            with open(file, 'w'):
                pass
        else:
            Io.print('file already exist')
        self.files = os.listdir(CRYPTPATH)

    def destroy(self, name: str) -> None:
        pass
        # pathfile = self.passpath+'/'+self.name+'/'+name
        # if os.path.exists(pathfile):
        #    os.remove(pathfile)
        # else:
        #    Io.print('file does not exist')

    def update(self, password: str) -> None:
        self.prompt = f'({self.name}) {DisplayConfig.PROMPT}'
        self.key = self.get_key(password)
        self.recover_password_data()

    def get_key(self, password: str) -> bytes:
        return Crypt.generate_hash_key(password)

    def generate_path(self) -> str:
        return os.path.join(self.passpath, self.name)

    def recover_password_data(self):
        self.content.clear()
        for l in Crypt.read(self.generate_path()):
            args = Crypt.decrypt(self.key, l).split(DisplayConfig.SEPARATOR)
            if args:
                p = PasswordData(*args)
                self.content.update({p.label: p})

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
