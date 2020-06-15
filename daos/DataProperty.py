import sys
sys.stdout.encoding
'UTF-8'
import json

class Emisor:
    def __init__(self):
        self.__data = self.__leerDatos()

    def getEmprId(self):
        return self.__data['empresa']

    def getSucuId(self):
        return self.__data['sucursal']

    def isAuth(self):
        return self.__data['isAuth']

    def setAuth(self, value = False):
        self.__data['isAuth'] = value
        self.__escribirDatos()

    def __escribirDatos(self):
        with open('./resources/datos/emisor.json', 'w') as file:
            json.dump(self.__data, file)
            file.close()

    def __leerDatos(self):
        with open('./resources/datos/emisor.json', 'r') as file:
            info = json.load(file)
            file.close()
            return info

class ConfigThreadsApi:
    def __init__(self):
        self.__data = self.__leerDatos()

    def usaMongoDB(self):
        return self.__data['usaMongoDB']

    def setMongoDB(self, value = True):
        self.__data['usaMongoDB'] = value
        self.__escribirDatos()

    def usaPostgreSQL(self):
        return self.__data['usaPostgreSQL']

    def setPostgreSQL(self, value = False):
        self.__data['usaPostgreSQL'] = value
        self.__escribirDatos()

    def getTimeForward(self):
        return self.__data['timeForward']

    def setTimeForward(self, value = 2):
        self.__data['timeForward'] = value
        self.__escribirDatos()

    def isListening(self):
        return self.__data['isListening']

    def setListening(self, value = False):
        self.__data['isListening'] = value
        self.__escribirDatos()

    def isForwarding(self):
        return self.__data['isForwarding']

    def setForwarding(self, value = False):
        self.__data['isForwarding'] = value
        self.__escribirDatos()

    def stopListen(self):
        return self.__data['stopListen']

    def setStopListen(self, value = False):
        self.__data['stopListen'] = value
        self.__escribirDatos()

    def stopForward(self):
        return self.__data['stopForward']

    def setStopForward(self, value=False):
        self.__data['stopForward'] = value
        self.__escribirDatos()

    def setInicial(self):
        self.__data['isListening'] = False
        self.__data['isForwarding'] = False
        self.__data['stopListen'] = False
        self.__data['stopForward'] = False
        self.__escribirDatos()

    def __escribirDatos(self):
        with open('./resources/datos/threads.json', 'w') as file:
            json.dump(self.__data, file)
            file.close()

    def __leerDatos(self):
        with open('./resources/datos/threads.json', 'r') as file:
            info = json.load(file)
            file.close()
            return info

