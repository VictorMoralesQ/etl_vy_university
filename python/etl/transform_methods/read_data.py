import os.path
import pandas as pd
from dotenv import load_dotenv

from utils.utils import log_error

load_dotenv()

EXTRACT_PATH = os.getenv("DESTINATION_PATH")

def read_data(filename:str):
    """
    Lee los datos de un archivo CSV o Excel desde una ruta predefinida y devuelve un DataFrame.

    La función intenta leer el archivo especificado por el parámetro `filename`. Si el archivo tiene la extensión
    `.csv`, se asume que es un archivo CSV y se lee utilizando el separador de pipe (`'|'`). Si el archivo tiene la
    extensión `.xlsx`, se asume que es un archivo Excel y se lee con el encabezado en la primera fila. Si el archivo
    no tiene una extensión válida, se genera una excepción.

    Args:
        filename (str): El nombre del archivo a leer. El archivo debe estar ubicado en el directorio definido por
                         `EXTRACT_PATH`.

    Returns:
        pd.DataFrame: El DataFrame que contiene los datos leídos desde el archivo.
    """
    file_path = os.path.join(EXTRACT_PATH, filename)
    if filename.endswith('.csv'):
        df = pd.read_csv(file_path, sep='|', header=0)
        log_error(df.dtypes)
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(file_path, sep='|', header=0)
        log_error(df.dtypes)
    else:
        raise ValueError(f"Error: El archivo {filename} no es un archivo CSV o Excel.")

    log_error(f"Datos leídos correctamente desde {file_path}")
    return df