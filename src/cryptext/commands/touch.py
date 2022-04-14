#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..shell import Shell
from ..utils import Io
from ..password import PasswordDataIO


class Touch:
    @staticmethod
    def do(shell: Shell, line: str):
        if shell.session.name is None:
            Touch.help(shell)
            return
        password = PasswordDataIO.input()
        shell.session.add_password(password)

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        pass

    @staticmethod
    def help(shell: Shell):
        Io.print('you need a session to add a pass')
