import pandas as pd
from utils.utils import log_error

currency_exchange_rate = {
    "GBP": 0.85,
    "CHF": 0.92,
    "CAD": 0.68,
    "DKK": 0.13,
    "EUR": 1.0,    # EUR siempre será 1
    "SEK": 0.087,
    "NOK": 0.09,
    "USD": 0.92
}


def convert_currency(df: pd.DataFrame, amount_column: str, currency_column: str, currency_exchange_rate: dict):
    """
    Convierte los valores monetarios en un DataFrame a EUR utilizando las tasas de cambio proporcionadas
    y actualiza la columna de moneda a 'EUR'.

    Esta función realiza las siguientes acciones:
    1. Verifica que las tasas de cambio para las monedas soportadas (GBP, CHF, CAD, DKK, EUR, SEK, NOK, USD) estén presentes en el diccionario `currency_exchange_rate`.
    2. Convierte los valores en la columna de monto (`amount_column`) a EUR utilizando las tasas de cambio correspondientes.
    3. Actualiza la columna de moneda (`currency_column`) a 'EUR' para todas las filas procesadas.

    Args:
        df (pd.DataFrame): El DataFrame que contiene los datos monetarios a convertir.
        amount_column (str): El nombre de la columna que contiene los valores monetarios a convertir.
        currency_column (str): El nombre de la columna que contiene las monedas de los valores monetarios.
        currency_exchange_rate (dict): Un diccionario con las tasas de cambio de las monedas soportadas hacia EUR.
            Ejemplo: {'USD': 0.85, 'GBP': 1.1, ...}

    Returns:
        pd.DataFrame: El DataFrame con los valores convertidos a EUR y la columna de moneda actualizada.
    """
    # Asegúrate de que las monedas y las columnas sean correctas
    supported_currencies = ['GBP', 'CHF', 'CAD', 'DKK', 'EUR', 'SEK', 'NOK', 'USD']

    # Verifica que las tasas de cambio estén disponibles para las monedas soportadas
    if not all(currency in currency_exchange_rate for currency in supported_currencies):
        log_error("Error: Faltan tasas de cambio para algunas de las monedas soportadas.")
        return df

    # Realizar la conversión en las columnas ForeignAmount y ForeignCurrencyCode
    if amount_column in df.columns and currency_column in df.columns:
        # Convertir los valores de ForeignAmount según la tasa de cambio
        df[amount_column] = df.apply(
            lambda row: convert_amount_to_eur(row, amount_column, currency_column, currency_exchange_rate), axis=1)

        # Cambiar el valor en la columna ForeignCurrencyCode a EUR después de la conversión
        df[currency_column] = 'EUR'

    return df


def convert_amount_to_eur(row, amount_column, currency_column, currency_exchange_rate):
    """
    Convierte una cantidad de una moneda a EUR utilizando la tasa de cambio proporcionada.

    Esta función toma una fila del DataFrame, obtiene la cantidad de dinero en la moneda indicada y la convierte a EUR
    utilizando la tasa de cambio correspondiente del diccionario `currency_exchange_rate`.

    Args:
        row (pd.Series): Una fila del DataFrame.
        amount_column (str): El nombre de la columna que contiene el monto a convertir.
        currency_column (str): El nombre de la columna que contiene la moneda del monto.
        currency_exchange_rate (dict): Un diccionario con las tasas de cambio de las monedas soportadas hacia EUR.

    Returns:
        float: El monto convertido a EUR si la moneda no es EUR; el valor original si ya está en EUR o no tiene tasa de cambio disponible.
    """
    from_currency = row[currency_column]
    amount = row[amount_column]

    # Si la moneda no es EUR y está en el diccionario de tasas de cambio, conviértela
    if from_currency != 'EUR' and from_currency in currency_exchange_rate:
        conversion_rate = currency_exchange_rate[from_currency]
        return round(amount * conversion_rate, 2)
    else:
        return amount