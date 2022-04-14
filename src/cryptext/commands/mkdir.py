#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..shell import Shell


class Mkdir:
    @staticmethod
    def do(shell: Shell, line: str):
        parameter, _ = shell.get_arguments(line)
        shell.session.create_session(parameter)

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        pass

    @staticmethod
    def help(shell: Shell):
        pass
