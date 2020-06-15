import sys
sys.stdout.encoding
'UTF-8'
from .ApiRestDispatcher import ApiRestClient
from daos import *
from utils import ObjJSON
from beans import bfSendAdapter
from beans import Authentication

def testConnect(bd):
    if bd == "mongo":
        dbconnect = MongoApiClient()
    elif bd == "pgsql":
        dbconnect = PgSQLApiClient()
    else:
        return False
    conectado = dbconnect.isConnect()
    if conectado:
        dbconnect.disconnect()
    return conectado

def iniciarSesion(uname, upass):
    user = Authentication(uname, upass)
    loginResponse = ApiRestClient().authClienteRest(ObjJSON(user).objEncoder())
    if loginResponse.isSuccess():
        Emisor().setAuth(True)
        user.setDataLogin()
    return loginResponse

def onListen():
    if not ConfigThreadsApi().isListening():
        if ConfigThreadsApi().usaPostgreSQL():
            PgSQLApiClient().creaTablaDocE()

        ApiThread(1, "listen", mongo=ConfigThreadsApi().usaMongoDB(), pgsql=ConfigThreadsApi().usaPostgreSQL()).start()

def onForward(numhrs = 2):
    if not ConfigThreadsApi().isForwarding():
        if ConfigThreadsApi().usaPostgreSQL():
            PgSQLApiClient().creaTablaDocE()
        ConfigThreadsApi().setTimeForward(numhrs)
        tiempo = numhrs*3600
        ApiThread(2, "forward", tiempo=tiempo, mongo=ConfigThreadsApi().usaMongoDB(), pgsql=ConfigThreadsApi().usaPostgreSQL()).start()

def envioCP(docuEmisorId, cpJSON, mongo = True, pgsql = False):
    envioResponse = ApiRestClient().cpSendToRest(cpJSON)
    if envioResponse.isSuccess():
        if pgsql:
            PgSQLApiClient().almacenaDocE(docuEmisorId, "Documento enviado con exito: RESTfaqture", "C", None,
                                          ObjJSON(envioResponse.data).objEncoder())
        if mongo:
            MongoApiClient().almacenaDocE(docuEmisorId, "Documento enviado con exito: RESTfaqture", "C", None,
                                          ObjJSON(envioResponse.data).objEncoder())
    else:
        if pgsql:
            PgSQLApiClient().almacenaDocE(docuEmisorId, envioResponse.message, "P", None, envioResponse.data)
        if mongo:
            MongoApiClient().almacenaDocE(docuEmisorId, envioResponse.message, "P", None, envioResponse.data)

def main_distributor(mongo = True, pgsql = False):
    q = PgQueueComercial('data')

    def newCallback(m):
        if m.payload:
            payload = m.payload
            docuPayload = ObjJSON(payload).objDecoder()
            compPago = bfSendAdapter(docuPayload)

            cpJSON = ObjJSON(compPago).objEncoder()
            if pgsql:
                PgSQLApiClient().almacenaDocE(docuPayload['docu_idkenaani'], "Documento extraido desde Kenaani", "P",
                                              cpJSON)
            if mongo:
                MongoApiClient().almacenaDocE(docuPayload['docu_idkenaani'], "Documento extraido desde Kenaani", "P",
                                              cpJSON)

            envioCP(docuPayload['docu_idkenaani'], cpJSON, mongo, pgsql)

    q.recvCallback = newCallback
    q.start()

def reenvioFaltantes(local_handler, tiempo, mongo = True, pgsql = False):
    ConfigThreadsApi().setForwarding(True)
    if pgsql:
        resultado = PgSQLApiClient().documentosFaltantes()
        for (doel_id, doel_idsysemisor, doel_documento, doel_estado, doel_fechahora, doel_respuesta,
             doel_observacion) in resultado:
            envioCP(doel_idsysemisor, doel_documento, mongo, pgsql)
    
    if mongo:
        resultado = MongoApiClient().documentosFaltantes()
        for row in resultado:
            envioCP(row['idsysemisor'], row['documento'], mongo, pgsql)

    if not ConfigThreadsApi().stopForward():
        local_handler.enter(tiempo, 1, reenvioFaltantes, (local_handler, tiempo, mongo, pgsql,))

def reenvioDaemon(tiempo, mongo = True, pgsql = False):
    from time import time, sleep
    from sched import scheduler
    handler = scheduler(time, sleep)
    handler.enter(tiempo, 1, reenvioFaltantes, (handler, tiempo, mongo, pgsql,))
    ConfigThreadsApi().setForwarding(True)
    handler.run()

from threading import Thread
class ApiThread (Thread):
    def __init__(self, threadID, name, tiempo = 7200, mongo = True, pgsql = False):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.tiempo = tiempo
        self.mongo = mongo
        self.pgsql = pgsql

    def run(self):
        print ("Iniciando el distribuidor: ", self.name)
        from views import newAPIVentana
        if self.threadID == 1:
            main_distributor(self.mongo, self.pgsql)
            ConfigThreadsApi().setListening(False)
            ConfigThreadsApi().setStopListen(False)
            newAPIVentana("Se dejó de escuchar al emisor")
        elif self.threadID == 2:
            reenvioDaemon(self.tiempo, self.mongo, self.pgsql)
            ConfigThreadsApi().setForwarding(False)
            ConfigThreadsApi().setStopForward(False)
            newAPIVentana("Se dejó de ejecutar el reenvio")
        else:
            print("no existe ninguna operación por realizar")

        print ("Se terminó de ejecutar el proceso: " + self.name)
