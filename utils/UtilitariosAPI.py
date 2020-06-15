import sys
sys.stdout.encoding
'UTF-8'
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, MultiFernet
import base64, os, re, json

class ObjModelEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__

class ObjJSON:
    def __init__(self, obj):
        self.obj = obj

    def objEncoder(self):
        return json.dumps(self.obj, cls=ObjModelEncoder, indent=4, ensure_ascii=False)

    def objDecoder(self):
        return json.loads(self.obj)

class AESCipher:
    def __init__(self, key = None):
        if key and len(key) >= 8:
            self.__key = bytes(''.join(r'\x{0:x}'.format(ord(c)) for c in key[:8]), encoding='utf-8')
        else:
            self.__key = None
            print("Generando nueva clave aleatoria ya que la clave entregada no cumple los requisitos")

    def encrypt(self, raw):
        if raw is None or len(raw) == 0:
            return ''
        raw = raw + '\0' * (32 - len(raw) % 32)
        raw = bytes(raw, encoding='utf-8')
        iv = os.urandom(16)
        if self.__key is None:
            self.__key = os.urandom(32)
            randomkey = self.key
        else:
            randomkey = b""
        cipher = Cipher(algorithms.AES(self.__key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        return bytes(base64.b64encode(iv + randomkey + encryptor.update(raw))).decode("utf-8")

    def decrypt(self, enc):
        if enc is None or len(enc) == 0:
            return ''
        enc = base64.b64decode(enc)
        iv = enc[:16]
        if self.__key is None:
            self.__key = enc[16:48]
            inicia = 48
        else:
            inicia = 16
        cipher = Cipher(algorithms.AES(self.__key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        try:
            dec = bytes(decryptor.update(enc[inicia:])).decode("utf-8")
        except Exception as e:
            print("Ocurrió un error:",e)
            dec = ""
        return re.sub('\0*$','', dec)

class FernetCrypt:
    def __init__(self, key):
        self.__key = bytes(key[::-1], encoding='utf-8')

    def encrypt(self, raw):
        raw = bytes(raw, encoding='utf-8')
        salt1 = os.urandom(16)
        salt2 = Fernet.generate_key()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt1,
            iterations=100000,
            backend=default_backend())
        key1 = Fernet(base64.urlsafe_b64encode(kdf.derive(self.__key)))
        key2 = Fernet(salt2)
        f = MultiFernet([key1, key2])
        return base64.b64encode(salt1) + salt2 + f.encrypt(raw)

    def decrypt(self, enc):
        salt1 = base64.b64decode(enc[:24])
        salt2 = enc[24:68]
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt1,
            iterations=100000,
            backend=default_backend())
        key1 = Fernet(base64.urlsafe_b64encode(kdf.derive(self.__key)))
        key2 = Fernet(salt2)
        f = MultiFernet([key1, key2])
        try:
            dec = bytes(f.decrypt(enc[68:])).decode("utf-8")
        except Exception as e:
            print("Ocurrió un error:",e)
            dec = None
        return dec