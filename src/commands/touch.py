#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.shell import Shell
from src.utils import Geometry, Io, Crypt
from src.password import PasswordData, PasswordDataIO


class Touch:
    @staticmethod
    def do(shell: Shell, line: str):
        if shell.session.name is None:
            Touch.help(shell)
            return
        password = PasswordDataIO.input()

        password.convert(shell.session.generate_path(), shell.session.key)
        del password
        shell.session.recover(PasswordData)

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        pass

    @staticmethod
    def help(shell: Shell):
        Io.print('you need a session to add a pass')
