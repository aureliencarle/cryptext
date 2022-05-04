#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional
from colorama import Fore, Style


class DisplayConfig:
    separator: str = '#netrisca#?!?#acsirten#'
    prompt: str = 'cryptext > '
    indent_size: int = 4


class InvalidColor(Exception):
    """Raised when an invalid color string is given to Format."""


class InvalidStyle(Exception):
    """Raised when an invalid style string is given to Format."""


class Format:
    @staticmethod
    def get_style(
        color: Optional[str] = None, style: Optional[str] = None
    ) -> str:
        """Return the string corresponding to a color and style."""
        try:
            color_str = getattr(Fore, color.upper()) if color else Fore.RESET
        except AttributeError as err:
            raise InvalidColor(f'Color {color!r} unknown') from err
        try:
            style_str = (
                getattr(Style, style.upper()) if style else Style.NORMAL
            )
        except AttributeError as err:
            raise InvalidStyle(f'Style {style!r} unknown') from err
        return color_str + style_str

    @staticmethod
    def styled(
        text: str, color: Optional[str] = None, style: Optional[str] = None
    ) -> str:
        """Apply color special characters to a string"""
        style = Format.get_style(color=color, style=style)
        reset = Format.get_style()
        return ''.join([style, text, reset])

    @staticmethod
    def styled_list(
        lines: List[str], color: str, style: str = 'normal'
    ) -> List[str]:
        """Apply color to list of string"""
        return [Format.styled(l, color, style) for l in lines]

    @staticmethod
    def equalize_rows(rows: List[str], right_str: str = '') -> List[str]:
        """Fill rows with space so that all have the same length"""
        max_row_size = max(len(row) for row in rows)
        return [row.ljust(max_row_size) + right_str for row in rows]

    @staticmethod
    def pretty_columns(
        lines: List[str],
        term_width: int = 80,
        indent: int = DisplayConfig.indent_size,
        pad: int = 5,
    ) -> str:
        """Generate a pretty string from a list of rows, aligning columns."""
        n_lines = len(lines)
        if n_lines == 0:
            return ''

        col_width = max(len(line) for line in lines)
        n_cols = int((term_width + pad - indent) / (col_width + pad))
        n_cols = min(n_lines, max(1, n_cols))

        col_len = int(n_lines / n_cols) + (0 if n_lines % n_cols == 0 else 1)
        if (n_cols - 1) * col_len >= n_lines:
            n_cols -= 1

        cols = [
            lines[i * col_len : i * col_len + col_len] for i in range(n_cols)
        ]

        rows = list(zip(*cols))
        rows_missed = zip(*[col[len(rows) :] for col in cols[:-1]])
        rows.extend(rows_missed)

        return '\n'.join(
            [
                ' ' * indent
                + (' ' * pad).join(line.ljust(col_width) for line in row)
                for row in rows
            ]
        )


class TerminalInterface:
    @staticmethod
    def print(
        text: str = '', indent: str = DisplayConfig.indent_size, **kwargs
    ) -> None:
        """Print a text in the standard output"""
        TerminalInterface._print(' ' * indent + text, **kwargs)

    @staticmethod
    def input(
        text: str = '',
        indent: str = DisplayConfig.indent_size,
        silent: bool = False,
    ) -> None:
        """Ask an input to the user"""
        res = TerminalInterface._input(' ' * indent + text)
        if silent:
            TerminalInterface.delete_line()
        return res

    @staticmethod
    def delete_line() -> None:
        """Delete the last line printed"""
        TerminalInterface._print('\033[A\033[K\033[A')

    @staticmethod
    def _print(*args, **kwargs):
        """Print function that should be used internally in the Io class"""
        print(*args, **kwargs)

    @staticmethod
    def _input(*args, **kwargs):
        """Input function that should be used internally in the Io class"""
        return input(*args, **kwargs)
