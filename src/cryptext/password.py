#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from getpass import getpass
from dataclasses import dataclass
from typing import List, Optional, Tuple

from .utils import DisplayConfig, Crypt, Io, Format


@dataclass
class PasswordData:
    label: str = 'nyancat'
    url: str = 'https://www.nyan.cat/'
    com: str = 'sorry for this'
    user: str = 'captain madness'
    passwd: str = '1234'


class PasswordDataIO:
    @staticmethod
    def summary(pass_data: PasswordData) -> None:
        """Print the data's summary"""
        PasswordDataIO.print_attributes(
            title=pass_data.label,
            attrs=[
                (pass_data.url, 'url', 'magenta'),
                (pass_data.user, 'user', 'cyan'),
            ],
        )

    @staticmethod
    def print(pass_data: PasswordData, is_secure: bool) -> None:
        """Print the password's data"""
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
    def convert(pass_data: PasswordData) -> List:
        if pass_data.passwd is None:
            PasswordDataIO.print_no_password_message()
            return
        compact = DisplayConfig.SEPARATOR.join(
            [
                pass_data.label,
                pass_data.url,
                pass_data.com,
                pass_data.user,
                pass_data.passwd,
            ]
        )
        return compact

    def write(name: str, key: str, compact: List) -> None:
        Crypt.write(name, key, compact)

    @staticmethod
    def secure_line(final_message: str) -> None:
        """Delete the password line after an input"""
        Io.input(silent=True)
        Io.delete_line()
        Io.print(final_message)

    @staticmethod
    def print_attributes(
        title: str, attrs: List[Tuple[str, str, str]]
    ) -> None:
        """Print a list of password attributes"""
        attrs, names, colors = list(zip(*attrs))
        equalized_names = Format.equalize_rows(names, ' : ')
        Io.print(title)
        for attr, name, color in zip(attrs, equalized_names, colors):
            PasswordDataIO.print_attribute(
                init_text=name, attr=attr, color=color
            )

    @staticmethod
    def print_attribute(init_text: str, attr: str, color: str) -> None:
        """Print one password attribute"""
        if attr:
            Io.print(init_text, end='')
            Io.print(Format.styled(text=attr, color=color), indent=0)

    @staticmethod
    def print_no_password_message() -> None:
        """Print a message when no password can be created"""
        Io.print('No password, no save')

    @staticmethod
    def input(label: str) -> PasswordData:
        """Input a PasswordData object"""
        Io.print(f'Creating password: {label!r}')
        url, com, user = PasswordDataIO.input_attributes(
            ['url', 'comment', 'user']
        )
        passwd = PasswordDataIO.input_password(confirm=True)
        return PasswordData(
            label=label, url=url, com=com, user=user, passwd=passwd
        )

    @staticmethod
    def input_attributes(prompts: List[str]) -> List[str]:
        """Input the attributes of PasswordData except the password"""
        equalized_prompts = Format.equalize_rows(prompts, ' : ')
        return [Io.input(prompt) for prompt in equalized_prompts]

    @staticmethod
    def input_password(
        confirm: bool = False,
        prompt: str = '[passphrase]',
        confirm_prompt: str = '[confirm]',
        right_token: str = ' > ',
    ) -> Optional[str]:
        """Input a password"""
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
    def _ask(
        input_text: str, confirm_text: Optional[str] = None, n_trials=2
    ) -> Optional[str]:
        """Internal function to input a password"""
        if confirm_text is not None:
            return PasswordDataIO._confirmation_ask(
                input_text=input_text,
                confirm_text=confirm_text,
                n_trials=n_trials,
            )
        else:
            return getpass(input_text)

    @staticmethod
    def _confirmation_ask(input_text, confirm_text, n_trials) -> Optional[str]:
        """Internal function to input a password with confirmation"""
        if n_trials <= 0:
            Io.print('code not added !')
            return None
        pas = getpass(' ' * DisplayConfig.INDENT + input_text)
        cof = getpass(' ' * DisplayConfig.INDENT + confirm_text)
        if pas == cof:
            return pas
        else:
            Io.print(f'!!! password do not match !!! left {n_trials-1} try')
            return PasswordDataIO._confirmation_ask(
                input_text=input_text,
                confirm_text=confirm_text,
                n_trials=n_trials - 1,
            )
