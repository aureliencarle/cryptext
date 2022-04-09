#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ast import Pass
from getpass import getpass
from dataclasses import dataclass
from selectors import EpollSelector
from typing import List, Optional, Tuple

from click import confirm

from src.utils import Geometry, Crypt
from src.utils.io import Io, Format


@dataclass
class PasswordData:
    label: str
    url: str
    com: str
    user: str
    passwd: str

    def show(self, is_secure: bool = True) -> None:
        PasswordDataIO.print(self, is_secure=is_secure)

    def convert(self, name: str, key) -> None:
        if self.passwd is None:
            PasswordDataIO.print_no_password_message()
            return
        compact = ''.join(
            [
                self.label,
                Geometry.MARK,
                self.url,
                Geometry.MARK,
                self.com,
                Geometry.MARK,
                self.user,
                Geometry.MARK,
                self.passwd,
            ]
        )
        Crypt.write(name, key, compact)


class PasswordDataIO:
    @staticmethod
    def print(pass_data: PasswordData, is_secure: bool) -> None:
        PasswordDataIO.print_attributes(
            title=pass_data.label,
            attrs=[
                (pass_data.url, 'url', 'magenta'),
                (pass_data.com, 'comment', 'yellow'),
                (pass_data.user, 'user', 'cyan'),
                (pass_data.passwd, 'pass', 'red'),
            ],
        )
        if is_secure:
            PasswordDataIO.secure_line('--- Mischief Managed! ---')

    @staticmethod
    def secure_line(final_message: str):
        Io.input(silent=True)
        Io.delete_line()
        Io.print(final_message)

    @staticmethod
    def print_attributes(
        title: str, attrs: List[Tuple[str, str, str]]
    ) -> None:
        attrs, names, colors = list(zip(*attrs))
        equalized_names = Format.equalize_rows(names, ' : ')
        Io.print(title)
        for attr, name, color in zip(attrs, equalized_names, colors):
            PasswordDataIO.print_attribute(
                init_text=name, attr=attr, color=color
            )

    @staticmethod
    def print_attribute(init_text: str, attr: str, color: str):
        if attr:
            Io.print(init_text, end='')
            Io.print(Format.colored(text=attr, color=color), indent=0)

    @staticmethod
    def print_no_password_message():
        Io.print('No password, no save')

    @staticmethod
    def input() -> PasswordData:
        label, url, com, user = PasswordDataIO.input_attributes(
            ['label', 'url', 'comment', 'user']
        )
        passwd = PasswordDataIO.input_password(confirm=True)
        return PasswordData(
            label=label, url=url, com=com, user=user, passwd=passwd
        )

    @staticmethod
    def input_attributes(prompts: List[str]) -> List[str]:
        equalized_prompts = Format.equalize_rows(prompts, ' : ')
        return [Io.input(prompt) for prompt in equalized_prompts]

    @staticmethod
    def input_password(
        confirm: bool = False,
        prompt: str = '[passphrase]',
        confirm_prompt: str = '[confirm]',
        right_token: str = ' > ',
    ) -> str:
        if confirm:
            prompt, confirm_prompt = Format.equalize_rows(
                [prompt, confirm_prompt], right_str=right_token
            )
            return PasswordDataIO._ask(
                input_text=prompt, confirm_text=confirm_prompt
            )
        else:
            return PasswordDataIO._ask(prompt + right_token)

    @staticmethod
    def _ask(input_text: str, confirm_text: Optional[str] = None, n_trials=2):
        if confirm_text is not None:
            return PasswordDataIO._confirmation_ask(
                input_text=input_text,
                confirm_text=confirm_text,
                n_trials=n_trials,
            )
        else:
            return getpass(input_text)

    @staticmethod
    def _confirmation_ask(input_text, confirm_text, n_trials):
        if n_trials <= 0:
            Io.print('code not added !')
            return None
        pas = getpass(' ' * Geometry.INDENT + input_text)
        cof = getpass(' ' * Geometry.INDENT + confirm_text)
        if pas == cof:
            return pas
        else:
            Io.print(f'!!! password do not match !!! left {n_trials-1} try')
            return PasswordDataIO._confirmation_ask(
                input_text=input_text,
                confirm_text=confirm_text,
                n_trials=n_trials - 1,
            )
