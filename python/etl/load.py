# importa tus cosas aqui
from dotenv import load_dotenv

from utils.utils import log_error
from query.PostgreSQL.DBPostgresConn import dbpostgresconn

def load():
    """
    Carga los datos en la base de datos PostgreSQL.

    Este proceso realiza lo siguiente:
    1. Carga las variables de entorno desde el archivo .env.
    2. Establece una conexión con la base de datos PostgreSQL.
    3. Crea las tablas necesarias en la base de datos.
    4. Inserta los datos en las tablas de acuerdo con el tipo de carga (full o incremental).

    Si ocurre un error durante cualquiera de estos pasos, se registra en los logs.
    """
    try:
        load_dotenv()
        db_conn = dbpostgresconn()
        db_conn.create_tables_from_sql()
        db_conn.insert_all_data()

    except Exception as e:
        log_error(f"Error al cargar los datos: {e}")
        raise
