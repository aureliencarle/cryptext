#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cryptext.session import SessionEnvironment
from cryptext.shell import Shell
from cryptext.command_register import Register
from cryptext.utils.arguments import parse_args


def main():

    args = parse_args()
    session = SessionEnvironment(args.session)

    if args.label:
        if args.label[0] in list(session.content.keys()):
            session.clipboard_copy(args.label[0])
        return

    Register.register(Shell, 'rw')
    shell = Shell(session)
    shell.cmdloop()


if __name__ == '__main__':
    main()
