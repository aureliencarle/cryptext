"""Layout configurations for cryptext."""

from dataclasses import dataclass
from enum import Enum


@dataclass
class LayoutConfig:
    """Define a layout configuration for cryptext."""

    prompt: str = 'cryptext > '
    indent_size: int = 4

    def get_indent(self) -> str:
        """Return the indent for the layout config."""
        return ' ' * self.indent_size


class CryptextLayouts(Enum):
    """Built-in cryptext layouts."""

    DEFAULT: LayoutConfig = LayoutConfig()
