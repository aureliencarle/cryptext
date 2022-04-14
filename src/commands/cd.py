#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.shell import Shell


class Cd:
    @staticmethod
    def do(shell: Shell, line: str):
        if not line:
            Cd.help(shell)
            return
        parameter, _ = shell.get_arguments(line)
        if parameter == '..':
            shell.session.close_session()
            shell.prompt = shell.session.prompt
            return
        elif shell.session.start_session(parameter):
            shell.prompt = shell.session.prompt
        else:
            Cd.help(shell)

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        return [
            k for k in shell.session.files if not text or k.startswith(text)
        ]

    @staticmethod
    def help(shell: Shell):
        shell.session.log()
