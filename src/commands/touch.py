#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.shell import Shell
from src.utils import DisplayConfig, Io, Crypt
from src.password import PasswordData, PasswordDataIO


class Touch:
    @staticmethod
    def do(shell: Shell, line: str):
        if shell.session.name is None:
            Touch.help(shell)
            return
        password = PasswordDataIO.input()
        shell.session.add_password(password)
        #readable_pass = PasswordDataIO.convert(password)
        #password.write(shell.session.generate_path(), shell.session.key)
        #shell.session.recover_password_data()

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        pass

    @staticmethod
    def help(shell: Shell):
        Io.print('you need a session to add a pass')
