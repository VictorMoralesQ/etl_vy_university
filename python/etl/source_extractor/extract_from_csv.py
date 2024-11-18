# IMPORTS
import os.path
import pandas as pd
from dotenv import load_dotenv
from utils.utils import log_error

load_dotenv()
DESTINATION_PATH = os.getenv("DESTINATION_PATH")
API_URL = f'http://{os.getenv("API_URL")}:{os.getenv("API_PORT")}'

CSV_FILES = {
    "PassengerJourneyLeg_20190201_20190331.csv": ";",
    "PassengerJourneyCharge_20190201_20190331.csv" : ","
}

def extract_from_csv(file_path, header=0, null_values=""):
    """
    Extrae datos desde un archivo CSV y los carga en un DataFrame de pandas.

    La función lee un archivo CSV usando el separador configurado para ese archivo. Si no se encuentra el separador
    en la configuración, se usa la coma como separador por defecto. Además, permite definir valores nulos en el archivo
    mediante el parámetro `null_values` y especificar qué fila debe ser usada como encabezado con el parámetro `header`.

    Args:
        file_path (str): Ruta del archivo CSV desde el que se extraerán los datos.
        header (int or str, optional): Fila que debe ser usada como encabezado. El valor por defecto es 0 (la primera fila).
        null_values (str, optional): Valor que debe ser tratado como `NaN`. El valor por defecto es una cadena vacía.

    Returns:
        pd.DataFrame or None: Si la extracción es exitosa, se devuelve un DataFrame con los datos del archivo. Si ocurre un
                               error (por ejemplo, el archivo no se encuentra o el archivo tiene problemas de formato),
                               se devuelve `None`.
    """
    try:

        base_name = os.path.basename(file_path)

        if base_name in CSV_FILES:
            sep = CSV_FILES[base_name]
        else:
            log_error(f"Error: No se encontró el separador para el archivo {file_path}")
            sep = ","

        df = pd.read_csv(file_path, sep=sep, header=header, na_values=null_values)

        log_error(f"Datos extraídos correctamente desde el archivo: {file_path}")
        return df

    except FileNotFoundError:
        log_error(f"Error: No se encontró el archivo {file_path}")
        return None
    except pd.errors.ParserError as e:
        log_error(f"Error al leer el archivo {file_path}: {e}")
        return None

