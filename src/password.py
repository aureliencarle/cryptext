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
            self.usr = info[3]
            self.has = info[4]
        else:
            pass
        
    def show(self, is_secure=True) -> None:
        Utils.print(self.lab)
        if self.url:
            Utils.print(Utils.colored('url     ', self.url, Fore.MAGENTA))
        if self.com:
            Utils.print(Utils.colored('comment ', self.com, Fore.YELLOW))
        if self.usr:
            Utils.print(Utils.colored('usr     ', self.usr, Fore.CYAN))
        if is_secure:
            blind = Utils.input(Utils.colored('pass    ',self.has, Fore.RED))
            Utils.print(Utils.deline('--- Mischief Managed! ---'))
        else:
            Utils.print(Utils.colored('pass    ', self.has, Fore.RED))

    def convert(self, name, key):
        compact = self.lab+MARK+self.url+MARK+self.com+MARK+self.usr+MARK+self.has
        write(name, key, compact)
    