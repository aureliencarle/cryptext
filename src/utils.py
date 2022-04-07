#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64, hashlib
from cryptography.fernet    import Fernet
from colorama               import Fore

class Geometry:
    MARK      = '#netrisca#?!?#acsirten#'
    ALINEA    = 'cryptext > '
    INDENT    = 4


class Crypt:
    def generate_hash_key(clear_pass):
        encoded_pass = clear_pass.encode("utf-8")
        hash_key     = hashlib.md5(encoded_pass).hexdigest()
        return base64.urlsafe_b64encode(hash_key.encode("utf-8"))

    def crypt(key, clear_text):
        fernet = Fernet(key)
        encrypted = fernet.encrypt(clear_text.encode("utf-8"))
        return encrypted

    def decrypt(key, encoded_text):
        fernet = Fernet(key)
        clear_text = fernet.decrypt(encoded_text)
        return clear_text.decode("utf-8")

    def read(name):
        with open(name, 'rb') as encrypted_file:
            text = encrypted_file.read()
            return text.split()


    def write(name, key, text):
        with open(name, 'ab') as encrypted_file:
            encrypted_file.write('\n'.encode('utf-8'))
            encrypted_file.write(crypt(key, text))


    def get_entry(input_text, space, default_text='none'):
        result = Utils.input('['+input_text+']'+space+' -> ') or default_text
        return result


class Utils:

    def deline(text):
        return '\033[1A'+text+'\033[K'

    def colored(intro, text, color):
        return intro+color+text+Fore.RESET

    def print(text = '', indent=INDENT):
        print(' '*indent+text)

    def input(text='', indent=INDENT):
        return input(' '*indent+text)

    def col_print(lines, term_width=80, indent=INDENT, pad=10):
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
