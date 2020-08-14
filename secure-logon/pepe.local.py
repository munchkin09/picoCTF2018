from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto import Random
from Crypto.Cipher import AES


BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]
key = 'seed removed'
iv = ''
hashed = ''
class AESCipher:
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    def __init__(self, key):
        print(key.encode('utf8'))
        self.key = md5(key.encode('utf8')).hexdigest()
        self.iv = Random.new().read(AES.block_size)
        
    def encrypt(self, raw):
        raw = pad(raw)
        
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        hashed = b64encode(self.iv + cipher.encrypt(raw))
        return hashed

    def decrypt(self, enc):
        enc = b64decode(enc)
        #self.iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        print(cipher.decrypt(enc[16:]))
        return unpad(cipher.decrypt(enc[16:])).decode('utf8')

if __name__ == "__main__":
    raw = "Cookie: {'username': 'pepe', 'password': '1234', 'admin': 0}"
    aes = AESCipher('seed removed')
    print(aes.encrypt(md5(raw.encode('utf8')).hexdigest()))
    print("Ahora el decrypt")
    print(aes.decrypt(hashed))
    #
