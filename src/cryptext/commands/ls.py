#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..shell import Shell
from ..io.terminal_io import TerminalInterface, Format


class Ls:
    @staticmethod
    def do(shell: Shell, line: str):
        if shell.session.name is None:
            TerminalInterface.print(
                Format.pretty_columns(
                    Format.styled_list(shell.session.files, 'blue', 'bright')
                )
            )
            return
        label_list = list(shell.session.content.keys())
        label_list.sort()
        TerminalInterface.print(
            Format.pretty_columns(Format.styled_list(label_list, 'yellow'))
        )

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        pass

    @staticmethod
    def help(shell: Shell):
        pass
