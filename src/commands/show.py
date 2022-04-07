from src.shell import Shell
from src.utils import Utils

class Show:

    @staticmethod
    def do(shell: Shell, line: str):
        try:
            secure = '--no-secure' not in arguments['options']
            arguments = shell.get_arguments(line)

            if arguments['parameter'] in shell.session.content.keys():
                shell.session.content[arguments['parameter']].show(secure)

        except ExceptionType:
            Utils.print('error with command see usage below :')
            Show.help(shell)

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        return [
            k for k in shell.session.content.keys()
            if not text or k.startswith(text)
        ]

    @staticmethod
    def help(shell: Shell):
        Utils.print('help :: show <label> [--no-secure]')
