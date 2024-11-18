import pandas as pd

def calculate_time_to_modify(df: pd.DataFrame, created_column: str, modified_column: str):
    """
    Calcula el tiempo transcurrido entre las fechas de creación y modificación de cada registro en un DataFrame.

    Esta función toma dos columnas de fechas (creación y modificación) en un DataFrame y calcula la diferencia
    entre las fechas en términos de tiempo (en formato `timedelta`). El resultado se guarda en una nueva columna
    llamada 'TimeToModify'.

    Args:
        df (pd.DataFrame): El DataFrame que contiene las columnas de fechas de creación y modificación.
        created_column (str): El nombre de la columna que contiene la fecha de creación.
        modified_column (str): El nombre de la columna que contiene la fecha de modificación.

    Returns:
        pd.DataFrame: El DataFrame original con la nueva columna 'TimeToModify', que contiene la diferencia
                       de tiempo entre la fecha de modificación y la fecha de creación para cada registro.
    """
    if 'CreatedDate' in df.columns:
        df['CreatedDate'] = pd.to_datetime(df[created_column], errors='coerce')
    if 'ModifiedDate' in df.columns:
        df['ModifiedDate'] = pd.to_datetime(df[modified_column], errors='coerce')

    df['TimeToModify'] = (df[modified_column] - df[created_column])

    return df