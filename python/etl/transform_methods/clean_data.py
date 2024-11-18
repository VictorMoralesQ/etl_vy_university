import os.path
import pandas as pd
import numpy as np
from dotenv import load_dotenv

from utils.utils import log_error

load_dotenv()

EXTRACT_PATH = os.getenv("DESTINATION_PATH")

def clean_data(df: pd.DataFrame):
    """
    Limpia los datos de un DataFrame, eliminando filas con todos los valores nulos,
    imputando valores nulos en columnas numéricas con la media y limpiando espacios
    en blanco en columnas de tipo cadena.

    Esta función realiza una serie de operaciones de limpieza de datos sobre un DataFrame:
    1. Elimina las filas que contienen únicamente valores nulos.
    2. Elimina los espacios en blanco al inicio y al final en las columnas de tipo cadena.
    3. Imputa los valores nulos en las columnas numéricas con la media de la columna.

    Args:
        df (pd.DataFrame): El DataFrame que contiene los datos a limpiar.

    Returns:
        pd.DataFrame: El DataFrame después de haber sido limpiado.
    """
    log_error("Valores nulos por columna antes de la limpieza:")
    log_error(df.isnull().sum())

    # Eliminar filas con todos los valores nulos
    df = df.dropna(axis=0, how='all')

    str_cols = df.select_dtypes(include=[object]).columns
    for col in str_cols:
        df[col] = df[col].str.strip()

    # Imputación de valores nulos numéricos con la media
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        df[col] = df[col].fillna(df[col].mean())

    # Mostrar los valores nulos por columna después de la limpieza
    log_error("\nValores nulos por columna después de la limpieza:")
    log_error(df.isnull().sum())

    return df