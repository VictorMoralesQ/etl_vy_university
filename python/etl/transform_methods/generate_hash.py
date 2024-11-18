import os.path
import pandas as pd
import hashlib
from utils.utils import log_error, set_audit_columns
from dotenv import load_dotenv

load_dotenv()

EXTRACT_PATH = os.getenv("DESTINATION_PATH")


key_attributes = {
    'booking_new': ['BookingID', 'BookingParentID', 'Status', 'RecordLocator'],
    'passenger_new': ['PassengerID', 'BookingID'],
    'leg': ['PassengerID', 'SegmentID', 'InventoryLegID'],
    'charge': ['PassengerID', 'SegmentID'],
    'segment': ['PassengerID', 'SegmentID']
}

def generate_hash(df: pd.DataFrame, file_type: str):
    """
    Genera una columna `hash` en el DataFrame basada en un conjunto de columnas clave,
    concatenando los valores de esas columnas y calculando un hash MD5 para cada fila.

    La función utiliza las columnas clave definidas en el diccionario `key_attributes` para el tipo de archivo
    proporcionado. Los valores de estas columnas se concatenan en un solo string y se calcula un hash MD5 para cada fila.
    La columna `hash` resultante contiene los valores de hash generados para cada fila del DataFrame.

    Args:
        df (pd.DataFrame): El DataFrame en el que se generará la columna `hash`.
        file_type (str): El tipo de archivo que determina qué columnas deben ser usadas para calcular el hash.
                         Este tipo se utiliza para buscar en el diccionario `key_attributes` las columnas que se deben
                         usar para la concatenación y el cálculo del hash.

    Returns:
        pd.DataFrame: El DataFrame con una nueva columna `hash` generada.
    """
    if file_type not in key_attributes:
        log_error(f"Error: El tipo de archivo {file_type} no está en el diccionario key_attributes.")
        return df

    attributes = key_attributes[file_type]
    missing_columns = [col for col in attributes if col not in df.columns]

    def generate_row_hash(row):
        concatenated_values = '_'.join(str(row[missing_columns].fillna('NULL')))
        return hashlib.md5(concatenated_values.encode('utf-8')).hexdigest()

    df['hash'] = df.apply(generate_row_hash, axis=1)

    return df
