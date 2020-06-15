import sys
sys.stdout.encoding
'UTF-8'
import json
from utils import AESCipher

class SourceDBemisor:
    def __init__(self):
        self.__filename = "./resources/datos/sourcedbemisor.json"
        self.__data = self.__leerDatos()
        self.__salt = "DBem1$0r"

    def getDBMotor(self):
        return self.__data['dbmotor']

    def setDBMotor(self, value):
        self.__data['dbmotor'] = value
        self.__escribirDatos()

    def getSchema(self):
        return self.__data['schema']

    def setSchema(self, value):
        self.__data['schema'] = value
        self.__escribirDatos()

    def getHostPort(self):
        return {"host": self.__data['host'], "port": self.__data['port']}

    def setHostPort(self, host, port):
        self.__data['host'] = host
        self.__data['port'] = port
        self.__escribirDatos()

    def setDBmainConnect(self, dbname, dbuser, dbupass):
        self.__data['dbname'] = self.__encripta(dbname)
        self.__data['dbuser'] = self.__encripta(dbuser)
        self.__data['dbupass'] = self.__encripta(dbupass)
        self.__escribirDatos()

    def getDataSourceConnection(self):
        if self.__data['dbmotor'] == "pgsql":
            dsn = "host='{0}' port='{1}' dbname='{2}' user='{3}' password='{4}'"\
                .format(self.__data['host'],
                        self.__data['port'],
                        self.__desencripta(self.__data['dbname']),
                        self.__desencripta(self.__data['dbuser']),
                        self.__desencripta(self.__data['dbupass']))
        return dsn

    def __encripta(self, dato):
        return AESCipher(self.__salt).encrypt(dato)

    def __desencripta(self, dato):
        return AESCipher(self.__salt).decrypt(dato)

    def __escribirDatos(self):
        with open(self.__filename, 'w') as file:
            json.dump(self.__data, file)
            file.close()

    def __leerDatos(self):
        with open(self.__filename, 'r') as file:
            info = json.load(file)
            file.close()
            return info

class SourceAPImongo:
    def __init__(self):
        self.__filename = "./resources/datos/sourceapimongo.json"
        self.__data = self.__leerDatos()
        self.__salt = "M0ng0D$N"

    def getDataSourceConnection(self):
        return {"host": self.__data['host'], "port": self.__data['port'],
                "dbuser": self.__desencripta(self.__data['dbuser']),
                "dbupass": self.__desencripta(self.__data['dbupass'])}

    def setDataSourceConnection(self, host, port, dbuser = None, dbupass = None):
        self.__data['host'] = host
        self.__data['port'] = port
        if dbuser and len(dbuser) > 3:
            self.__data['dbuser'] = self.__encripta(dbuser)
        if dbupass and len(dbupass) > 3:
            self.__data['dbupass'] = self.__encripta(dbupass)
        self.__escribirDatos()

    def __encripta(self, dato):
        return AESCipher(self.__salt).encrypt(dato)

    def __desencripta(self, dato):
        return AESCipher(self.__salt).decrypt(dato)

    def __escribirDatos(self):
        with open(self.__filename, 'w') as file:
            json.dump(self.__data, file)
            file.close()

    def __leerDatos(self):
        with open(self.__filename, 'r') as file:
            info = json.load(file)
            file.close()
            return info

class SourceAPIpgsql:
    def __init__(self):
        self.__filename = "./resources/datos/sourceapipgsql.json"
        self.__data = self.__leerDatos()
        self.__salt = "Pq$q1D$N"

    def getSchema(self):
        return self.__data['schema']

    def setSchema(self, value):
        self.__data['schema'] = value
        self.__escribirDatos()

    def getHostPort(self):
        return {"host": self.__data['host'], "port": self.__data['port']}

    def setHostPort(self, host, port):
        self.__data['host'] = host
        self.__data['port'] = port
        self.__escribirDatos()

    def setDBmainConnect(self, dbname, dbuser, dbupass):
        self.__data['dbname'] = self.__encripta(dbname)
        self.__data['dbuser'] = self.__encripta(dbuser)
        self.__data['dbupass'] = self.__encripta(dbupass)
        self.__escribirDatos()

    def getDataSourceConnection(self):
        dsn = "host='{0}' port='{1}' dbname='{2}' user='{3}' password='{4}'".format(self.__data['host'],
                                                                                    self.__data['port'],
                                                                                    self.__desencripta(
                                                                                        self.__data['dbname']),
                                                                                    self.__desencripta(
                                                                                        self.__data['dbuser']),
                                                                                    self.__desencripta(
                                                                                        self.__data['dbupass']))
        return dsn

    def __encripta(self, dato):
        return AESCipher(self.__salt).encrypt(dato)

    def __desencripta(self, dato):
        return AESCipher(self.__salt).decrypt(dato)

    def __escribirDatos(self):
        with open(self.__filename, 'w') as file:
            json.dump(self.__data, file)
            file.close()

    def __leerDatos(self):
        with open(self.__filename, 'r') as file:
            info = json.load(file)
            file.close()
            return info