#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from colorama import Fore
from src.utils import Geometry, Io, Crypt

class Password():
    lab = None
    url = None
    com = None
    usr = None
    has = None

    def __init__(self, info=None):
        if info:
            self.lab = info[0]
            self.url = info[1]
            self.com = info[2]
            self.usr = info[3]
            self.has = info[4]
        else:
            pass

    def show(self, is_secure=True) -> None:
        Io.print(self.lab)
        if self.url:
            Io.print(Io.colored('url     ', self.url, Fore.MAGENTA))
        if self.com:
            Io.print(Io.colored('comment ', self.com, Fore.YELLOW))
        if self.usr:
            Io.print(Io.colored('usr     ', self.usr, Fore.CYAN))
        if is_secure:
            blind = Io.input(Io.colored('pass    ',self.has, Fore.RED))
            Io.print(Io.deline('--- Mischief Managed! ---'))
        else:
            Io.print(Io.colored('pass    ', self.has, Fore.RED))

    def convert(self, name, key):
        if self.has is None:
            Io.print('No password, no save')
            return
        compact = ''.join([
            self.lab,
            Geometry.MARK,
            self.url,
            Geometry.MARK,
            self.com,
            Geometry.MARK,
            self.usr,
            Geometry.MARK,
            self.has
        ])
        Crypt.write(name, key, compact)
