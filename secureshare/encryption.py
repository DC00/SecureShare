#!/usr/bin/env python
# from Crypto.Hash import SHA256
# from Crypto import Random
# from Crypto.Cipher import DES

from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import ARC4

import os.path
import os
iv = b'12345678'

# def encrypt(text, key):
#     key_size8 = key[0:8]
#     print(key_size8)
#     cipher = DES.new(key_size8, DES.MODE_CFB, iv)
#     encrypted = cipher.encrypt(text)
#     return encrypted


def encrypt(text, key):
	# key = '12345678'
    cipher = ARC4.new(key)
    encrypted_text = cipher.encrypt(text)
    ascii_list = []
    for c in encrypted_text:
    	ascii_list.append(ord(c))
    return ascii_list


# def decrypt(text, key)
#     key_size8 = key[0:8]
#     cipher = DES.new(key_size8, DES.MODE_CFB, iv)
#     return cipher.decrypt(text)


def decrypt(values, key):
	# key = '12345678'
	ascii_values = ""
	for i in values[1:len(values)-1]:
		if i == ',':
			continue
		ascii_values += str(unichr(int(i)))
	cipher = ARC4.new(key)
	decrypted_text = cipher.decrypt(ascii_values)
	return decrypted_text



if __name__ == "__main__":
    # random_generator = Random.new().read
    # key = RSA.generate(1024, random_generator)
    # public_key = key.publickey()
    # secret_string('abcdefghijklmplkjdfklsjfklj', public_key)

    test = encrypt("test", '12345678')
    final = decrypt(test, '12345678')
    print final