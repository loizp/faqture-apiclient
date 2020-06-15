import sys
sys.stdout.encoding
'UTF-8'
import psycopg2
from select import select
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .DataProperty import ConfigThreadsApi
from .SourcesDBconnect import SourceDBemisor

class PgQueueComercial:
    conn = None
    channel = None

    undsunat_sql = """  DROP SEQUENCE IF EXISTS {0}.unidades_sunat_umsu_id_seq CASCADE;
                    \n  CREATE SEQUENCE {0}.unidades_sunat_umsu_id_seq;
                    \n
                    \n  DROP TABLE IF EXISTS {0}.unidades_sunat;
                    \n  CREATE TABLE {0}.unidades_sunat (
                    \n          umsu_id INTEGER NOT NULL DEFAULT nextval('{0}.unidades_sunat_umsu_id_seq'),
                    \n          umsu_codigo_actual VARCHAR(10) NOT NULL,
                    \n          umsu_codigo_sunat VARCHAR(10) NOT NULL,
                    \n          CONSTRAINT unidades_sunat_pk PRIMARY KEY (umsu_id)
                    \n  );
                    \n  COMMENT ON TABLE {0}.unidades_sunat IS 'para hacer un parser de las unidades que manejan los sistemas hacia los de la sunat';
                    \n  COMMENT ON COLUMN {0}.unidades_sunat.umsu_id IS 'Campo PK autoincremental';
                    \n  COMMENT ON COLUMN {0}.unidades_sunat.umsu_codigo_actual IS 'Campo con los códigos de identificación de la unidades en el sistema actual';
                    \n  COMMENT ON COLUMN {0}.unidades_sunat.umsu_codigo_sunat IS 'campo con los codigo admitidos en sunat';
                    \n
                    \n  ALTER SEQUENCE {0}.unidades_sunat_umsu_id_seq OWNED BY {0}.unidades_sunat.umsu_id;""".format(SourceDBemisor().getSchema())

    insertus_sql = """  INSERT INTO {0}.unidades_sunat (umsu_codigo_actual, umsu_codigo_sunat)
                    \n  VALUES  ('U001', 'NIU'),('U002', 'DZN'),('U003', 'PR'),('U004', 'PK'),
                    \n      ('U005', 'BX'),('U006', 'CEN'),('U007', 'PK'),('U008', 'MIL'),
                    \n      ('U009', 'CH'),('U010', 'PK'),('U011', 'BL'),('U012', 'D64'),
                    \n      ('U013', 'CS'),('U014', 'RM'),('U015', 'D63'),('U016', 'CS'),
                    \n      ('U017', 'MTR'),('U018', 'ST'),('U019', 'RO'),('U020', 'BX'),
                    \n      ('U021', 'PK'),('U022', 'PG'),('U023', 'CS'),('U024', 'MIL'),
                    \n      ('U025', 'CS'),('U026', 'CJ'),('U027', 'D63'),('U028', 'PK'),
                    \n      ('U029', 'BL'),('U030', 'PK'),('U31', 'PK');""".format(SourceDBemisor().getSchema())

    funcion_sql = """CREATE OR REPLACE FUNCTION {0}.notifica_insert_data() RETURNS TRIGGER AS $check_insert_fe$
                   \n   DECLARE
                   \n       payload TEXT;                                                               
                   \n       rec RECORD;
                   \n
                   \n   BEGIN
                   \n       CASE TG_OP
                   \n           WHEN 'INSERT' THEN
				   \n               rec := NEW;
                   \n           WHEN 'UPDATE' THEN
				   \n               rec := OLD;
			       \n           ELSE
				   \n               RAISE EXCEPTION 'Unknown TG_OP: "%". Should occur!', TG_OP;
		           \n       END CASE;
		           \n                                                                                   
                   \n       payload = ( SELECT row_to_json(cp)
                   \n                   FROM (
                   \n                       SELECT  NEW.id_venta                                                            AS docu_idkenaani,
                   \n                               docu.fecha_hora                                                         AS docu_fechaemision,
                   \n                               tido.codigo_sunat                                                       AS tido_codigo,
                   \n                               docu.num_serie || '-' || docu.num_documento                             AS docu_numero,
                   \n                               CASE docu.id_moneda
                   \n                                   WHEN 2 THEN 'USD'
                   \n                                   ELSE 'PEN'
                   \n                               END                                                                     AS mone_codigo,
                   \n                               docu.observaciones                                                      AS docu_observacion,
                   \n                               clie.nombres_cliente                                                    AS clie_nombrelegal,
                   \n                               cdir.direccion                                                          AS clie_direccion,
                   \n                               CASE
                   \n                                   WHEN clie.dni NOTNULL AND TRIM(clie.dni) != '' THEN TRIM(clie.dni)
                   \n                                   WHEN clie.ruc NOTNULL AND TRIM(clie.ruc) != '' THEN TRIM(clie.ruc)
                   \n                                   ELSE NULL
                   \n                               END                                                                     AS clie_numerodocumento,
                   \n                               CASE
                   \n                                   WHEN clie.dni NOTNULL AND TRIM(clie.dni) != '' THEN '1'
                   \n                                   WHEN clie.ruc NOTNULL AND TRIM(clie.ruc) != '' THEN '6'
                   \n                                   ELSE '0'
                   \n                               END                                                                     AS tidi_codigo,
                   \n                               ubig.cod_dpto || ubig.cod_prov || ubig.cod_dist                         AS ubig_codigo,
                   \n                               CASE NEW.codigo_cliente
                   \n                                   WHEN 'ANULADO' THEN True
                   \n                                   ELSE False
                   \n                               END                                                                     AS docu_anulado,
                   \n                               docu.taza_igv                                                           AS docu_tasaigv,
                   \n                               docu.monto_venta                                                        AS docu_subtotal,
                   \n                               docu.igv                                                                AS docu_igv,
                   \n                               docu.descuento                                                          AS docu_descuento,
                   \n                               docu.monto_efectivo                                                     AS docu_total,
                   \n                               docu.cod_empleado                                                       AS docu_vendedor,
                   \n                               (
                   \n                               SELECT array_to_json(array_agg(row_to_json(dcp)))
                   \n                               FROM (
                   \n                                   SELECT  ROW_NUMBER()
                   \n                                               OVER (PARTITION BY docu.id_venta ORDER BY dedo.id_detalle_venta)    AS dedo_orden,
                   \n                                           dedo.cantidad                                                           AS dedo_cantidad,
                   \n                                           unsu.umsu_codigo_sunat                                                  AS unme_codigo,
                   \n                                           dedo.codigo_producto                                                    AS dedo_codigoproducto,
                   \n                                           dedo.descripcion                                                        AS dedo_descripcion,
                   \n                                           dedo.monto                                                              AS dedo_precioventa,
                   \n                                           dedo.descuento_total + dedo.descuento_individual                        AS dedo_descuento,
                   \n                                           dedo.monto_total                                                        AS dedo_subtotal
                   \n                                   FROM {0}.detalle_venta AS dedo
                   \n                                       INNER JOIN {0}.unidades_sunat AS unsu ON unsu.umsu_codigo_actual = dedo.cod_unidad_medida
                   \n                                   WHERE dedo.id_venta = docu.id_venta
                   \n                                   ORDER BY docu.id_venta, dedo.id_detalle_venta
                   \n                               ) dcp )                                                                 AS docu_detalles
                   \n                       FROM {0}.ventas AS docu
                   \n                           INNER JOIN {0}.tipodocumento AS tido ON tido.id_tipodocumento = docu.id_tipodocumento
                   \n                           INNER JOIN {0}.cliente AS clie ON clie.codigo_cliente = rec.codigo_cliente
                   \n                           LEFT JOIN {0}.direcciones AS cdir ON cdir.id_direcciones = docu.id_direcciones
                   \n                           LEFT JOIN {0}.ubigeo AS ubig ON ubig.id_ubigeo = cdir.id_ubigeo
                   \n                       WHERE docu.id_venta = NEW.id_venta
                   \n                   ) cp );
                   \n
                   \n       PERFORM pg_notify('data', payload);
                   \n       RETURN NEW;
                   \n   END;
                   \n$check_insert_fe$ LANGUAGE plpgsql;""".format(SourceDBemisor().getSchema())

    trigger_sql = """DROP TRIGGER IF EXISTS check_insert_fe ON {0}.ventas;
                     CREATE TRIGGER check_insert_fe
                   \n   BEFORE INSERT OR UPDATE ON {0}.ventas
                   \n   FOR EACH ROW
                   \n   EXECUTE PROCEDURE {0}.notifica_insert_data();""".format(SourceDBemisor().getSchema())

    def __init__(self, channel):
        self.dataBaseConnection()
        self.creaUnidadesSunat()
        self.channel = channel
        self.__listening = ConfigThreadsApi().stopListen()

        if not channel:
            raise Exception('No existe un canal de escucha')

        self.addNotify()

    def dataBaseConnection(self):
        try:
            self.conn = psycopg2.connect(SourceDBemisor().getDataSourceConnection())
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.curs = self.conn.cursor()
            print('Conectado a la Base de Datos del Emisor')
        except:
            print('Ocurrió un error al conectar a la Base de Datos del Emisor')

    def creaUnidadesSunat(self):
        self.curs.execute(self.undsunat_sql)
        self.curs.execute(self.insertus_sql)
        print("Se creó la tabla unidades_sunat con sus respectivos datos para matching")

    def addNotify(self):
        self.curs.execute(self.funcion_sql)
        self.curs.execute(self.trigger_sql)
        print("Se creó el emitidor de notificaciones en el canal: data")

    def addListen(self):
        self.curs.execute("LISTEN {0};".format(self.channel))
        print("Se inició a escuchar en el canal: {0}".format(self.channel))

    def removeListen(self):
        self.curs.execute("UNLISTEN {0};".format(self.channel))
        print("Se dejó de escuchar en el canal: {0}".format(self.channel))

    def recvLoop(self):
        self.addListen()
        conn = self.conn
        while self.__listening:
            if select([conn],[],[],30) == ([],[],[]):
                self.__listening = not ConfigThreadsApi().stopListen()
                print ("Esperando notificación despues de tiempo en el canal: {0}".format(self.channel))
            else:
                conn.poll()
                while conn.notifies:
                    notif = conn.notifies.pop(0)
                    self.recvCallback(notif)

    def stop(self):
        self.__listening = False
        ConfigThreadsApi().setStopListen(True)

    def cerrarConect(self):
        self.curs.close()
        self.conn.close()

    def start(self):
        if not self.__listening:
            self.__listening = True
            ConfigThreadsApi().setListening(True)
            self.recvLoop()

    def recvCallback(self, notification):
        pass