#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cryptext.session import SessionEnvironment
from cryptext.shell import Shell
from cryptext.commands import Ls, Cat, Touch, Mkdir, Rm, Cd, Exit


def main():
    Shell.register(Ls)
    Shell.register(Cat)
    Shell.register(Touch)
    Shell.register(Mkdir)
    Shell.register(Rm)
    Shell.register(Cd)
    Shell.register(Exit)

    session = SessionEnvironment()
    shell = Shell(session)
    shell.cmdloop()


if __name__ == '__main__':
    main()
