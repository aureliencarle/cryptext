
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cmd
from pathlib import Path
#print(Path.home())

from src.session    import SessionEnvironment

from src.commands   import *

class Shell(cmd.Cmd):
    prompt  = ALINEA
    session = None
    
    def __init__(self, session) -> None:
        super().__init__()
        self.session    =  session
        self.prompt     = self.session.prompt
        self.session.log()
    
    # Needed to not repeat the last sucess command if you spam retrun ;)
    def emptyline(self):
        pass
    
    def do_test(self, line):
        list_param = line.split()
        print(list_param)

    def do_exit(self, line):
        print('You\'re quitting cryptext')
        exit()

    def add_command(self, Command):
        try :
            setattr(Shell, 'do_'+Command.name, Command.do_cmd)
            setattr(Shell, 'complete_'+Command.name, Command.complete_cmd)
            setattr(Shell, 'help_'+Command.name, Command.help_cmd)
        except:
            pass
        

if __name__ == '__main__': 

    session = SessionEnvironment()
    shell = Shell(session)
    shell.add_command(Show)
    shell.add_command(Ls)
    shell.add_command(Add)
    shell.add_command(Session)
    shell.cmdloop()
