#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.shell import Shell
from src.utils.io import Io


class Exit:
    @staticmethod
    def do(shell: Shell, line: str):
        shell.session.save()
        Io.print("You're quitting cryptext")
        shell.close()

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        pass

    @staticmethod
    def help(shell: Shell):
        pass
