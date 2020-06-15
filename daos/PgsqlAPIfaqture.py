import sys
sys.stdout.encoding
'UTF-8'
import psycopg2, datetime
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .SourcesDBconnect import SourceAPIpgsql

class PgSQLApiClient:
    def __init__(self):
        self.__connect = False
        self.dataBaseConnection()

    def dataBaseConnection(self):
        try:
            self.conn = psycopg2.connect(SourceAPIpgsql().getDataSourceConnection())
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.curs = self.conn.cursor()
            self.__connect = True
            print('Conectado a la Base de Datos BD_APICliente_faqture')
        except:
            print('Ocurrió un error al conectar a la Base de Datos APIClient_faqture')

    def isConnect(self):
        return self.__connect

    def disconnect(self):
        if self.__connect:
            self.__connect = False
            self.curs.close()
            self.conn.close()

    def existeTabla(self, tabla):
        if self.__connect:
            existe_sql = """SELECT CASE WHEN COUNT(*) = 0  THEN False ELSE True END AS existe
                            FROM information_schema.tables 
                            WHERE table_catalog = CURRENT_CATALOG AND table_schema = CURRENT_SCHEMA 
                                AND table_name = '{0}';""".format(tabla)
            self.curs.execute(existe_sql)
            result = self.curs.fetchone()
            return result[0]

    def creaTablaDocE(self):
        tabladoce_sql = """ CREATE SEQUENCE documentos_electronicos_doel_id_seq;
                            CREATE TABLE documentos_electronicos (
                                doel_id INTEGER NOT NULL DEFAULT nextval('documentos_electronicos_doel_id_seq'),
                                doel_idsysemisor INTEGER NOT NULL,
                                doel_documento TEXT NOT NULL,
                                doel_estado CHAR(1) DEFAULT 'P' NOT NULL,
                                doel_fechahora TIMESTAMP NOT NULL,
                                doel_respuesta TEXT,
                                doel_observacion VARCHAR NOT NULL,
                                CONSTRAINT documentos_electronicos_pk PRIMARY KEY (doel_id)
                            );
                            COMMENT ON TABLE documentos_electronicos IS 'Tabla con los documentos electrónicos del cliente';
                            COMMENT ON COLUMN documentos_electronicos.doel_id IS 'Campo PK autoincremental';
                            COMMENT ON COLUMN documentos_electronicos.doel_idsysemisor IS 'Campo clave para identificar el documento en el sistema del emisor';
                            COMMENT ON COLUMN documentos_electronicos.doel_documento IS 'Campo con el documento en JSON';
                            COMMENT ON COLUMN documentos_electronicos.doel_estado IS 'Estado del proceso de envio que tiene los valores.
                            P = Pendiente de envio.
                            E = Enviado
                            C = Completado satisfactoriamente el envio';
                            COMMENT ON COLUMN documentos_electronicos.doel_fechahora IS 'Campo con la fecha y hora en la que ocurrio el último estado del proceso.';
                            COMMENT ON COLUMN documentos_electronicos.doel_respuesta IS 'Campo con el Objeto JSON de respuesta del REST al API';
                            COMMENT ON COLUMN documentos_electronicos.doel_observacion IS 'Campo en caso de existir algun error o detalle sobre el envio y/o recepcion según el estado';

                            ALTER SEQUENCE documentos_electronicos_doel_id_seq OWNED BY documentos_electronicos.doel_id;"""
        if self.__connect:
            if not self.existeTabla("documentos_electronicos"):
                self.curs.execute(tabladoce_sql)
                self.disconnect()
                print("Se ha creado la tabla documentos_electronicos")

    def existeDocuE(self, idsysemisor):
        existe_sql = """SELECT CASE WHEN COUNT(*) = 0  THEN False ELSE True END AS existe 
                        FROM documentos_electronicos 
                        WHERE doel_idsysemisor = {0};""".format(idsysemisor)
        if self.__connect:
            self.curs.execute(existe_sql)
            result = self.curs.fetchone()
            return result[0]

    def almacenaDocE(self, idsysemisor, observacion = '', estado = 'P', docujson = None, respuesta = None):
        ahora = datetime.datetime.now().isoformat()
        msg = "Documento: %s - Almacenado correctamente." % (idsysemisor)

        if self.__connect:
            if self.existeDocuE(idsysemisor):
                if docujson is None:
                    query = """ UPDATE documentos_electronicos
                                SET doel_estado = %s, doel_fechahora = %s,
                                    doel_respuesta = %s, doel_observacion = %s
                                WHERE doel_idsysemisor = %s"""
                    data = (estado, ahora, respuesta, observacion, idsysemisor)
                else:
                    query = """ UPDATE documentos_electronicos
                                SET doel_estado = %s, doel_fechahora = %s,
                                    doel_respuesta = %s, doel_observacion = %s, doel_documento = %s
                                WHERE doel_idsysemisor = %s"""
                    data = (estado, ahora, respuesta, observacion, docujson, idsysemisor)

                self.curs.execute(query, data)
            else:
                if docujson:
                    query = """ INSERT INTO documentos_electronicos (doel_idsysemisor, doel_documento, doel_estado, 
                                            doel_fechahora, doel_respuesta, doel_observacion)
                                VALUES (%s, %s, %s, TIMESTAMP %s, %s, %s);"""
                    data = (idsysemisor, docujson, estado, ahora, respuesta, observacion)
                    self.curs.execute(query, data)
                else:
                    msg = 'No existe ningun documento electrónico'

            self.disconnect()
            print(msg)

    def documentosFaltantes(self):
        if self.__connect:
            existe_sql = "SELECT * from documentos_electronicos WHERE doel_estado != 'C';"
            self.curs.execute(existe_sql)
            result = self.curs.fetchall()
            self.disconnect()
            return result