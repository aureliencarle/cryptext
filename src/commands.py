#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cmd
import os            

from src.password   import Password
from getpass        import getpass
from src.utils      import *


class Shell(cmd.Cmd):
    prompt  = ALINEA
    session = None
    
    def __init__(self, session) -> None:
        super().__init__()
        self.session    = session
        self.prompt     = self.session.prompt


    def get_arguments(self, line):
        arguments = {}
        all_parameters = line.split()
        arguments.update({'parameter' : all_parameters[0]})
        options = []
        for p in all_parameters[1:]:
            if p.startswith('-') or  p.startswith('--'):
                options.append(p)
        arguments.update({'options' : options})
        return arguments

    # Needed to not repeat the last sucess command if you spam retrun ;)
    def emptyline(self):
        pass

################################################################################
## LS COMMAND

    def do_ls(self, line):
        if self.session.name is not None:
            label_list = list(self.session.content.keys()) 
            label_list.sort()
            Utils.col_print(label_list)
        else:
            Utils.col_print(self.session.files)

################################################################################
## SHOW COMMAND

    def do_show(self, line):
        try:
            secure = True
            arguments = self.get_arguments(line)

            if '--no-secure' in arguments['options']:
                secure = False
                            
            if arguments['parameter'] in self.session.content.keys():
                self.session.content[arguments['parameter']].show(secure)
        
        except:
            Utils.print('error with command see usage below :')
            self.help_show()


    def complete_show(self, text, line, begidx, endidx):
        if not text:
            completions = [k for k in self.session.content.keys()] 
        else:
            completions = [k
                           for k in self.session.content.keys()
                           if k.startswith(text)
                          ]
        return completions
    
    def help_show(self):
        Utils.print('help :: show <label> [--no-secure]')
        
        
################################################################################
## ADD COMMAND

    def do_add(self, line):
        if self.session.name is not None:
            password = Password()
            password.lab = get_entry('label','  ')
            password.url = get_entry('url','    ')
            password.com = get_entry('comment', '')        
            password.usr = get_entry('usr', '    ')                
            tentative = 2
            while tentative != -1:
                pas = getpass(' '*INDENT+'pass    : ')
                cof = getpass(' '*INDENT+'confirm : ')
                if (pas == cof):
                    password.has = pas
                    password.convert(self.session.generate_path(), self.session.key)
                    break
                else:
                    if tentative == 0:
                        Utils.print('code not added !')
                        break
                    else:
                        Utils.print('!!! password do not match !!! left '+str(tentative)+' try')
                    tentative -= 1
            del password
            self.session.recover(Password)
        else:
            self.help_add()
        
    def help_add(self):
        Utils.print('you need a session to add a pass')

################################################################################
## START COMMAND

    def do_start(self, line):
        if line != '':
            arguments = self.get_arguments(line)
            if self.session.start(arguments['parameter']):
                self.prompt = self.session.prompt
            else:
                self.help_start()
        else:
            self.help_start()
        
    def complete_start(self, text, line, begidx, endidx):    
        if not text:
            completions = [k for k in self.session.files] 
        else:
            completions = [k
                            for k in self.session.files
                            if k.startswith(text)
                            ]
        return completions
      
    def help_start(self):
        self.session.log()
          
################################################################################
## CREATE COMMAND 
         
    def do_create(self, line):
        arguments = self.get_arguments(line)
        
        self.session.create(arguments['parameter'])

        
        
################################################################################

    def do_test(self, line):
        list_param = line.split()
        Utils.print(list_param)

    def do_exit(self, line):
        Utils.print('You\'re quitting cryptext')
        exit()
