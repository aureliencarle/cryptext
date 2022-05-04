#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List
from colorama import Fore, Style


class DisplayConfig:
    SEPARATOR: str = '#netrisca#?!?#acsirten#'
    PROMPT: str = 'cryptext > '
    INDENT: int = 4


class Format:
    @staticmethod
    def styled(text: str, color: str, style: str = 'normal') -> str:
        """Apply color special characters to a string"""
        color_str = getattr(Fore, color.upper())
        style_str = getattr(Style, style.upper())
        reset_str = Style.RESET_ALL
        return f'{color_str}{style_str}{text}{reset_str}'

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
        indent: int = DisplayConfig.INDENT,
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
        text: str = '', indent: str = DisplayConfig.INDENT, **kwargs
    ) -> None:
        """Print a text in the standard output"""
        TerminalInterface._print(' ' * indent + text, **kwargs)

    @staticmethod
    def input(
        text: str = '',
        indent: str = DisplayConfig.INDENT,
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
    def ask_user_confirmation(prompt: str, default_str: str):
        """Ask a confirmation to the user and return the answer"""
        default_str = default_str.lower()
        if default_str not in 'yn':
            raise (NameError("Default string should be 'y' or 'n'."))
        answer = (
            TerminalInterface.input(f'{prompt} [y/n, default={default_str}] ')
            or default_str
        )
        return 'y' == answer.lower()

    @staticmethod
    def _print(*args, **kwargs):
        """Print function that should be used internally in the Io class"""
        print(*args, **kwargs)

    @staticmethod
    def _input(*args, **kwargs):
        """Input function that should be used internally in the Io class"""
        return input(*args, **kwargs)
