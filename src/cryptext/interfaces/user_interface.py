"""User interface of cryptext."""

from __future__ import annotations
import copy

from dataclasses import dataclass
from getpass import getpass
from typing import Optional, Union

from ..io.terminal_io import TerminalInterface, Format
from ..config.layout import CryptextLayouts, LayoutConfig
from ..config.theme import (
    CryptextThemes,
    Theme,
    ThemeItem,
)


@dataclass
class UserInterface:
    """Interact with the user through the terminal."""

    layout_config: LayoutConfig = CryptextLayouts.DEFAULT.value
    theme: Theme = CryptextThemes.DEFAULT.value

    def print(self, text: str, **kwargs) -> None:
        """Print text in the terminal using the base style."""
        self.print_with_style(text=text, item=self.theme['base'], **kwargs)

    def print_with_style(
        self, text: Union[str, list[str]], item: ThemeItem, **kwargs
    ) -> None:
        """Print a string or list of strings applying a given style"""
        formatted_text = self.apply_theme_item(text, item)
        TerminalInterface.print(
            formatted_text, self.layout_config.indent, **kwargs
        )

    def info(self, text: str) -> None:
        """Print an info in the terminal."""
        self.print_with_style(text=text, item=self.theme['info'])

    def warning(self, text: str) -> None:
        """Print a warning in the terminal."""
        self.print_with_style(
            text=f'Warning: {text}', item=self.theme['warning']
        )

    def error(self, text: str) -> None:
        """Print an error in the terminal."""
        self.print_with_style(text=f'Error: {text}', item=self.theme['error'])

    def list_files(self, files: list[str]) -> None:
        """Print the list of files using the relevant theme."""
        self.print_with_style(files, self.theme['files'])

    def list_directories(self, directories: list[str]) -> None:
        """Print the list of directories using the relevant theme."""
        self.print_with_style(directories, self.theme['directories'])

    def get_prompt(self, session: Optional[str] = None) -> str:
        """Return the prompt after applying the theme"""
        session_prompt = ''
        if session:
            session_prompt = ''.join(
                [
                    self.apply_theme_item('(', item=self.theme['base']),
                    self.apply_theme_item(
                        session, item=self.theme['session_name']
                    ),
                    self.apply_theme_item(') ', item=self.theme['base']),
                ]
            )
        default_prompt = self.apply_theme_item(
            self.layout_config.prompt, item=self.theme['prompt'],
        )
        user_style = self.get_user_mode()
        return session_prompt + default_prompt + user_style

    def ask_user_confirmation(self, prompt: str, default_str: str) -> bool:
        """Ask a confirmation to the user and return the answer"""
        default_str = default_str.lower()
        if default_str not in 'yn':
            raise NameError("Default string should be 'y' or 'n'.")
        prompt = self.apply_theme_item(
            f'{prompt} [y/n, default={default_str}] ', item=self.theme['base']
        )
        answer = (
            TerminalInterface.input(prompt, self.layout_config.indent)
            or default_str
        )
        return 'y' == answer.lower()

    def input_attributes(self, prompts: list[str]) -> list[str]:
        """Input a list of attributes."""
        equalized_prompts = Format.equalize_rows(prompts, ' : ')
        formatted_prompts = [
            self.apply_theme_item(prompt, item=self.theme['base'])
            + self.get_user_mode()
            for prompt in equalized_prompts
        ]
        return [
            TerminalInterface.input(prompt, self.layout_config.indent)
            for prompt in formatted_prompts
        ]

    def print_attributes(self, title: str, attrs: list[tuple]) -> None:
        """Print a list of attributes in column."""
        attrs, names, colors = list(zip(*attrs))
        equalized_names = Format.equalize_rows(names, ' : ')
        TerminalInterface.print(title, indent=self.layout_config.indent)
        for attr, name, color in zip(attrs, equalized_names, colors):
            if not attr:
                continue
            self.print(name, end='')
            item = copy.copy(self.theme['base'])
            item.color = color
            self.print_with_style(attr, item=item)

    def secure_line(self, final_message: str) -> None:
        """Delete the password line after an input"""
        TerminalInterface.input(silent=True)
        self.print(final_message)

    def input_password(self, confirm: bool = True, n_trials: int = 3) -> str:
        """Input a password from the user."""
        if n_trials <= 0:
            self.error('No more trials for password input')
            return None
        pass_ = self._ask_password(self.layout_config.indent + 'password > ')
        if confirm:
            conf = self._ask_password(
                self.layout_config.indent + 'confirm  > '
            )
            if pass_ != conf:
                self.info(
                    f'!!! password do not match !!! left {n_trials-1} try'
                )
                return self.input_password(confirm, n_trials - 1)
        return pass_

    def _ask_password(self, input_text: str) -> str:
        """Internal function to input a password"""
        return getpass(input_text)

    def get_user_mode(self) -> str:
        """Reset the format and set it to the user input format."""
        item = self.theme['user_input']
        return Format.get_style(color=item.color, style=item.style)

    def apply_theme_item(
        self, text: Union[str, list[str]], item: ThemeItem
    ) -> str:
        """
        Apply a theme-defined format to a string or a string list (columns)
        """
        if isinstance(text, str):
            return Format.styled(text=text, color=item.color, style=item.style)
        else:
            return Format.pretty_columns(
                Format.styled_list(text, color=item.color, style=item.style),
                indent=self.layout_config.indent,
            )
