from Crypto.Hash import SHA256

from Crypto import Random
import os.path
import os
from Crypto.Cipher import DES

iv = b'\x15\xff\xf3\xdfL\xa3\x82\xb8'

def encrypt_text(text, key):
    key_size8 = key[0:8]
    cipher = DES.new(key_size8, DES.MODE_CFB, iv)
    encrypted = cipher.encrypt(text)
    return encrypted

def decrypt_text(text, key):
    key_size8 = key[0:8]
    cipher = DES.new(key_size8, DES.MODE_CFB, iv)
    return cipher.decrypt(text)

def downloadFile():
    #include code to download the file here
    pass

def viewFiles():
    print('REPORTS:')
    for file in os.listdir(os.curdir):
       if file.endswith(".txt"):
	  print(file)
    print('\n')
    while True:
       choice = raw_input('Which file would you like to open (enter q to quit): ')
       if choice is 'q':
          break
       elif not os.path.isfile(choice):
          print('THAT FILE DOES NOT EXIST')
       else:
          f = open(choice, 'r')
          contents = f.read()
          f.close()
          print('\n')
          print(choice)
	  print
          print(contents)
          print('\n')
          break


def decrypt_file(fileName, key):
    if not os.path.isfile(fileName):
        print('\nTHAT FILE IS NOT IN THE CURRENT DIRECTORY OR DOES NOT EXIST. PLEASE TRY AGAIN\n')
        return False
    output = ""
    f = open(fileName, 'rb')
    key_size8 = key[0:8]
    cipher = DES.new(key_size8, DES.MODE_CFB, iv)
    for line in f:
	output += cipher.decrypt(line)
	output += '\n'
    print '\n'
    print fileName
    print
    print output

def logIn():
    print('Please Log In')
    global user
    user = raw_input('Username: ')
    global password
    password = raw_input('Password: ')

def mainMenu():
    run = True
    while True:
        print('Please select one of the following options.')
        print('1. View/Download Articles')
        print('2. Decrypt File')
        print('3. Relog In')
        print('4. Quit')
        choice = raw_input('Enter your choice: ')
	print('\n')
        if choice is '1':
            viewFiles()
        elif choice is '2':
	    choice = raw_input('Enter the name of the file you want to decrypt: ')
            decrypt_file(choice, 'this is a secure key')
        elif choice is '3':
            logIn()
        elif choice is '4':
            break
        else:
            print('PLEASE ENTER A VALID CHOICE\n')


if __name__ == "__main__":
    print('Secure Share v1.0')
    logIn()
    mainMenu()
