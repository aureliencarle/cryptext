#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.shell import Shell
from src.utils import Geometry, Io, Crypt
from src.password import Password

class Add:

    @staticmethod
    def do(shell: Shell, line: str):
        if shell.session.name is None:
            Add.help(shell)
            return
        lab = Crypt.get_entry('label','  ')
        url = Crypt.get_entry('url','    ')
        com = Crypt.get_entry('comment', '')
        usr = Crypt.get_entry('usr', '    ')
        has = Crypt.pass_confirmation_ask('pass    : ')
        password = Password(
            lab=lab,
            url=url,
            com=com,
            usr=usr,
            has=has
        )

        password.convert(shell.session.generate_path(), shell.session.key)
        del password
        shell.session.recover(Password)

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        pass

    @staticmethod
    def help(shell: Shell):
        Io.print('you need a session to add a pass')
