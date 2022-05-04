#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..shell import Shell
from ..io.terminal_io import TerminalInterface


class Exit:
    @staticmethod
    def do(shell: Shell, line: str):
        if shell.session.name is not None:
            shell.session.save()
        TerminalInterface.print("You're quitting cryptext")
        shell.close()

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        pass

    @staticmethod
    def help(shell: Shell):
        pass
