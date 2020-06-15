import sys
sys.stdout.encoding
'UTF-8'
class Empresa:
    def __init__(self, emprId):
        self.id = emprId

class Cliente:
    def __init__(self, nombreLegal, numeroDocumento, urbanizacion = None, ubigcod = None, direccion = None,
                 nombreComercial = None, tdocIdent = "6", clieId = None):
        self.id = clieId
        self.nombreLegal = nombreLegal
        self.nombreComercial = nombreComercial
        self.direccion = direccion
        self.numeroDocumento = numeroDocumento
        self.urbanizacion = urbanizacion
        self.tipoDocumentoIdentidad = TipoDocumentoIdentidad(tdocIdent)
        self.ubigeo = Ubigeo(ubigcod)

class Sucursal:
    def __init__(self, sucuId):
        self.id = sucuId


class TipoDocumentoIdentidad:
    def __init__(self, codigo = '6'):
        self.codigo = codigo

class Ubigeo:
    def __init__(self, codigo = None):
        self.codigo = codigo