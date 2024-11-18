# IMPORTS
import os.path
import threading
from datetime import datetime
from dotenv import load_dotenv
from etl.source_extractor.extract_from_api import extract_from_api
from etl.source_extractor.extract_from_csv import extract_from_csv
from etl.source_extractor.extract_from_excel import extract_from_excel
from utils.utils import set_audit_columns

from utils.utils import log_error

load_dotenv()
DESTINATION_PATH = os.getenv("DESTINATION_PATH")
API_URL = f'http://{os.getenv("API_URL")}:{os.getenv("API_PORT")}'

#Función para extraer datos de Booking
def extract_booking(extract_date):
    log_error("Extrayendo data de Booking...")
    df_booking = extract_from_api("booking/new")
    if df_booking is not None:
        set_audit_columns(df_booking, "Booking", extract_date, "extracted", DESTINATION_PATH)



#Función para extraer datos de BookingPassenger
def extract_booking_passenger(extract_date):
    log_error("Extrayendo data de BookingPassenger...")
    df_passenger = extract_from_api("booking/passenger/new")
    if df_passenger is not None:
        set_audit_columns(df_passenger, "BookingPassenger", extract_date, "extracted", DESTINATION_PATH)

# Función para extraer datos de PassengerJourneySegment
def extract_passenger_journey_segment(extract_date):
    log_error("Extrayendo data de PassengerJourneySegment...")
    df_segment = extract_from_excel(os.getenv("PATH_EXCEL"))
    if df_segment is not None:
        set_audit_columns(df_segment, "PassengerJourneySegment", extract_date, "extracted", DESTINATION_PATH)


# Función para extraer datos de PassengerJourneyLeg
def extract_passenger_journey_leg(extract_date):
    log_error("Extrayendo data de PassengerJourneyLeg...")
    df_leg = extract_from_csv(os.getenv("PATH_CSV_LEG"))
    if df_leg is not None:
        set_audit_columns(df_leg, "PassengerJourneyLeg", extract_date, "extracted", DESTINATION_PATH)


# Función para extraer datos de PassengerJourneyCharge
def extract_passenger_journey_charge(extract_date):
    log_error("Extrayendo data de PassengerJourneyCharge...")
    df_charge = extract_from_csv(os.getenv("PATH_CSV_CHARGE"))
    if df_charge is not None:
        set_audit_columns(df_charge, "PassengerJourneyCharge", extract_date, "extracted", DESTINATION_PATH)


def extract():
    """
    Realiza la extracción de datos desde diversas fuentes de manera concurrente utilizando hilos.

    Esta función coordina la extracción de datos de varias fuentes: `Booking`, `BookingPassenger`,
    `PassengerJourneySegment`, `PassengerJourneyLeg`, y `PassengerJourneyCharge`, utilizando hilos
    para que todas las extracciones se realicen en paralelo, mejorando la eficiencia y reduciendo el tiempo
    de ejecución total.

    Para cada fuente de datos, se llama a la función correspondiente de extracción (`extract_booking`,
    `extract_booking_passenger`, etc.), se le asigna una fecha de extracción (`extract_date`), y luego
    se asignan columnas de auditoría con la función `set_audit_columns`.

    La función hace uso de la biblioteca `threading` para ejecutar todas las tareas en paralelo. Después
    de iniciar los hilos, espera que todos terminen su ejecución antes de finalizar.

    Steps:
    1. Define la fecha de extracción utilizando la fecha y hora actual.
    2. Crea hilos para ejecutar las funciones de extracción de datos de las diferentes tablas.
    3. Inicia todos los hilos para que las extracciones de datos se realicen en paralelo.
    4. Espera a que todos los hilos terminen antes de finalizar el proceso.

    Returns:
        None: La función no devuelve ningún valor. Las extracciones se realizan directamente sobre los
        DataFrames correspondientes y las columnas de auditoría se actualizan en el proceso.
    """
    log_error(DESTINATION_PATH)
    extract_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Crear hilos para cada tarea de extracción
    threads = []

    # Crear y agregar los hilos
    thread_booking = threading.Thread(target=extract_booking, args=(extract_date,))
    thread_passenger = threading.Thread(target=extract_booking_passenger, args=(extract_date,))
    thread_segment = threading.Thread(target=extract_passenger_journey_segment, args=(extract_date,))
    thread_leg = threading.Thread(target=extract_passenger_journey_leg, args=(extract_date,))
    thread_charge = threading.Thread(target=extract_passenger_journey_charge, args=(extract_date,))

    # Agregar los hilos a la lista
    threads.append(thread_booking)
    threads.append(thread_passenger)
    threads.append(thread_segment)
    threads.append(thread_leg)
    threads.append(thread_charge)

    # Iniciar todos los hilos
    for thread in threads:
        thread.start()

    # Esperar que todos los hilos terminen
    for thread in threads:
        thread.join()

    log_error("All data extraction threads completed.")

