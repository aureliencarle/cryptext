#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cryptext.session import SessionEnvironment
from cryptext.shell import Shell
from cryptext.command_register import Register
from cryptext.utils.arguments import arguments


def main():

    args = arguments()
    session = SessionEnvironment(args.session)

    if all(arg is None for arg in args.__dict__.values()):
        Register.register(Shell, 'rw')
        shell = Shell(session)
        shell.cmdloop()
    else:
        if args.label[0] in list(session.content.keys()):
            session.print_content(args.label[0], True)
        else:
            print('obviously need to be changed but it\'s a draft')


if __name__ == '__main__':
    main()
