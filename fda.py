from Crypto.Hash import SHA256

from Crypto import Random
import os.path
from Crypto.Cipher import DES

iv = b'\x15\xff\xf3\xdfL\xa3\x82\xb8'

def encrypt_file(fileName, key):
    if not os.path.isfile(fileName):
        return False
    f = open(fileName, 'rb')
    f2 = open(fileName+'.enc', 'wb')
    if f.__sizeof__() is 0:
        return False
    key_size8 = key[0:8]
    cipher = DES.new(key_size8, DES.MODE_CFB, iv)
    for line in f:
        f2.write((cipher.encrypt(line)))
    return True

def decrypt_file(fileName, key):
    if not os.path.isfile(fileName):
        return False
    f = open(fileName, 'rb')
    f2 = open('DEC_' + fileName[:-4], 'wb')
    if(f.__sizeof__() is 0) or fileName[-3:] != 'enc':
        return False
    key_size8 = key[0:8]
    cipher = DES.new(key_size8, DES.MODE_CFB, iv)
    for line in f:
        f2.write((cipher.decrypt(line)))
    return True


def downloadFile():
    #include code to download the file here
    pass

def viewFiles():
    #include code to print out a list of files to choose from
    pass

def decryptFile():
    pass

def logIn():
    print('Please Log In')
    global user
    user = input('Username: ')
    global password
    password = input('Passowrd: ')

def mainMenu():
    run = True
    while True:
        print('Please select one of the following options.')
        print('1. View/Download Articles')
        print('2. Decrypt File')
        print('3. Relog In')
        print('4. Quit')
        choice = input('Enter your choice: ')
        if choice == '1':
            viewFiles()
        if choice == '2':
            decryptFile()
        if choice == '3':
            logIn()
        if choice == '4':
            break

if __name__ == "__main__":
    print('Secure Share v1.0')
    logIn()
    mainMenu()
    encrypt_file('test.txt', 'well memed mlady')
    decrypt_file('test.txt.enc', 'well memed mlady')