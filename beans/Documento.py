import sys
sys.stdout.encoding
'UTF-8'
from .Contribuyente import Empresa, Sucursal
from daos import Emisor

class Documento:
    def __init__(self, docId, idSysEmisor, numero, fechaEmision, tipoDocu, observacion, leyendas, moneda, tasaIgv, linkPdf,
                 linkXml, cdrStatus, cdrNota, cdrObservacion, referenciados):
        self.id = docId
        self.idSysEmisor = idSysEmisor
        self.empresa = Empresa(Emisor().getEmprId())
        if Emisor().getSucuId() is None or Emisor().getSucuId() < 1:
            self.emprSucursal = None
        else:
            self.emprSucursal = Sucursal(Emisor().getSucuId())
        self.numero = numero
        self.fechaEmision = fechaEmision
        self.tipoDocumento = TipoDocumento(tipoDocu)
        self.observacion = observacion
        self.leyendas = leyendas
        self.moneda = Moneda(moneda)
        self.enviarSunat = True;
        self.tasaIgv = tasaIgv
        self.linkPdf = linkPdf
        self.linkXml = linkXml
        self.cdrStatus = cdrStatus
        self.cdrNota = cdrNota
        self.cdrObservacion = cdrObservacion
        self.docsReferenciados = referenciados

class ComprobantePago(Documento):
    def __init__(self, idSysEmisor, numero, fechaEmision, tipoDocu, leyendas, cliente, subtotal, total, detallesDocumento,
                 grabada = 0.0, inafecta = 0.0, exonerada = 0.0, gratuita = 0.0, descuento = 0.0, igv = 0.0,
                 isc = 0.0, otrosTributos = 0.0, otrosCargos = 0.0, moneda = "PEN", tiop = "01", anulado = False,
                 emailCliente = None, vendedor = None, linkPdf = None, linkXml = None, cdrStatus = None, cdrNota = None,
                 cdrObservacion = None, tasaIgv = 18, observacion = None, docId = None, referenciados =None):
        super().__init__(docId, idSysEmisor, numero, fechaEmision, tipoDocu, observacion, leyendas, moneda, tasaIgv, linkPdf,
                 linkXml, cdrStatus, cdrNota, cdrObservacion, referenciados)
        self.cliente = cliente
        self.tipoOperacion = TipoOperacion(tiop)
        self.subtotal = subtotal
        self.grabada = grabada
        self.inafecta = inafecta
        if igv is None:
            igv = 0.0
        self.igv = igv
        if self.igv > 0:
            self.exonerada = exonerada
        else:
            self.exonerada = total
        self.gratuita = gratuita
        self.descuento = descuento
        self.isc = isc
        self.otrosTributos = otrosTributos
        self.otrosCargos = otrosCargos
        self.total = total
        self.anulado = anulado
        self.emailCliente = emailCliente
        self.vendedor = vendedor
        self.detallesDocumento = detallesDocumento

class DetalleDocumento:
    def __init__(self, orden, codigoProducto, descripcion, cantidad, precioVenta, subtotal, moneda = "PEN",
                 descuento = 0.0, igv = 0.0, isc = 0.0, ventaNoOnerosa = 0.0, undMedida = "NIU",
                 tiai = None, tisc = None, igvTotal = 0.0):
        self.orden = orden
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precioVenta = precioVenta
        self.subtotal = subtotal
        self.moneda = Moneda(moneda)
        self.descuento = descuento
        if isc is None:
            isc = 0.0
        self.isc = isc
        if igv is None:
            igv = 0.0
        self.igv = igv
        self.ventaNoOnerosa = ventaNoOnerosa
        self.codigoProducto = codigoProducto
        self.unidadMedida = UnidadMedida(undMedida)
        if tiai:
            self.tipoAfectacionIgv = TipoAfectacionIgv(tiai)
        else:
            if self.igv > 0.0:
                self.tipoAfectacionIgv = TipoAfectacionIgv("10")
            else:
                if igvTotal:
                    if igvTotal > 0.0:
                        self.tipoAfectacionIgv = TipoAfectacionIgv(10)
                    else:
                        self.tipoAfectacionIgv = TipoAfectacionIgv("20")
                else:
                    self.tipoAfectacionIgv = TipoAfectacionIgv("20")
        if tisc:
            self.tipoIsc = TipoIsc(tisc)
        else:
            self.tipoIsc = None

class NotaCD(Documento):
    def __init__(self, numero, fechaEmision, tipoDocu, leyendas, subtotal, sustentoNota, tnotacod,
                 referenciados, total = 0.0, moneda = "PEN", anulado = False,
                 igv=0.0, linkPdf = None, linkXml = None, cdrStatus = None, cdrNota = None,
                 cdrObservacion = None, tasaIgv = 18, observacion = None, docId = None):
        super().__init__(docId, numero, fechaEmision, tipoDocu, observacion, leyendas, moneda, tasaIgv, linkPdf,
                 linkXml, cdrStatus, cdrNota, cdrObservacion, referenciados)
        self.subtotal = subtotal
        if igv is None:
            igv = 0.0
        self.igv = igv
        if total is None:
            total = 0.0
        self.total = total
        self.anulado = anulado
        self.sustentoNota = sustentoNota
        self.tipoNota = TipoNota(tnotacod, tipoDocu)

class Moneda:
    def __init__(self, codigo="PEN"):
        self.codigo = codigo

class UnidadMedida:
    def __init__(self, codigo="NIU"):
        self.codigo = codigo

class Leyenda:
    def __init__(self, codigo, descripcion):
        self.codigo = codigo
        self.descripcion = descripcion

class TipoDocumento:
    def __init__(self, codigo):
        self.codigo = codigo

class DocReferenciado:
    def __init__(self, docuId, numero = None, tipoDocu = None):
        self.id = docuId
        self.numero = numero
        self.tipoDocu = tipoDocu

class TipoNota:
    def __init__(self, codigo = None, tipoDocu = None):
        self.codigo = codigo
        self.tipoDocumento = TipoDocumento(tipoDocu)

class TipoOperacion:
    def __init__(self, codigo="01"):
        self.codigo = codigo

class TipoAfectacionIgv:
    def __init__(self, codigo):
        self.codigo = codigo

class TipoIsc:
    def __init__(self, codigo):
        self.codigo = codigo