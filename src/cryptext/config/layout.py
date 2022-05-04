"""Layout configurations for cryptext."""

from dataclasses import dataclass
from enum import Enum


@dataclass
class LayoutConfig:
    """Define a layout configuration for cryptext."""

    separator: str = '#netrisca#?!?#acsirten#'
    prompt: str = 'cryptext > '
    indent_size: int = 4


class CryptextLayouts(Enum):
    """Built-in cryptext layouts."""

    DEFAULT: LayoutConfig = LayoutConfig()
