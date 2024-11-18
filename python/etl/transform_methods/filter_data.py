import pandas as pd
import os.path
from utils.utils import log_error
import json
from dotenv import load_dotenv

load_dotenv()

EXTRACT_PATH = os.getenv("DESTINATION_PATH")

dtypes_dict = {
    'booking_new': {
        'ExpiredDate': 'datetime64',
        'BookingDate': 'datetime64',
        'CreatedDate': 'datetime64',
        'ModifiedDate': 'datetime64',
        'extract_dt': 'datetime64',
    },
    'passenger_new': {
        'CreatedDate': 'datetime64',
        'ModifiedDate': 'datetime64',
        'extract_dt': 'datetime64',

    },
    'leg': {
        'CreatedDate': 'datetime64',
        'ModifiedDate': 'datetime64',
        'extract_dt': 'datetime64',
    },
    'charge': {
        'ChargeDateTime': 'datetime64',
        'CreatedDate': 'datetime64',
        'extract_dt': 'datetime64',
    },
    'segment': {
        'DepartureDate': 'datetime64',
        'SalesDate': 'datetime64',
        'ActivityDate': 'datetime64',
        'CreatedDate': 'datetime64',
        'ModifiedDate': 'datetime64',
        'extract_dt': 'datetime64',
    }
}

conversion_dict = {
    'booking_new': {},
    'passenger_new': {
        'ProgramNumber': 'string[python]',
        'CustomerNumber': 'string[python]',
        'DOB': 'string[python]',
        'Infant': 'int64',
    },
    'leg': {},
    'charge': {},
    'segment': {},
}


def filter_data(df: pd.DataFrame, file_type: str):
    """
    Filtra y convierte las columnas de un DataFrame según su tipo de archivo, utilizando los diccionarios de
    tipos de datos (`dtypes_dict`) y conversiones (`conversion_dict`) definidos previamente.

    Esta función realiza las siguientes acciones:
    1. Convierte las columnas de fechas en el DataFrame a formato `datetime64[ns]`, según el tipo de archivo,
       y las redondea a la precisión de segundos.
    2. Convierte las columnas especificadas a los tipos de datos deseados, como `float`, `int`, `string`, etc.
    3. Para las columnas que no se especifican en los diccionarios de conversiones, se verifican si son de tipo
       adecuado y se ajustan, si es necesario, a `string` o se mantienen en su tipo original.
    4. Si una columna no puede ser convertida a su tipo correspondiente, se registra un error y se retorna el DataFrame sin cambios.

    Args:
        df (pd.DataFrame): El DataFrame que contiene los datos a filtrar y convertir.
        file_type (str): El tipo de archivo que se está procesando, que determina qué columnas deben ser convertidas
                         y cómo se deben filtrar. Este tipo se utiliza para buscar en los diccionarios `dtypes_dict`
                         y `conversion_dict`.

    Returns:
        pd.DataFrame: El DataFrame con las columnas convertidas y filtradas según el tipo de archivo.
    """
    if file_type not in dtypes_dict:
        log_error(f"Error: El tipo de archivo {file_type} no está en el diccionario dtypes_dict.")
        return df

    date_columns = dtypes_dict[file_type]

    for column, dtype in date_columns.items():
        if column in df.columns:
            try:
                df[column] = pd.to_datetime(df[column], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
                df[column] = df[column].dt.floor('s')  # Elimina milisegundos

                if df[column].isnull().any():
                    log_error(f"Error: La columna {column} no se pudo convertir a datetime.")

                log_error(f"Columna {column} convertida correctamente a datetime.")

            except Exception as e:
                log_error(f"Error al convertir la columna {column} a datetime: {e}")

    if file_type not in conversion_dict:
        log_error(f"Error: El tipo de archivo {file_type} no está en el diccionario conversion_dict.")
        return df

    conversion_types = conversion_dict[file_type]

    for column, target_dtype in conversion_types.items():
        if column in df.columns:
            try:
                df[column] = df[column].astype(target_dtype)
            except Exception as e:
                log_error(f"Error: No se pudo convertir la columna {column} a {target_dtype}. Error: {e}")

    for column in df.columns:
        if column in date_columns:
            df[column] = df[column].astype('datetime64[ns]')
        elif column not in conversion_types and column not in date_columns:
            if df[column].dtype == 'object':
                df[column] = df[column].astype('string')
            elif df[column].dtype in ['float64', 'int64', 'bool']:
                pass
            else:
                log_error(f"Error: La columna {column} no es de tipo numérico ni objeto.")

    log_error(df.dtypes)
    log_error(f"Datos filtrados correctamente para el tipo de archivo {file_type}")
    return df