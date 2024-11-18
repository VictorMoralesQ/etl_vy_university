import pandas as pd
from utils.utils import log_error


key_attributes = {
    'booking_new': ['BookingID', 'BookingParentID', 'Status', 'RecordLocator'],
    'passenger_new': ['PassengerID', 'BookingID'],
    'leg': ['PassengerID', 'SegmentID', 'InventoryLegID'],
    'charge': ['PassengerID', 'SegmentID'],
    'segment': ['PassengerID', 'SegmentID']
}


def generate_business_key(df: pd.DataFrame, file_type: str):
    """
    Genera una columna `business_key` en el DataFrame concatenando los valores de las columnas clave
    especificadas para el tipo de archivo dado.

    La columna `business_key` es generada concatenando los valores de las columnas listadas en el diccionario
    `key_attributes` correspondiente al tipo de archivo proporcionado. Los valores se unen con un guion bajo ('_'),
    y los valores nulos en las columnas clave son reemplazados por el string 'NULL'.

    Args:
        df (pd.DataFrame): El DataFrame en el que se generará la columna `business_key`.
        file_type (str): El tipo de archivo que determina qué columnas deben ser usadas para generar el `business_key`.
                         Este tipo se usa para buscar en el diccionario `key_attributes` las columnas que se deben usar
                         para la concatenación.

    Returns:
        pd.DataFrame: El DataFrame con una nueva columna `business_key` generada.
    """
    if file_type not in key_attributes:
        log_error(f"Error: El tipo de archivo {file_type} no está en el diccionario key_attributes.")
        return df

    attributes = key_attributes[file_type]
    missing_columns = [col for col in attributes if col not in df.columns]
    if missing_columns:
        log_error(f"Error: Las siguientes columnas faltan en el DataFrame: {', '.join(missing_columns)}")
        return df

    # Crear la columna 'business_key' concatenando los valores de las columnas especificadas
    # Usando .agg() para eficiencia y manejar nulos
    df['business_key'] = df[attributes].agg(lambda x: '_'.join(x.fillna('NULL').astype(str)), axis=1)

    return df