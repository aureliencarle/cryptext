#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.shell import Shell
from src.utils import Io

class Rm:

    @staticmethod
    def do(shell: Shell, line: str):
        if shell.session.name is None:
            pass
        shell.session.destroy(line)

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        pass

    @staticmethod
    def help(shell: Shell):
        pass