#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ast import Pass
from dataclasses import dataclass
from colorama import Fore

from src.utils import Geometry, Crypt
from src.utils.io import Io, Format


@dataclass
class PasswordData:
    lab: str
    url: str
    com: str
    usr: str
    passwd: str

    def show(self, is_secure: bool = True) -> None:
        PasswordDataRenderer.show(self, is_secure=is_secure)

    def convert(self, name: str, key) -> None:
        if self.passwd is None:
            PasswordDataRenderer.no_password_message()
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
                self.passwd,
            ]
        )
        Crypt.write(name, key, compact)


class PasswordDataRenderer:
    @staticmethod
    def show(pass_data: PasswordData, is_secure: bool) -> None:
        Io.print(pass_data.lab)
        PasswordDataRenderer.show_attribute(
            init_text='url     ', attr=pass_data.url, color='magenta'
        )
        PasswordDataRenderer.show_attribute(
            init_text='comment ', attr=pass_data.com, color='yellow'
        )
        PasswordDataRenderer.show_attribute(
            init_text='usr     ', attr=pass_data.usr, color='cyan'
        )
        PasswordDataRenderer.show_attribute(
            init_text='pass    ', attr=pass_data.passwd, color='red'
        )
        if is_secure:
            PasswordDataRenderer.secure_line('--- Mischief Managed! ---')

    @staticmethod
    def secure_line(final_message: str):
        Io.input(silent=True)
        Io.delete_line()
        Io.print(final_message)

    @staticmethod
    def show_attribute(init_text: str, attr: str, color: str):
        if attr:
            Io.print(init_text, end='')
            Io.print(Format.colored(text=attr, color=color))

    @staticmethod
    def no_password_message():
        Io.print('No password, no save')
