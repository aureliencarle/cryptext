#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.shell import Shell

class Start:

    @staticmethod
    def do(shell: Shell, line: str):
        if not line:
            Start.help(shell)
            return
        arguments = shell.get_arguments(line)
        if shell.session.start(arguments['parameter']):
            shell.prompt = shell.session.prompt
        else:
            Start.help(shell)

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        if not text:
            completions = [k for k in shell.session.files]
        else:
            completions = [k
                            for k in shell.session.files
                            if k.startswith(text)
                            ]
        return completions

    @staticmethod
    def help(shell: Shell):
        shell.session.log()
