__author__ = 'las3wh'
"""I'm adding a conflict........."""
from Crypto.Hash import SHA256

userpass = {}
while True:
    i = input('Enter a username: ')
    if i is '':
        break
    else:
        user = i
    i = input('Enter a password: ')
    if i is '':
        break
    else:
        pword = SHA256.new(i.encode()).hexdigest()
    userpass[user] = pword
print("Usernames and passwords updated. You can now attempt to log in.")
while False:
    i = input('User: ')
    if i is '':
        break
    else:
        user = i
    i = input('Password: ')
    if i is '':
        break
    else:
        pword = i.encode()
    if not user in userpass:
        print('User not found')
    elif userpass[user] == SHA256.new(bytes(pword)).hexdigest():
        print('hello yo')
    else:
        print('login fails')
    #test comment changing the lines
