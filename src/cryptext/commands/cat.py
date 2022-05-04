#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..shell import Shell


class Cat:
    @staticmethod
    def do(shell: Shell, line: str):
        try:
            parameter, options = shell.get_arguments(line)
            secure = '--no-secure' not in options

            if parameter in shell.session.content.keys():
                shell.session.print_content(parameter, secure)

        except IndexError:
            shell.session.user_interface.error(
                f'File {parameter!r} does not exist'
            )
            Cat.help(shell)

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        return [
            k
            for k in shell.session.content.keys()
            if not text or k.startswith(text)
        ]

    @staticmethod
    def help(shell: Shell):
        shell.session.user_interface.print(
            'help :: show <label> [--no-secure]'
        )
