from Crypto.Hash import SHA256
from Crypto import Random

from Crypto.Cipher import ARC4
import binascii
import base64


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
    #print("encrypted receives: %s" %(text))
    cipher = ARC4.new(key)
    encrypted_text = cipher.encrypt(text.encode('utf-8'))
    #print("encrypt sends: %s" %(encrypted_text))
    return encrypted_text


def decrypt(text, key):
    #print("decrypt receives: %s" %(text))
    cipher = ARC4.new(key)
    decrypted_text = cipher.decrypt(text)
    #print("decrypted text: %s" %(decrypted_text))
    return decrypted_text.decode("utf-8")




# text to unicode
# unicode to ascii
# send the ascii
# convert ascii back to unicode
# decrypt the unicode
# unicode to python string


# unicode to ascii: u.encode('utf8')
# unicode to ascii: maybe u.encode('utf-8')
# unicode to ascii: u.encode('ascii', 'ignore')

# byte string to python string  b'string'.deocde("utf-8")




def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))



if __name__ == "__main__":
    test2 = base64.b64encode(encrypt("test message", '123456789'))
    print(test2)
    test3 = decrypt(base64.b64decode(test2), '123456789')
    print(test3)
    #test = encrypt("test message. pls work", '12345678')
    #final = decrypt(test, '12345678')


