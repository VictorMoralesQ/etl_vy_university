import pandas as pd

from utils.utils import log_error

channel_type_map = {
    0: 'Default',
    1: 'Direct',
    2: 'Web',
    3: 'GDS',
    4: 'API',
    5: 'DigitalAPI',
    6: 'DigitalWeb',
    7: 'NDC'
}

def categorize_channel_type(df: pd.DataFrame, column: str):
    """
    Categoriza los valores de una columna en el DataFrame según un mapa predefinido.

    Esta función toma una columna de un DataFrame y mapea sus valores a nuevas categorías basadas
    en un diccionario predefinido (`channel_type_map`). Los valores de la columna se reemplazan con
    sus correspondientes valores mapeados y luego se convierten en tipo `str`.

    Args:
        df (pd.DataFrame): El DataFrame que contiene la columna que se desea categorizar.
        column (str): El nombre de la columna que contiene los valores a categorizar.

    Returns:
        pd.DataFrame: El DataFrame original con la columna actualizada con los valores categorizados.
    """
    if column not in df.columns:
        log_error(f"Error: La columna {column} no está presente en el DataFrame.")
        return df

    # Mapear los valores de 'ChannelType' a sus correspondientes valores numéricos
    df[column] = df[column].map(channel_type_map).astype(str)

    log_error(f"Categorías aplicadas correctamente a la columna {column}")
    return df