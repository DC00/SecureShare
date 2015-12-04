from Crypto.Hash import SHA256
from Crypto import Random
import os.path
import os
from Crypto.Cipher import DES

def encrypt_text(text, key):
    key_size8 = key[0:8]
    cipher = DES.new(key_size8, DES.MODE_CFB, b'\x15\xff\xf3\xdfL\xa3\x82\xb8')
    encrypted = cipher.encrypt(text)
    return encrypted
​
def decrypt_text(text, key):
    key_size8 = key[0:8]
    cipher = DES.new(key_size8, DES.MODE_CFB, iv)
    return cipher.decrypt(text)