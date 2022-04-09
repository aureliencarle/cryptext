#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from colorama import Fore

from src.utils import Geometry, Io, Crypt


@dataclass
class Password:
    lab: str
    url: str
    com: str
    usr: str
    has: str

    def show(self, is_secure=True) -> None:
        Io.print(self.lab)
        if self.url:
            Io.print(Io.colored('url     ', self.url, Fore.MAGENTA))
        if self.com:
            Io.print(Io.colored('comment ', self.com, Fore.YELLOW))
        if self.usr:
            Io.print(Io.colored('usr     ', self.usr, Fore.CYAN))
        if is_secure:
            blind = Io.input(Io.colored('pass    ', self.has, Fore.RED))
            Io.delete_line()
            Io.print('--- Mischief Managed! ---')
        else:
            Io.print(Io.colored('pass    ', self.has, Fore.RED))

    def convert(self, name, key):
        if self.has is None:
            Io.print('No password, no save')
            return
        compact = ''.join(
            [
                self.lab,
                Geometry.MARK,
                self.url,
                Geometry.MARK,
                self.com,
                Geometry.MARK,
                self.usr,
                Geometry.MARK,
                self.has,
            ]
        )
        Crypt.write(name, key, compact)
