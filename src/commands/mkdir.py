#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.shell import Shell

class Mkdir:

    @staticmethod
    def do(shell: Shell, line: str):
        arguments = shell.get_arguments(line)
        shell.session.create(arguments['parameter'])

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        pass

    @staticmethod
    def help(shell: Shell):
        pass
