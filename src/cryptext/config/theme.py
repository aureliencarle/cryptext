"""ThemeItem class, Theme class and built-in themes for cryptext."""


from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class ThemeItem:
    """Contain color and format for a cryptext item."""

    color: Optional[str] = None
    style: Optional[str] = None


def get_final_theme_item(items: list[ThemeItem]) -> ThemeItem:
    """Stack them items and use the last non-default parameter."""
    final_item = ThemeItem()
    for item in items:
        final_item.color = final_item.color or item.color
        final_item.style = final_item.style or item.style
    return final_item


@dataclass
class Theme:
    """Theme for terminal display in cryptext."""

    base: ThemeItem  # Applies to all text displayed (can be overriden)
    info: ThemeItem  # Info from the application
    warning: ThemeItem  # Warning from the application
    error: ThemeItem  # Error from the application
    prompt: ThemeItem  # Applies to the prompt (e.g. cryptext > )
    user_input: ThemeItem  # Applies to user inputs
    session_name: ThemeItem  # Applies to the current session name
    dir_name: ThemeItem  # Applies to directory names (ls)
    file_name: ThemeItem  # Applies to file names (ls)

    def __getitem__(self, item: str) -> ThemeItem:
        """Return a theme item applying the base item first."""
        return get_final_theme_item([self.base, getattr(self, item)])


class CryptextThemes(Enum):
    """Built-in themes for cryptext."""

    DEFAULT: Theme = Theme(
        base=ThemeItem(),
        info=ThemeItem(),
        warning=ThemeItem(color='red'),
        error=ThemeItem(color='red', style='bright'),
        prompt=ThemeItem(),
        user_input=ThemeItem(),
        session_name=ThemeItem(color='cyan', style='bright'),
        dir_name=ThemeItem(color='blue', style='bright'),
        file_name=ThemeItem(color='yellow'),
    )
