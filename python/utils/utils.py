from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import logging
import os.path
FILE_NAME = os.getenv("LOG_FILE_NAME")
DESTINATION_PATH = os.path.join(os.getenv('DESTINATION_PATH'))

logging.basicConfig(
    filename=FILE_NAME,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()

def log_error(message:str):
    """
    Función para registrar un mensaje de error en el log y escribirlo en un archivo si es necesario.

    Parameters:
    - message: El mensaje de error a registrar.
    """
    logging.error(message)
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'w') as f:
            f.write(message)


def set_audit_columns(df:pd.DataFrame,source:str,extract_date, proc_type:str, path:str):
    """
    Función para agregar columnas de auditoría al DataFrame y guardar el archivo resultante.

    Parameters:
    - df: DataFrame con los datos procesados.
    - source: Fuente de los datos.
    - extract_date: Fecha de extracción de los datos.
    - proc_type: Tipo de procesamiento (ej. 'full' o 'incremental').
    - path: Ruta donde se guardará el archivo procesado.

    Returns:
    - df: El DataFrame actualizado con las columnas de auditoría, o None si ocurre un error.
    """
    try:
        df['extract_dt'] = pd.to_datetime(extract_date, format="%Y-%m-%d %H:%M:%S")
        df['source'] = str(source)
        df['proc_status'] = str(proc_type)

        timestamp = datetime.now().strftime("%Y%m%d")
        new_file_name = f'{source}_{timestamp}_{proc_type}.csv'
        new_file_path = os.path.join(path, new_file_name)

        df.to_csv(new_file_path, sep='|', index=False)

        log_error(f"Archivo procesado y guardado en: {new_file_path}")
        log_error(df.dtypes)
        return df

    except Exception as e:
        log_error(f"Error al agregar columnas de auditoría o guardar el archivo: {e}")
        return None