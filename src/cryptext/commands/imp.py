#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..shell import Shell
from ..io.terminal_io import TerminalInterface


class Import:
    @staticmethod
    def do(shell: Shell, line: str):
        if not line:
            Import.help(shell)
            return
        parameter, _ = shell.get_arguments(line)
        shell.session.plug_external(parameter)

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        return [
            k.removesuffix('.py')
            for k in shell.session.plugins
            if not text or k.startswith(text)
        ]

    @staticmethod
    def help(shell: Shell):
        TerminalInterface.print('Need plug-in name')
