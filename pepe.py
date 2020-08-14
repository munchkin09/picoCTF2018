import json
from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto import Random
from Crypto.Cipher import AES
from itertools import islice
import threading
import time
import queue

BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

FLAG = False
expectedHash = 'eyJfZmxhc2hlcyI6W3siIHQiOlsibWVzc2FnZSIsIkVycm9yOiBQbGVhc2UgbG9nLWluIGFnYWluLiJdfV19=='
q = queue.Queue()

fo = open("resultPepe.txt", "r+")

iv = b''
ivFlask = b'\xcb\x9d\xaeMl\x18G"_\x01w\xbc\xe2L\x13 '
def getIV(hash):
    enc = b64decode(hash)
    iv = enc[:16]
    print("iv vale " + str(iv))
    return iv

def thread_function(line, iv):
    raw = "{'password': '1234', 'username': 'pepe', 'admin': 0}"
    hashed = ''
    hashed2 = ''
    try:
        hashed2 = str(encrypt(raw, md5(line.encode('utf8')).hexdigest(),ivFlask))
        hashed = str(encrypt(raw, md5(line.encode('utf8')).hexdigest(),iv))
    except ValueError as e:
        print(e)
        pass
    print( "Clave " + line + " hash " + hashed  )
    print( "Clave " + line + " hash " + hashed2  )
    #if(hashed == expectedHash):
    if(expectedHash in hashed):
        print("Esta última clave es la correcta")
        output = fo.write("La clave (" + line + ") genera este output " + hashed + " igual al esperado " + expectedHash)
        FLAG = True

def worker(iv):
    while True and FLAG == False:
        item = q.get()
        thread_function(item, iv)
        q.task_done()

def attack(iv):
    N = 8
    filename = "./passwords.local.txt"
    
    #AESCipher('seed removed').decrypt()
    # with open(filename, 'r') as infile:
    #     while(N <= 10000000 or FLAG != True):
    #         lines_gen = islice(infile, N)
    #         for line in lines_gen:
    #             x = threading.Thread(target=thread_function, args=(line,))
    #             x.start()
    #         print(threading.active_count())
    #         N += 8
    with open(filename, 'r') as infile:
        for _ in range(N):
            t = threading.Thread(target=worker, args=(iv,))
            t.daemon = True
            t.start()

        for item in infile:
            if FLAG == True:
                break
            else:
                q.put(item)
        q.join()       # block until all tasks are done


"""
Usage:
    c = AESCipher('password').encrypt('message')
    m = AESCipher('password').decrypt(c)
Tested under Python 3 and PyCrypto 2.6.1.
"""
def encrypt(raw, key, iv):
    raw = pad(raw)
    #print(raw)
    #iv = bytes(iv,encoding='utf8')
    #iv = iv[2:-1]
    #print("?????????????????")
    #print(iv)
    #iv = Random.new().read(AES.block_size) # Aquí hay que poner el iv que podamos conseguir del decrypt parcial de la cookie del server
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return b64encode(iv + cipher.encrypt(raw))


def decrypt(enc, key):
    enc = b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:])).decode('utf8')

if __name__ == "__main__":
    iv = getIV('y52uTWwYRyJfAXe84kwTIDTwgndVeGkDkXwca4qKfFaIahbFS1LFiuQ3TUYnUm1+PnGv8VR4YpwF1wk1UZPtd4nBaouT3ZelpAonu532J1s=')
    #attack(iv)
    _ = "{'password': '1234', 'username': 'pepe', 'admin': 0}"
    encrypt("Cookie: {'username': 'pepe', 'password': '1234', 'admin': 0}",'seed removed',md5(str(ivFlask).encode('utf8')).hexdigest())