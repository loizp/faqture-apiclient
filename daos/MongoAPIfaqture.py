import sys
sys.stdout.encoding
'UTF-8'
import pymongo
import datetime
from .SourcesDBconnect import SourceAPImongo

class MongoApiClient:
    def __init__(self):
        self.__connect = False
        self.__conectar()
        if self.__connect:
            self.mongodata = self.mongodb["APIfaqtureData"]
            self.docFE = self.mongodata["DocumentosFE"]

    def __conectar(self):
        try:
            source = SourceAPImongo().getDataSourceConnection()
            self.mongodb = pymongo.MongoClient("{0}:{1}".format(source['host'],source['port']),
                                               serverSelectionTimeoutMS=1000)
            self.mongodb.server_info()
            self.__connect = True
        except pymongo.errors.ServerSelectionTimeoutError as err:
            print("No se puede establecer conexión con MongoDB ",err)

    def isConnect(self):
        return self.__connect

    def disconnect(self):
        if self.__connect:
            self.mongodb.close()
            self.__connect = False

    def existeDocuE(self, idsysemisor):
        if self.__connect:
            try:
                existe = self.docFE.count({"idsysemisor": idsysemisor})
                if existe > 0:
                    return True
                else:
                    return False
            except ImportError:
                platform_specific_module = None

    def almacenaDocE(self, idsysemisor, observacion = '', estado = 'P', docujson = None, respuesta = None):
        ahora = datetime.datetime.now().isoformat()
        msg = "Documento: %s - Almacenado correctamente."%(idsysemisor)
        if self.__connect:
            try:
                if self.existeDocuE(idsysemisor):
                    if not docujson:
                        self.docFE.update_one(
                            {"idsysemisor": idsysemisor},
                            {
                                "$set":
                                    {
                                        "estado": estado,
                                        "fechahora": ahora,
                                        "observacion": observacion,
                                        "respuesta": respuesta
                                    }
                            }
                        )
                    else:
                        self.docFE.update_one(
                            {"idsysemisor": idsysemisor},
                            {
                                "$set":
                                    {
                                        "documento": docujson,
                                        "estado": estado,
                                        "fechahora": ahora,
                                        "observacion": observacion,
                                        "respuesta": respuesta
                                    }
                            }
                        )
                else:
                    if docujson:
                        self.docFE.insert_one(
                            {
                                "idsysemisor": idsysemisor,
                                "documento": docujson,
                                "estado": estado,
                                "fechahora": ahora,
                                "observacion": observacion,
                                "respuesta": respuesta
                            }
                        )
                    else:
                        msg = 'No existe ningun documento electrónico por almacenar'
                print(msg)
            except ImportError:
                platform_specific_module = None
                print("Ocurrio un error en el almacenamiento en la Base de Datos")
            finally:
                self.disconnect()

    def documentosFaltantes(self):
        if self.__connect:
            try:
                faltantes = self.docFE.find({"estado": "P"})
                return faltantes
            except ImportError:
                platform_specific_module = None
            finally:
                self.disconnect()