from src.shell import Shell
from src.utils import Crypt

from src.cryptext_io import Geometry, Io

from src.password import Password
from getpass import getpass

class Add:

    @staticmethod
    def do(shell: Shell, line: str):
        if shell.session.name is None:
            Add.help(shell)
            return
        password = Password()
        password.lab = Crypt.get_entry('label','  ')
        password.url = Crypt.get_entry('url','    ')
        password.com = Crypt.get_entry('comment', '')
        password.usr = Crypt.get_entry('usr', '    ')
        tentative = 2
        while tentative != -1:
            pas = getpass(' '*Geometry.INDENT+'pass    : ')
            cof = getpass(' '*Geometry.INDENT+'confirm : ')
            if (pas == cof):
                password.has = pas
                password.convert(shell.session.generate_path(), shell.session.key)
                break
            else:
                if tentative == 0:
                    Io.print('code not added !')
                    break
                else:
                    Io.print('!!! password do not match !!! left '+str(tentative)+' try')
                tentative -= 1
        del password
        shell.session.recover(Password)

    @staticmethod
    def complete(shell: Shell, text: str, line: str, begidx: str, endidx: str):
        pass

    @staticmethod
    def help(shell: Shell):
        Io.print('you need a session to add a pass')
