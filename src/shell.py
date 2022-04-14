#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cmd
import sys
from typing import List, Tuple

from src.session import SessionEnvironment


class Shell(cmd.Cmd):
    def __init__(self, session) -> None:
        super().__init__()
        self.session: SessionEnvironment = session
        self.update_prompt()

    def close(self):
        sys.exit()

    def update_prompt(self) -> None:
        self.prompt = self.session.prompt

    def start_session(self, session_name: str) -> bool:
        if self.session.start_session(session_name):
            self.update_prompt()
            return True
        return False

    def close_session(self) -> None:
        self.session.close_session()
        self.update_prompt()

    def get_arguments(self, line: str) -> Tuple[str, List[str]]:
        if line:
            parameter, *args = line.split()
            return parameter, args
        return '', []

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
            help_func=getattr(cls, 'help'),
        )
