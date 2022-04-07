from src.shell import Shell
from src.utils import Utils

class Ls:

    @staticmethod
    def do(shell: Shell, line: str):
        if shell.session.name is not None:
            label_list = list(shell.session.content.keys())
            label_list.sort()
            Utils.col_print(label_list)
        else:
            Utils.col_print(shell.session.files)

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        print("Completing ls")

    @staticmethod
    def help(shell: Shell):
        print("RTFM ls")
