#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from colorama import Fore

class Geometry:
    MARK      = '#netrisca#?!?#acsirten#'
    ALINEA    = 'cryptext > '
    INDENT    = 4

class Io:

    def deline(text):
        return '\033[1A'+text+'\033[K'

    def colored(intro, text, color):
        return intro+color+text+Fore.RESET

    def print(text = '', indent=Geometry.INDENT):
        print(' '*indent+text)

    def input(text='', indent=Geometry.INDENT):
        return input(' '*indent+text)

    def col_print(lines, term_width=80, indent=Geometry.INDENT, pad=10):
        n_lines = len(lines)
        if n_lines == 0:
            return

        col_width = max(len(line) for line in lines)
        n_cols = int((term_width + pad - indent)/(col_width + pad))
        n_cols = min(n_lines, max(1, n_cols))

        col_len = int(n_lines/n_cols) + (0 if n_lines % n_cols == 0 else 1)
        if (n_cols - 1) * col_len >= n_lines:
            n_cols -= 1

        cols = [lines[i*col_len : i*col_len + col_len] for i in range(n_cols)]

        rows = list(zip(*cols))
        rows_missed = zip(*[col[len(rows):] for col in cols[:-1]])
        rows.extend(rows_missed)

        for row in rows:
            print(" "*indent + (" "*pad).join(line.ljust(col_width) for line in row))
