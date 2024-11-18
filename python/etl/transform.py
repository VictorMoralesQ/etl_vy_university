import os.path
from datetime import datetime
import threading
from etl.transform_methods.read_data import read_data
from etl.transform_methods.clean_data import clean_data
from etl.transform_methods.filter_data import filter_data
from etl.transform_methods.transform_all_sources import transform_all_sources
from etl.transform_methods.generate_business_key import generate_business_key
from etl.transform_methods.generate_hash import generate_hash
from utils.utils import set_audit_columns
from dotenv import load_dotenv

from utils.utils import log_error

load_dotenv()

EXTRACT_PATH = os.getenv("DESTINATION_PATH")
TRANSFORM_PATH = os.getenv("TRANSFORMED_PATH")


transform_sources = {
    "Booking": {
        "source": os.getenv('SOURCE_BOOKING_NEW'),
        "file_type": os.getenv('FILETYPE_BOOKING')
    },
    "BookingPassenger": {
        "source": os.getenv('SOURCE_PASSENGER_NEW'),
        "file_type": os.getenv('FILETYPE_PASSENGER')
    },
    "PassengerJourneySegment": {
        "source": os.getenv('SOURCE_SEGMENT'),
        "file_type": os.getenv('FILETYPE_SEGMENT')
    },
    "PassengerJourneyLeg": {
        "source": os.getenv('SOURCE_LEG'),
        "file_type": os.getenv('FILETYPE_LEG')
    },
    "PassengerJourneyCharge": {
        "source": os.getenv('SOURCE_CHARGE'),
        "file_type": os.getenv('FILETYPE_CHARGE')
    }
}
log_error(transform_sources.values())

def transform_source(source, info, results):
    """
     Realiza la transformación de una fuente de datos y almacena el resultado en el diccionario `results`.

    Esta función toma una fuente de datos, lee los datos desde el archivo correspondiente, los limpia,
    los filtra, aplica las transformaciones necesarias y genera las columnas de auditoría. También calcula
    el `business_key` y el `hash` para los datos transformados, y luego almacena el estado de la transformación
    en el diccionario `results`.

    Args:
        source (str): El nombre de la fuente de datos que está siendo transformada.
        info (dict): Un diccionario que contiene la información necesaria para procesar la fuente,
                     como la ruta del archivo y el tipo de archivo.
        results (dict): Un diccionario para almacenar el estado de la transformación para cada fuente.

    Returns:
        None: La función no retorna un valor. El estado de la transformación se almacena en el diccionario `results`.
    """
    try:
        df = read_data(info['source'])
        df_cleaned = clean_data(df)
        df_filtered = filter_data(df_cleaned, info['file_type'])
        df_transformed = transform_all_sources(df_filtered, info['file_type'])

        df_business_key = generate_business_key(df_transformed, info['file_type'])
        df_hash = generate_hash(df_business_key, info['file_type'])

        # Agregar las columnas de auditoría
        extract_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        set_audit_columns(df_hash, source, extract_date, 'transformed', TRANSFORM_PATH)
        results[source] = "Transformación completa"
        log_error(f"Transformación completa para {source}")

    except Exception as e:
        results[source] = f"Error: {str(e)}"
        log_error(f"Error al transformar {source}: {str(e)}")

def transform():
    """
    Realiza la transformación de todas las fuentes de datos de manera paralela usando hilos.

    Esta función coordina la transformación de varias fuentes de datos en paralelo. Para cada fuente, se
    crea un hilo que ejecuta la función `transform_source`. Al final, la función espera que todos los hilos
    terminen y luego imprime los resultados de la transformación para cada fuente.

    El diccionario `results` se usa para almacenar el estado de la transformación de cada fuente de datos.

    Returns:
        None: La función no retorna un valor. Los resultados de la transformación se imprimen al final.
    """
    log_error("Transformando los datos...")

    # Diccionario para almacenar los resultados de los hilos
    results = {}

    # Lista de hilos
    threads = []

    # Se crea un hilo para cada fuente de datos
    for source, info in transform_sources.items():
        thread = threading.Thread(target=transform_source, args=(source, info, results))
        threads.append(thread)
        thread.start()

    # Se espera a que todos los hilos terminen
    for thread in threads:
        thread.join()

    # Se procesan los resultados
    for source, result in results.items():
        log_error(f"{source}: {result}")

    log_error("Transformación completada para todas las fuentes.")