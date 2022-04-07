from src.shell import Shell
from src.utils import Utils

class Show:

    @staticmethod
    def do(shell: Shell, line: str):
        try:
            secure = True
            arguments = shell.get_arguments(line)

            if '--no-secure' in arguments['options']:
                secure = False

            if arguments['parameter'] in shell.session.content.keys():
                shell.session.content[arguments['parameter']].show(secure)

        except:
            Utils.print('error with command see usage below :')
            shell.help_show()

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        if not text:
            completions = [k for k in shell.session.content.keys()]
        else:
            completions = [k
                           for k in shell.session.content.keys()
                           if k.startswith(text)
                          ]
        return completions

    @staticmethod
    def help(shell: Shell):
        Utils.print('help :: show <label> [--no-secure]')
