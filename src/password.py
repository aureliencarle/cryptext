#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.utils  import *

class Password():
    lab = None
    url = None
    com = None
    usr = None
    has = None
    
    def __init__(self, info=None):
        if info:
            self.lab = info[0]
            self.url = info[1]
            self.com = info[2]
            self.usr = None
            self.has = info[3]
        else:
            pass
        
    def show(self, is_secure=True) -> None:
        print(self.lab)
        if self.url:
            print(colored('url     ', self.url, Fore.MAGENTA))
        if self.com:
            print(colored('comment ', self.com, Fore.YELLOW))
        if is_secure:
            blind = input(colored('pass    ',self.has, Fore.RED))
            print(deline('--- Mischief Managed! ---'))
        else:
            print(colored('pass    ', self.has, Fore.RED))

    def convert(self, name, key):
        compact = self.lab+MARK+self.url+MARK+self.com+MARK+self.has
        write(name, key, compact)
    
