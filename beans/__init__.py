import sys
sys.stdout.encoding
'UTF-8'
from .Login import Authentication
from .Login import Authorization
from .Contribuyente import Cliente
from .Documento import ComprobantePago
from .Documento import NotaCD
from .Documento import DetalleDocumento
from .Documento import Leyenda
from .Documento import DocReferenciado

def bfSendAdapter(bfOriginal):
    itemsdoc = bfdetSendAdapter(bfOriginal['docu_detalles'], bfOriginal['docu_igv'])
    bf = ComprobantePago(idSysEmisor=bfOriginal['docu_idkenaani'] ,numero=bfOriginal['docu_numero'], fechaEmision=bfOriginal['docu_fechaemision'],
                         tipoDocu=bfOriginal['tido_codigo'], leyendas=None,
                         cliente=Cliente(nombreLegal=bfOriginal['clie_nombrelegal'],
                                         numeroDocumento=bfOriginal['clie_numerodocumento'],
                                         direccion=bfOriginal['clie_direccion'],
                                         tdocIdent=bfOriginal['tidi_codigo'], ubigcod=bfOriginal['ubig_codigo']),
                         subtotal=bfOriginal['docu_subtotal'], total=bfOriginal['docu_total'],
                         descuento=bfOriginal['docu_descuento'], igv=bfOriginal['docu_igv'],
                         vendedor=bfOriginal['docu_vendedor'], moneda=bfOriginal['mone_codigo'],
                         tasaIgv=bfOriginal['docu_tasaigv'], observacion=bfOriginal['docu_observacion'],
                         anulado=bfOriginal['docu_anulado'], detallesDocumento=itemsdoc)
    return bf

def bfdetSendAdapter(bfdetOriginal, igvTotal):
    bfdet = []
    for item in bfdetOriginal:
        bfdet.append(DetalleDocumento(orden=item['dedo_orden'], descripcion=item['dedo_descripcion'],
                                      cantidad=item['dedo_cantidad'], precioVenta=item['dedo_precioventa'],
                                      subtotal=item['dedo_subtotal'], descuento=item['dedo_descuento'],
                                      codigoProducto=item['dedo_codigoproducto'], undMedida=item['unme_codigo'],
                                      igvTotal=igvTotal))
    return bfdet