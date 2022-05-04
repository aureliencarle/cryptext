"""ThemeItem class, Theme class and built-in themes for cryptext."""


from dataclasses import dataclass
from enum import Enum


@dataclass
class ThemeItem:
    """Contain color and format for a cryptext item."""

    color: str = 'default'
    format: str = 'default'


@dataclass
class Theme:
    """Theme for terminal display in cryptext."""

    text: ThemeItem  # Applies to all text displayed (can be overriden)
    prompt: ThemeItem  # Applies to the prompt (e.g. cryptext > )
    user_input: ThemeItem  # Applies to user inputs
    session_name: ThemeItem  # Applies to the current session name
    dir_name: ThemeItem  # Applies to directory names (ls)
    file_name: ThemeItem  # Applies to file names (ls)


class CryptextThemes(Enum):
    """Built-in themes for cryptext."""

    DEFAULT: Theme = Theme(
        text=ThemeItem(),
        prompt=ThemeItem(),
        user_input=ThemeItem(),
        session_name=ThemeItem(color='cyan', format='bold'),
        dir_name=ThemeItem(color='blue', format='bold'),
        file_name=ThemeItem(color='yellow'),
    )
