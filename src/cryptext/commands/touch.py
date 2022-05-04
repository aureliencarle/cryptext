#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..shell import Shell
from ..password import PasswordDataIO


class Touch:
    @staticmethod
    def do(shell: Shell, line: str):
        if shell.session.name is None:
            Touch.help(shell)
            return
        try:
            parameter, _ = shell.get_arguments(line)
            if not parameter:
                Touch.help(shell)
                return
            password = PasswordDataIO.input(label=parameter)
            shell.session.add_password(password)
        except KeyboardInterrupt:
            shell.session.user_interface.error(
                'KeyboardInterrupt exception, abort file creation'
            )

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        pass

    @staticmethod
    def help(shell: Shell):
        shell.session.user_interface.print(
            'Once in an active session, type \'touch <file_name>\''
        )
