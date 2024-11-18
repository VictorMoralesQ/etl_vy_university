# IMPORTS
import os.path
import pandas as pd
import requests
import time
from dotenv import load_dotenv
from utils.utils import log_error

load_dotenv()
DESTINATION_PATH = os.getenv("DESTINATION_PATH")
API_URL = f'http://{os.getenv("API_URL")}:{os.getenv("API_PORT")}'

ENDPOINTS_CONFIG = {
    "booking/new": {
        "columns": os.getenv("BOOKING_NEW_COLUMNS").split(","),
        "process_data": None,
        "params": {
            "limit": 1000,
            "offset": 0
        }
    },
    "booking/passenger/new": {
        "columns": os.getenv("BOOKING_PASSENGER_NEW_COLUMNS").split(","),
        "process_data": None,
        "params": {
            "limit": 1000,
            "offset": 0
        }
    },
}

def extract_from_api(endpoint):
    """
     Extrae datos de un API configurado en el archivo de configuración de endpoints, procesando la respuesta
    y devolviendo un DataFrame con los datos extraídos.

    La función realiza una solicitud GET a un endpoint específico de la API, gestionando la paginación
    y procesando los datos recibidos según la configuración definida en `ENDPOINTS_CONFIG`. Los datos
    extraídos se devuelven como un DataFrame de pandas con las columnas especificadas para cada endpoint.

    Args:
        endpoint (str): El nombre del endpoint de la API desde el cual se extraerán los datos. Este endpoint
                         debe estar previamente configurado en el diccionario `ENDPOINTS_CONFIG`.

    Returns:
        pd.DataFrame or None: Si los datos se extraen correctamente, se devuelve un DataFrame con los datos
                               obtenidos. Si ocurre un error o no se encuentran datos, se devuelve `None`.
    """
    if endpoint not in ENDPOINTS_CONFIG:
        log_error(f"Endpoint {endpoint} no está configurado en los endpoints disponibles.")
        return None

    endpoint_config = ENDPOINTS_CONFIG[endpoint]

    params = endpoint_config.get("params", {})
    limit = params.get("limit", 1000)
    offset = params.get("offset", 0)
    all_data = []

    while True:
        params.update({"limit": limit, "offset": offset})

        try:
            response = requests.get(f'{API_URL}/{endpoint}', params=params)
            response.raise_for_status()

            data = response.json()

            data = data.get('data', [])

            if endpoint_config["process_data"]:
                data = endpoint_config["process_data"](data)

            if isinstance(data, list):
                all_data.extend(data)
            elif isinstance(data, dict):
                all_data.append(data)

            if len(data) < limit:
                break

            offset += limit
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            log_error(f"Error al hacer la solicitud GET a {API_URL}/{endpoint}: {e}")
            return None
        except ValueError:
            log_error(f"Error: La respuesta no es un JSON válido para {endpoint}.")
            return None

    if all_data:
        df = pd.DataFrame(all_data, columns=endpoint_config["columns"])
        log_error(f"Datos extraídos correctamente para el endpoint: {endpoint}")
        return df
    else:
        log_error(f"No se encontraron datos para el endpoint {endpoint}.")
        return None