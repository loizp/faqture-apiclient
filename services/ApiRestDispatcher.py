import sys
sys.stdout.encoding
'UTF-8'
import requests
from beans import Authorization
from utils import ObjJSON

class ApiRestClient:
    def __init__(self):
        self.url_domain = "http://localhost:8080"
        self.url_service = ""
        self.headers = {'Content-type': 'application/json'}

    def authClienteRest(self,userJSON):
        self.url_service = "/auth/login"
        url = "%s%s"%(self.url_domain,self.url_service)
        try:
            response = requests.post(url, json=ObjJSON(userJSON).objDecoder(), headers=self.headers)
            if response.status_code == 200:
                data = ObjJSON(response.content.decode("UTF8")).objDecoder()
                if data['success']:
                    Authorization(data['token'])
                return RespuestaREST(data['success'], data['message'])
            else:
                print(response)
                return RespuestaREST(False, "Accesos denegado al servicio")
        except requests.ConnectionError as e:
            print(e)
            return RespuestaREST(False,"No se puede establecer una conexión")
        except requests.ConnectTimeout as e:
            print(e)
            return RespuestaREST(False, "Tiempo de espera de conexión agotada")
        except requests.HTTPError as e:
            print(e)
            return RespuestaREST(False, "Ruta de enlace no encontrada")
        except requests.RequestException as e:
            print(e)
            return RespuestaREST(False, "No se puede conectar al servicio")

    def cpSendToRest(self,cpJSON):
        self.url_service = "/docs/add/bf/full"
        self.tokenAuth = Authorization().token
        self.headers = {'Content-type': 'application/json', 'Authorization': self.tokenAuth}
        url = "%s%s"%(self.url_domain,self.url_service)
        try:
            response = requests.post(url, json=ObjJSON(cpJSON).objDecoder(), headers=self.headers)
            if response.status_code == 200:
                data = ObjJSON(response.content.decode("UTF8")).objDecoder()
                return RespuestaREST(data['response']['success'],"RestCode: %s; RestMessage: %s"
                                     %(data['response']['code'], data['response']['message']), data['data'])
            else:
                print(response)
                return RespuestaREST(False, "Accesos denegado al servicio")
        except requests.ConnectionError as e:
            print(e)
            return RespuestaREST(False, "No se puede establecer una conexión")
        except requests.ConnectTimeout as e:
            print(e)
            return RespuestaREST(False, "Tiempo de espera de conexión agotada")
        except requests.HTTPError as e:
            print(e)
            return RespuestaREST(False, "Ruta de enlace no encontrada")
        except requests.RequestException as e:
            print(e)
            return RespuestaREST(False, "No se puede conectar al servicio")

class RespuestaREST:
    def __init__(self, success, message, data = None):
        self.__success = success
        self.message = message
        self.data = data

    def isSuccess(self):
        return self.__success