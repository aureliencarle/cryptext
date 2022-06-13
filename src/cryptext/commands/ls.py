#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..shell import Shell


class Ls:
    @staticmethod
    def do(shell: Shell, line: str):
        if shell.session.name is None:
            shell.session.user_interface.list_directories(shell.session.files)
            return
        label_list = list(shell.session.content.keys())
        label_list.sort()
        shell.session.user_interface.list_files(label_list)

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        pass

    @staticmethod
    def help(shell: Shell):
        pass
