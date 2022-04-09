#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64, hashlib
from cryptography.fernet import Fernet
from getpass import getpass
from src.utils import Io, Geometry


class Crypt:
    @staticmethod
    def pass_confirmation_ask(input_text, n_trials=2):
        if n_trials <= 0:
            Io.print('code not added !')
            return None
        pas = getpass(' ' * Geometry.INDENT + input_text)
        cof = getpass(' ' * Geometry.INDENT + 'confirm : ')
        if pas == cof:
            return pas
        else:
            Io.print(f'!!! password do not match !!! left {n_trials-1} try')
            return Crypt.pass_confirmation_ask(
                input_text=input_text, n_trials=n_trials - 1
            )

    @staticmethod
    def pass_ask(input_text):
        return getpass(input_text)

    @staticmethod
    def generate_hash_key(clear_pass):
        encoded_pass = clear_pass.encode('utf-8')
        hash_key = hashlib.md5(encoded_pass).hexdigest()
        return base64.urlsafe_b64encode(hash_key.encode('utf-8'))

    @staticmethod
    def crypt(key, clear_text):
        fernet = Fernet(key)
        encrypted = fernet.encrypt(clear_text.encode('utf-8'))
        return encrypted

    @staticmethod
    def decrypt(key, encoded_text):
        fernet = Fernet(key)
        clear_text = fernet.decrypt(encoded_text)
        return clear_text.decode('utf-8')

    @staticmethod
    def read(name):
        with open(name, 'rb') as encrypted_file:
            text = encrypted_file.read()
            return text.split()

    @staticmethod
    def write(name, key, text):
        with open(name, 'ab') as encrypted_file:
            encrypted_file.write('\n'.encode('utf-8'))
            encrypted_file.write(Crypt.crypt(key, text))

    @staticmethod
    def get_entry(input_text, space, default_text='none'):
        result = Io.input(f'[{input_text}]{space} -> ') or default_text
        return result
