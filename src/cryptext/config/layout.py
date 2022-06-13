"""Layout configurations for cryptext."""

from dataclasses import dataclass, field
from enum import Enum


@dataclass(frozen=True)
class LayoutConfig:
    """Define a layout configuration for cryptext."""

    prompt: str
    indent_size: int
    _indent: str = field(init=False, repr=False, default='')

    def __post_init__(self) -> None:
        """Initialize the string indent from the indent size."""
        object.__setattr__(self, '_indent', self.indent_size * ' ')

    @property
    def indent(self) -> str:
        """Return the indent for the layout config."""
        return self._indent


class CryptextLayouts(Enum):
    """Built-in cryptext layouts."""

    DEFAULT: LayoutConfig = LayoutConfig('cryptext > ', indent_size=4)
