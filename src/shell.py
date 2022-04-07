#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cmd

from src.password   import Password
from src.utils      import *


class Shell(cmd.Cmd):
    prompt  = ALINEA
    session = None

    def __init__(self, session) -> None:
        super().__init__()
        self.session    = session
        self.prompt     = self.session.prompt

    def exit(exit_code: int=0) -> None:
        exit(exit_code)

    def get_arguments(self, line):
        arguments = {}
        all_parameters = line.split()
        arguments.update({'parameter' : all_parameters[0]})
        options = [
            p for p in all_parameters[1:] if p.startswith('-')
        ]
        arguments.update({'options' : options})
        return arguments

    # Needed to not repeat the last sucess command if you spam return ;)
    def emptyline(self):
        pass

    @staticmethod
    def _register(name, do_func, complete_func, help_func):
        setattr(Shell, f'do_{name}', do_func)
        setattr(Shell, f'complete_{name}', complete_func)
        setattr(Shell, f'help_{name}', help_func)

    @staticmethod
    def get_method_name(cls_name):
        return cls_name.lower()

    @staticmethod
    def register(cls):
        """Register a new commands by reading methods 'do', 'complete' and 'help'"""
        name = Shell.get_method_name(cls.__name__)
        Shell._register(
            name=name,
            do_func=getattr(cls, 'do'),
            complete_func=getattr(cls, 'complete'),
            help_func=getattr(cls, 'help')
        )

