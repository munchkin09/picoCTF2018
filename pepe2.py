import json
from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto import Random
from Crypto.Cipher import AES
from itertools import islice
import threading
import time

BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

FLAG = False
expectedHash = 'eyJfZmxhc2hlcyI6W3siIHQiOlsibWVzc2FnZSIsIkVycm9yOiBQbGVhc2UgbG9nLWluIGFnYWluLiJdfV19=='

"""
Usage:
    c = AESCipher('password').encrypt('message')
    m = AESCipher('password').decrypt(c)
Tested under Python 3 and PyCrypto 2.6.1.
"""

def thread_function(line):
    raw = "Cookie: {'username': 'pelos', 'password': 'pelos', 'admin': 0}"
    hashed = str(encrypt(raw, md5(line.encode('utf8')).hexdigest()))
    pssword = line
    print( "Clave " + line + " hash " + hashed  )
    if(hashed == expectedHash):
        print("Esta última clave es la correcta")
        FLAG = True
        N = 100000
        exit()
    return

def encrypt(raw, key):
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return b64encode(iv + cipher.encrypt(raw))

def attack():
    
    N = 8
    y = 0
    filename = "./passwords.txt"
    
    #AESCipher('seed removed').decrypt()
    with open(filename, 'r') as infile:
        while(N <= 10000000 or FLAG != True):
            lines_gen = islice(infile, N)
            for line in lines_gen:
                x = threading.Thread(target=thread_function, args=(line,))
                x.start()
            print(threading.active_count())
            N += 8

def decrypt(enc, key):
    enc = b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:])).decode('utf8')

if __name__ == "__main__":
    attack()