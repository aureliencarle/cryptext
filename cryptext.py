#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.session import SessionEnvironment
from src.shell import Shell
from src.commands import (
    Ls,
    Show,
    Add,
    Create,
    Cd,
    Exit
)

def main():
    Shell.register(Ls)
    Shell.register(Show)
    Shell.register(Add)
    Shell.register(Create)
    Shell.register(Cd)
    Shell.register(Exit)

    session = SessionEnvironment()
    shell = Shell(session)
    shell.cmdloop()


if __name__ == '__main__':
    main()