import sys
sys.stdout.encoding
'UTF-8'
from utils import FernetCrypt

class Authentication:
    def __init__(self, username = None, password = None):
        self.username = username
        self.password = password

    def setDataLogin(self):
        key = "$APIf@qtureL0g1n"
        usernameenc = FernetCrypt(key).encrypt(self.username)
        with open('./private/log_security1.bin', 'wb') as file_uname:  file_uname.write(usernameenc)
        file_uname.close()
        passwordenc = FernetCrypt(key).encrypt(self.password)
        with open('./private/log_security2.bin', 'wb') as file_upass:  file_upass.write(passwordenc)
        file_upass.close()

    def getDataLogin(self):
        key = "$APIf@qtureL0g1n"
        with open('./private/log_security1.bin', 'rb') as file_uname:
            for line in file_uname:
                usernameenc = line
            file_uname.close()
        with open('./private/log_security2.bin', 'rb') as file_upass:
            for line in file_upass:
                passwordenc = line
            file_upass.close()
        self.username = FernetCrypt(key).decrypt(usernameenc)
        self.password = FernetCrypt(key).decrypt(passwordenc)

class Authorization:
    def __init__(self, token = None):
        self.token = token

        if self.token:
            self.__setDataToken()
        else:
            self.__getDataToken()

    def __setDataToken(self):
        key = "$API@uth0r1z@t10n"
        tokenenc = FernetCrypt(key).encrypt(self.token)
        with open('./private/con_security.bin', 'wb') as file_token:  file_token.write(tokenenc)
        file_token.close()

    def __getDataToken(self):
        key = "$API@uth0r1z@t10n"
        with open('./private/con_security.bin', 'rb') as file_token:
            for line in file_token:
                tokenenc = line
            file_token.close()
        self.token = FernetCrypt(key).decrypt(tokenenc)