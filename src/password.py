#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from colorama import Fore

from src.utils import Geometry, Crypt
from src.utils.io import Io, Format


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
            Io.print('url     ', end='')
            Io.print(Format.colored(self.url, 'magenta'))
        if self.com:
            Io.print('comment ', end='')
            Io.print(Format.colored(self.com, 'yellow'))
        if self.usr:
            Io.print('usr     ', end='')
            Io.print(Format.colored(self.com, 'cyan'))
        if is_secure:
            Io.print('pass    ', end='')
            Io.print(Format.colored(self.has, 'red'))
            Io.input()
            Io.delete_line()
            Io.print('--- Mischief Managed! ---')
        else:
            Io.print('pass    ', end='')
            Io.print(Format.colored(self.has, 'red'))

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
