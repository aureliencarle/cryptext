#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.shell import Shell
from src.utils import Io

class Rm:

    @staticmethod
    def do(shell: Shell, line: str):
        parameter, options = shell.get_arguments(line)
        if shell.session.name is None:
            if '-r' in options and parameter in shell.session.files:
                shell.session.destroy(parameter)
            else:
                Rm.help(shell)
        elif parameter in list(shell.session.content.keys()):
            del shell.session.content[parameter]
        else:
            Rm.help(shell)

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        listing = shell.session.content.keys()
        if shell.session.name is None:
            listing = shell.session.files
        return [
            k
            for k in listing
            if not text or k.startswith(text)
        ]

    @staticmethod
    def help(shell: Shell):
        Io.print('To remove a directory type -r as option')
