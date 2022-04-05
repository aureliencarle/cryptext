#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.password   import Password
from getpass        import getpass
from src.utils      import *

def get_arguments(line):
    arguments = {}
    all_parameters = line.split()
    arguments.update({'parameter' : all_parameters[0]})
    options = []
    for p in all_parameters[1:]:
        if p.startswith('-') or  p.startswith('--'):
            options.append(p)
    arguments.update({'options' : options})
    return arguments

class Command():

    def do_cmd(self, line):
        pass
    def complete_cmd(self, text, line, begidx, endidx):
        pass
    def help_cmd(self):
        print('no help yet')


class Show(Command):
    name = 'show'

    def do_cmd(self, line):
        secure  = True
        arguments = get_arguments(line)
                
        if '--no-secure' in arguments['options']:
            secure = False
                        
        if arguments['parameter'] in self.session.content.keys():
            self.session.content[arguments['parameter']].show(secure)

    def complete_cmd(self, text, line, begidx, endidx):
        if not text:
            completions = [k for k in self.session.content.keys()] 
        else:
            completions = [k
                           for k in self.session.content.keys()
                           if k.startswith(text)
                          ]
        return completions
    
    def help_cmd(self):
        print('help :: show <label> [--no-secure]')

class Ls(Command):
    name = 'ls'
    
    def do_cmd(self, line):
        #for k in self.session.content.keys():
        #    print('    '+k)
        label_list = list(self.session.content.keys()) 
        label_list.sort()
        col_print(label_list)

class Add(Command):
    name = 'add'
    
    def do_cmd(self, line):
        password = Password()
        password.lab = get_entry('label','  ')
        password.url = get_entry('url','    ')
        password.com = get_entry('comment', '')        
        
        tentative = 2
        while tentative != -1:
            pas = getpass('pass    : ')
            cof = getpass('confirm : ')
            if (pas == cof):
                password.has = pas
                password.convert(self.session.generate_path(), self.session.key)
                break
            else:
                if tentative == 0:
                    print('code not added !')
                    break
                else:
                    print('!!! password do not match !!! left '+str(tentative)+' try')
                tentative -= 1
        del password
        self.session.recover(Password)


class Session:
    name = 'session'
    
    def do_cmd(self, line):
        arguments = get_arguments(line)
        
        if arguments['parameter'] == 'switch':
            col_print(self.session.all_sec)