from src.shell import Shell
from src.cryptext_io import Io

class Ls:

    @staticmethod
    def do(shell: Shell, line: str):
        if shell.session.name is None:
            Io.col_print(shell.session.files)
            return
        label_list = list(shell.session.content.keys())
        label_list.sort()
        Io.col_print(label_list)

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        pass

    @staticmethod
    def help(shell: Shell):
        pass