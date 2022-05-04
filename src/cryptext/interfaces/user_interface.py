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
    get_final_theme_item,
)


@dataclass
class UserInterface:
    """Interact with the user through the terminal."""

    layout_config: LayoutConfig = CryptextLayouts.DEFAULT.value
    theme: Theme = CryptextThemes.DEFAULT.value

    def get_prompt(self, session: Optional[str] = None) -> str:
        """Return the prompt after applying the theme"""
        prompt = ''
        if session:
            prompt = ''.join(
                [
                    UserInterface.apply_theme_item('(', item=self.theme.text),
                    UserInterface.apply_theme_item(
                        session,
                        item=get_final_theme_item(
                            [self.theme.text, self.theme.session_name]
                        ),
                    ),
                    UserInterface.apply_theme_item(') ', item=self.theme.text),
                ]
            )
        return prompt + UserInterface.apply_theme_item(
            self.layout_config.prompt,
            item=get_final_theme_item([self.theme.text, self.theme.prompt]),
        )

    def __enter__(self) -> UserInterface:
        """Enter a new context: do nothing."""
        return self

    def __exit__(self, *args) -> None:
        """Exit a context, reset the format to user input."""
        self.set_user_mode()

    def set_user_mode(self) -> None:
        """Reset the format and set it to the user input format."""
        UserInterface.reset_format(item=self.theme.user_input)

    @staticmethod
    def reset_format(item: ThemeItem) -> None:
        UserInterface.print_with_format('', item=item)

    @staticmethod
    def apply_theme_item(text: str, item: ThemeItem) -> str:
        """Apply a theme-defined format to a string."""
        return Format.styled(text=text, color=item.color, style=item.style)

    @staticmethod
    def print_with_format(text: str, item: ThemeItem) -> None:
        formatted_text = UserInterface.apply_theme_item(text, item)
        TerminalInterface.print(formatted_text, end='')

    @staticmethod
    def new_line() -> None:
        TerminalInterface.print('')
