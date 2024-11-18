# IMPORTS
import os.path
import pandas as pd
from utils.utils import log_error


XLS_FILES = {
    "PassengerJourneySegment_20190201_20190331.xlsx": 0
}

def extract_from_excel(file_path, null_values=None):
    """
    Extrae datos desde un archivo Excel y los carga en un DataFrame de pandas.

    Esta función lee un archivo Excel y carga los datos de una hoja específica configurada para ese archivo. Si no se
    encuentra la hoja en la configuración, se devuelve un error. También permite definir valores nulos en el archivo
    mediante el parámetro `null_values`.

    Args:
        file_path (str): Ruta del archivo Excel desde el que se extraerán los datos.
        null_values (str, optional): Valor que debe ser tratado como `NaN`. El valor por defecto es `None`.

    Returns:
        pd.DataFrame or None: Si la extracción es exitosa, se devuelve un DataFrame con los datos del archivo. Si ocurre un
                               error (por ejemplo, el archivo no se encuentra o el archivo está vacío), se devuelve `None`.
    """
    try:
        # Obtener el nombre base del archivo
        base_name = os.path.basename(file_path)

        # Verifica si el archivo está en el diccionario de archivos de Excel
        if base_name in XLS_FILES:
            sheet_name = XLS_FILES[base_name]  # obtener el número de la hoja o el nombre de la hoja
        else:
            log_error(f"Error: No se encontró el archivo {file_path} en los archivos disponibles.")
            return None

        # Leer el archivo Excel
        df = pd.read_excel(file_path, sheet_name=sheet_name, na_values=null_values)

        # Verificación de si los datos fueron leídos correctamente
        if df.empty:
            log_error(f"El archivo {file_path} está vacío o no contiene datos válidos.")
            return None

        log_error(f"Datos extraídos correctamente desde el archivo Excel: {file_path}")
        return df

    except FileNotFoundError:
        log_error(f"Error: No se encontró el archivo {file_path}")
        return None
    except ValueError as e:
        log_error(f"Error al leer el archivo Excel {file_path}: {e}")
        return None
    except Exception as e:
        log_error(f"Error desconocido al leer el archivo {file_path}: {e}")
        return None