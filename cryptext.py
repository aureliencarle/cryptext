
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cmd
import os
import getpass
from pathlib import Path
#print(Path.home())

from password import Password, Session

ALINEA = ' (amnesia)> '

CODE_LIST = [
    'clap',
    'nop',
    'asdf',
    'zxc',
    'wer',
    'fewq',
    're',
    'qwe'
]

session = Session()

class Search(cmd.Cmd):
    name = 'search'

    def do_cmd(self, line):
        print(line)

    def complete_cmd(self, text, line, begidx, endidx):
        if not text:
            completions = session.content[0]
        else:
            completions = [ f
                            for f in session.content[0]
                            if f.startswith(text)
                            ]
        return completions

class Ls(cmd.Cmd):
    name = 'ls'
    
    def do_cmd(self, line):
        for c in session.content:
            print(c.lab)



def deline(text):
    return '\033[1A'+text+'\033[K'

def get_entry(input_text, space, default_text=''):
    result = input(' ['+input_text+']'+space+' -> ') or default_text
    return result

class Shell(cmd.Cmd):
    prompt = ALINEA
    command_list = ['exit']
    # Needed to not repeat the last sucess command if you spam retrun ;)
    def emptyline(self):
        pass

    def do_add_code(self, line):
        password = Password()
        password.lab = get_entry('label','  ')
        password.url = get_entry('url','    ')
        password.com = get_entry('comment', '')
        pas = getpass.getpass('pass    : ')
        cof = getpass.getpass('confirm : ')
        if (pas == cof):
            password.has = pas
            password.convert(session.generate_path(), session.key)
        else:
            print('!!! password do not match !!!')
        del password
    
    def do_recover(self, line):
            session.recover(session.key)
    
    def do_pass(self, line):
        mdp = '*********'
        blind = input(mdp+' [press key to hide password]')
        print(deline('hidden'))

    def do_exit(self, line):
        print('You\'re quitting cryptext')
        exit()


    def add_command(self, Command):
        self.command_list.append(Command.name)
        try :
            setattr(Shell, 'do_'+Command.name, Command.do_cmd)
            setattr(Shell, 'complete_'+Command.name, Command.complete_cmd)
        except:
            pass

if __name__ == '__main__': 
    
    shell = Shell()
    
    shell.add_command(Search)
    shell.add_command(Ls)
    print(shell.command_list)

    shell.cmdloop()
