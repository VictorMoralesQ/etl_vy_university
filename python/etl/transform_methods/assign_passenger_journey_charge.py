import pandas as pd

def assign_passenger_journey_charge(df: pd.DataFrame, charge_column: str) -> pd.DataFrame:
    """
    Asigna un valor a la columna 'PassengerJourneyCharge' basado en los valores de una columna de cargos.

    Esta función agrega una nueva columna al DataFrame, llamada 'PassengerJourneyCharge'.
    Los valores de esta columna son determinados por los valores de la columna indicada por `charge_column`.
    Si el valor en `charge_column` es mayor que 0, se asigna 'Charged', de lo contrario se asigna 'Not Charged'.

    Args:
        df (pd.DataFrame): El DataFrame al que se le añadirá la nueva columna 'PassengerJourneyCharge'.
        charge_column (str): El nombre de la columna en el DataFrame que contiene los valores de los cargos.

    Returns:
        pd.DataFrame: El DataFrame modificado con la nueva columna 'PassengerJourneyCharge'.
    """
    if charge_column in df.columns:
        df['PassengerJourneyCharge'] = df[charge_column].apply(lambda x: 'Charged' if x > 0 else 'Not Charged')
    return df