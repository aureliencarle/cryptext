#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.shell import Shell
from src.utils.io import Io, Format

class Ls:

    @staticmethod
    def do(shell: Shell, line: str):
        if shell.session.name is None:
            Io.print(Format.pretty_columns(shell.session.files))
            return
        label_list = list(shell.session.content.keys())
        label_list.sort()
        Io.col_print(label_list)

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        pass

    @staticmethod
    def help(shell: Shell):
        pass
