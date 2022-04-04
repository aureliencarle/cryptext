#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.password   import Password
from src.session    import Session
from getpass        import getpass
from src.utils      import *

def build_options_list(line):
    results = []
    all_parameters = line.split()   
    for p in all_parameters:
        if p.startswith('-') or  p.startswith('--'):
            results.append(p)
    return results 

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
        label  = None
        secure = True
        list_params = line.split()
        label = list_params[0]
        
        options = build_options_list(line)
        if '--no-secure' in options:
            secure = False
                        
        if label in self.session.content.keys():
            self.session.content[label].show(secure)

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
