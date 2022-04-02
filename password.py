#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64, hashlib
from getpass             import getpass
from cryptography.fernet import Fernet


CRYPTPATH = './test/'
MARK      = '#netrisca#?!?#acsirten#'

def generate_hash_key(clear_pass):
    encoded_pass = clear_pass.encode("utf-8") 
    hash_key     = hashlib.md5(encoded_pass).hexdigest()
    return base64.urlsafe_b64encode(hash_key.encode("utf-8"))

def crypt(key, clear_text):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(clear_text.encode("utf-8"))
    return encrypted

def decrypt(key, encoded_text):
    fernet = Fernet(key)
    clear_text = fernet.decrypt(encoded_text)
    return clear_text.decode("utf-8")

def read(name):
    with open(name, 'rb') as encrypted_file:
        text = encrypted_file.read()
        return text.split()
    

def write(name, key, text):
    with open(name, 'ab') as encrypted_file:
        encrypted_file.write('\n'.encode('utf-8'))
        encrypted_file.write(crypt(key, text))
        

class Password():
    lab = None
    url = None
    com = None
    has = None
    
    def __init__(self, info=None):
        if info:
            self.lab = info[0]
            self.url = info[1]
            self.com = info[2]
            self.has = info[3]
        else:
            pass
        

    def convert(self, name, key):
        compact = self.lab+MARK+self.url+MARK+self.com+MARK+self.has
        write(name, key, compact)
    

           
class Session():
    passpath = CRYPTPATH
    passfile = 'essai'
    key      = None
    content  = []
    
    
    def __init__(self):
        self.key = self.get_key()
        self.recover()
    
    def get_key(self, password = 'as'):
        return generate_hash_key(password)
    
    def generate_path(self):
        return self.passpath+'/'+self.passfile

    def recover(self):
        for l in read(self.generate_path()):
            p = Password(decrypt(self.key,l).split(MARK))        
            self.content.append(p)