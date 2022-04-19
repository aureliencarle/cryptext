#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cryptext.session import SessionEnvironment
from cryptext.shell import Shell
from cryptext.command_register import Register


def main():
    session = SessionEnvironment()
    shell = Shell(session)
    shell.cmdloop()


if __name__ == '__main__':
    main()
