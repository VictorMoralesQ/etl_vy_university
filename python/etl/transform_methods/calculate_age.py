import numpy as np
import pandas as pd

from utils.utils import log_error


def calculate_age(df: pd.DataFrame, dob_column: str):
    """
    Calcula la edad y si la persona es adulta (mayor o igual a 18 años) a partir de una columna de fechas de nacimiento.

    Esta función toma una columna de fechas de nacimiento (DOB), calcula la edad en base al año actual y asigna
    el valor correspondiente a la nueva columna 'age'. También asigna un valor booleano a la columna 'IsAdult',
    indicando si la persona es adulta (mayor o igual a 18 años).

    Args:
        df (pd.DataFrame): El DataFrame que contiene la columna de fechas de nacimiento.
        dob_column (str): El nombre de la columna en el DataFrame que contiene las fechas de nacimiento.

    Returns:
        pd.DataFrame: El DataFrame original con las columnas 'age' e 'IsAdult' añadidas. La columna 'age' contiene
                       la edad calculada y 'IsAdult' es un valor booleano que indica si la persona es adulta.
    """
    if dob_column not in df.columns:
        log_error(f"Error: La columna {dob_column} no está en el DataFrame.")
        return df

    # Obtener el año actual
    current_year = pd.to_datetime("today").year

    df['age'] = np.nan
    df['IsAdult'] = False

    for index, row in df.iterrows():
        dob = row[dob_column]

        if dob == '9999-12-31':
            df.at[index, 'age'] = np.nan
            df.at[index, 'IsAdult'] = False
        else:
            try:
                birth_year = int(dob[:4])  # Tomar solo los primeros 4 caracteres (año)

                if birth_year != 9999:
                    age = current_year - birth_year
                    df.at[index, 'age'] = int(age)

                    if df.at[index, 'age'] >= 18:
                        df.at[index, 'IsAdult'] = True
                    else:
                        df.at[index, 'IsAdult'] = False
            except Exception as e:
                log_error(f"Error al procesar el valor {dob} en la fila {index}: {e}")

    df['IsAdult'] = df['IsAdult'].astype(bool)
    df['age'] = pd.to_numeric(df['age'], errors='coerce', downcast='integer')

    return df
