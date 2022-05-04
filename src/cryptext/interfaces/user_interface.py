"""User interface of cryptext."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

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

    def print(self, text: str) -> None:
        """Print text in the terminal using the base style."""
        UserInterface.print_with_format(text=text, item=self.theme['base'])

    def info(self, text: str) -> None:
        """Print an info in the terminal."""
        UserInterface.print_with_format(text=text, item=self.theme['info'])

    def warning(self, text: str) -> None:
        """Print a warning in the terminal."""
        UserInterface.print_with_format(
            text=f'Warning: {text}', item=self.theme['warning']
        )

    def error(self, text: str) -> None:
        """Print an error in the terminal."""
        UserInterface.print_with_format(
            text=f'Error: {text}', item=self.theme['error']
        )

    def get_prompt(self, session: Optional[str] = None) -> str:
        """Return the prompt after applying the theme"""
        session_prompt = ''
        if session:
            session_prompt = ''.join(
                [
                    UserInterface.apply_theme_item(
                        '(', item=self.theme['base']
                    ),
                    UserInterface.apply_theme_item(
                        session, item=self.theme['session_name']
                    ),
                    UserInterface.apply_theme_item(
                        ') ', item=self.theme['base']
                    ),
                ]
            )
        default_prompt = UserInterface.apply_theme_item(
            self.layout_config.prompt, item=self.theme['prompt'],
        )
        user_style = self.get_user_mode()
        return session_prompt + default_prompt + user_style

    def ask_user_confirmation(self, prompt: str, default_str: str) -> bool:
        """Ask a confirmation to the user and return the answer"""
        default_str = default_str.lower()
        if default_str not in 'yn':
            raise NameError("Default string should be 'y' or 'n'.")
        prompt = UserInterface.apply_theme_item(
            f'{prompt} [y/n, default={default_str}] ', item=self.theme['base']
        )
        answer = TerminalInterface.input(prompt) or default_str
        return 'y' == answer.lower()

    def get_user_mode(self) -> str:
        """Reset the format and set it to the user input format."""
        item = self.theme['user_input']
        return Format.get_style(color=item.color, style=item.style)

    @staticmethod
    def apply_theme_item(text: str, item: ThemeItem) -> str:
        """Apply a theme-defined format to a string."""
        return Format.styled(text=text, color=item.color, style=item.style)

    @staticmethod
    def print_with_format(text: str, item: ThemeItem) -> None:
        formatted_text = UserInterface.apply_theme_item(text, item)
        TerminalInterface.print(formatted_text)
