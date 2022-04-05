#!/usr/bin/env python3
# -*- coding: utf-8 -*-
           
           
import os            
from src.password import Password
from src.utils import *
           
class SessionEnvironment():
    name        = 'essai'
    all_sec     = os.listdir(CRYPTPATH)
    prompt      = ALINEA
    passpath    = CRYPTPATH
    key         = None
    content     = {}
    
    def __init__(self):
        self.update()
    
    def update(self):
        self.prompt = '('+self.name+') '+ALINEA 
        self.key = self.get_key()
        self.recover(Password)
    
    def get_key(self, password = 'as'):
        return generate_hash_key(password)
    
    def generate_path(self):
        return self.passpath+'/'+self.name

    def recover(self, object):
        self.content.clear()
        for l in read(self.generate_path()):
            p = object(decrypt(self.key,l).split(MARK))        
            self.content.update({p.lab : p})
            
    def log(self):
        print('#######################')
        print('# Session : '+self.name)
        print('#######################')
