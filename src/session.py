#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from getpass import getpass
import os
from src.password import Password
from src.utils import *
from src.cryptpath import CRYPTPATH

from src.cryptext_io import Geometry, Io

class SessionEnvironment():
    name        = None
    files       = os.listdir(CRYPTPATH)
    prompt      = Geometry.ALINEA
    passpath    = CRYPTPATH
    key         = None
    content     = {}

    def start(self, session_name=None):
        if session_name != '':
            if session_name in self.files:
                self.name = session_name
            else:
                Io.print(' -- file not found --')
                creation = Io.input('Do you want to create it ? [yes] : ')
                if creation == 'yes':
                    self.create(session_name)
                    self.start(session_name)
                return False
            passwd = getpass('[passphrase] > ')
            try:
                self.update(passwd)
            except:
                self.name = None
                Io.print(' -- wrong file key --')
                return False
            return True
        else:
            Io.print('Nothing to start')
            return False

    def create(self, name):
        if not os.path.exists(self.passpath+'/'+name):
            with open(self.passpath+'/'+name, 'w'): pass
        else:
            Io.print('file already exist')
        self.files = os.listdir(CRYPTPATH)

    def update(self, password):
        self.prompt = '('+self.name+') '+Geometry.ALINEA
        self.key = self.get_key(password)
        self.recover()

    def get_key(self, password = 'as'):
        return Crypt.generate_hash_key(password)

    def generate_path(self):
        return self.passpath+'/'+self.name

    def recover(self, object=Password):
        self.content.clear()
        for l in Crypt.read(self.generate_path()):
            p = object(Crypt.decrypt(self.key,l).split(Geometry.MARK))
            self.content.update({p.lab : p})

    def log(self):
        if self.name is not None:
            Io.print('#=======================================')
            Io.print('#')
            Io.print('# Session loaded : '+self.name)
            Io.print('#')
            Io.print('#=======================================')
        else:
            Io.print()
            Io.print('No session is loaded !')
            Io.print()
