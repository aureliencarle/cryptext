from src.shell import Shell
from src.utils import Utils

class Create:

    @staticmethod
    def do(shell: Shell, line: str):
        arguments = shell.get_arguments(line)
        shell.session.create(arguments['parameter'])

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        pass

    @staticmethod
    def help(shell: Shell):
        pass
