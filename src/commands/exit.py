from src.shell import Shell
from src.utils import Utils

class Exit:

    @staticmethod
    def do(shell: Shell, line: str):
        Utils.print('You\'re quitting cryptext')
        shell.exit(0)

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        pass

    @staticmethod
    def help(shell: Shell):
        pass
