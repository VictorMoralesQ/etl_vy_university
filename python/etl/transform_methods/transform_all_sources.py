import os
from dotenv import load_dotenv
import pandas as pd
from etl.transform_methods.convert_currency import convert_currency
from etl.transform_methods.calculate_age import calculate_age
from etl.transform_methods.calculate_time_to_modify import calculate_time_to_modify
from etl.transform_methods.assign_passenger_journey_charge import assign_passenger_journey_charge
from etl.transform_methods.convert_currency import currency_exchange_rate
from etl.transform_methods.categorize_channel_type import categorize_channel_type

load_dotenv()


def transform_all_sources(df: pd.DataFrame, file_type: str):
    """
    Aplica una serie de transformaciones a un DataFrame según el tipo de archivo especificado.

    Esta función evalúa el tipo de archivo y, en función de ello, aplica las transformaciones necesarias
    sobre las columnas del DataFrame. Las transformaciones incluyen conversión de divisas, cálculo de la
    edad de los pasajeros, cálculo del tiempo de modificación de los registros, categorización de tipos
    de canales y asignación de cargos a los pasajeros.

    Args:
        df (pd.DataFrame): El DataFrame que contiene los datos a transformar.
        file_type (str): El tipo de archivo que determina qué transformaciones se deben aplicar.
                          Este parámetro es usado para aplicar diferentes transformaciones dependiendo
                          del tipo de archivo (por ejemplo, 'charge', 'passenger', 'segment').

    Returns:
        pd.DataFrame: El DataFrame transformado con las modificaciones correspondientes.
    """
    if file_type == 'charge' and 'ForeignAmount' in df.columns and 'ForeignCurrencyCode' in df.columns and 'CurrencyCode' in df.columns and 'ChargeAmount' in df.columns:
        df = convert_currency(df, 'ForeignAmount', 'ForeignCurrencyCode', currency_exchange_rate)

    if file_type == 'passenger' or file_type == 'passenger_new' and 'DOB' in df.columns:
        df = calculate_age(df, 'DOB')

    if 'CreatedDate' in df.columns and 'ModifiedDate' in df.columns:
        df = calculate_time_to_modify(df, 'CreatedDate', 'ModifiedDate')

    if file_type == 'charge' and 'ChargeAmount' in df.columns:
        df = assign_passenger_journey_charge(df, 'ChargeAmount')

    if file_type == 'segment' and 'ChannelType' in df.columns:
        df = categorize_channel_type(df, 'ChannelType')

    return df