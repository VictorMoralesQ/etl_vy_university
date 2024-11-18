from etl.extract.extract_from_api import extract_from_api
from etl.extract.extract_from_csv import extract_from_csv
from etl.extract.extract_from_excel import extract_from_excel
from source_extractor import extract
from python.etl.transform import read_data, filter_data, clean_data, generate_business_key, generate_hash
import os
from dotenv import load_dotenv

load_dotenv()

def test_extract_from_api():
    if not os.getenv("API_URL") or not os.getenv("API_PORT"):
        print("Las variables de entorno API_URL o API_PORT no están configuradas.")
    else:
        # endpoint = "booking"
        endpoint = "booking"
        print(f"Extrayendo datos para el endpoint: {endpoint}")
        df_booking = extract_from_api(endpoint)

        if df_booking is not None:
            print("Datos extraídos correctamente para 'booking'.")
            print(df_booking.head())

        # endpoint = "booking/passenger"
        endpoint = "booking/passenger"
        print(f"Extrayendo datos para el endpoint: {endpoint}")
        df_passenger = extract_from_api(endpoint)

        if df_passenger is not None:
            print("Datos extraídos correctamente para 'booking/passenger'.")
            print(df_passenger.head())


def test_extract_from_csv_passenger_journey():
    file_path = os.getenv("PATH_CSV_LEG")
    df = extract_from_csv(file_path)
    if df is not None:
        print("Datos extraídos correctamente.")
        print(df.head())

def test_extract_from_csv_passenger_leg():
    file_path = os.getenv("PATH_CSV_LEG")
    df = extract_from_csv(file_path)
    if df is not None:
        print("Datos extraídos correctamente.")
        print(df.head())

def test_extract_from_excel():
    file_path = os.getenv("PATH_EXCEL")
    df = extract_from_excel(file_path)
    if df is not None:
        print("Datos extraídos correctamente.")
        print(df.head())

def test_read_data():
    file_path = os.getenv("SOURCE_PASSENGER")
    df = read_data(file_path)
    if df is not None:
        print("Datos extraídos correctamente.")
        print(df.head())
        return df

def test_clean_data():
    df = read_data(os.getenv("SOURCE_PASSENGER"))
    clean_data(df)
    if df is not None:
        print("Datos limpiados correctamente.")
        print(df.head())
        return df

def test_filter_data():
    df = read_data(os.getenv("SOURCE_PASSENGER"))
    filter_data(df, 'passenger')
    if df is not None:
        print("Datos transformados correctamente.")
        print(df.head())
        return df

def test_generate_business_key():
    df = read_data(os.getenv("SOURCE_PASSENGER"))
    generate_business_key(df, 'passenger')
    if df is not None:
        print("Clave de negocio generada correctamente.")
        print(df['business_key'].head())
        return df

def test_generate_hash():
    df = read_data(os.getenv("SOURCE_PASSENGER"))
    generate_hash(df, 'passenger')
    if df is not None:
        print("Encriptación de datos realizada correctamente.")
        print(df['hash'].head())
        return df


if __name__ == "__main__":
    print("Iniciando las pruebas de extracción de datos...")
    extract()