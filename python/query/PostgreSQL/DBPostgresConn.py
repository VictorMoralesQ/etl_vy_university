import psycopg2
from dotenv import load_dotenv
import os
import threading
from query.PostgreSQL.CREATE.create_tables_sql import create_Booking, create_BookingPassenger, create_PassengerJourneyCharge, create_PassengerJourneyLeg, create_PassengerJourneySegment
import pandas as pd

from utils.utils import log_error


class dbpostgresconn:
    def __init__(self):
        """Inicia la configuración de la conexión a la base de datos PostgreSQL"""
        try:
            load_dotenv()
            self.user = os.getenv("POSTGRES_USER")
            self.password = os.getenv("POSTGRES_PASSWORD")
            self.host = os.getenv("POSTGRES_HOST")
            self.port = os.getenv("POSTGRES_PORT")
            self.database = os.getenv("POSTGRES_DB")
        except Exception as e:
            log_error(f"Error al cargar las variables de entorno: {e}")

    def create_table_thread(self, sql_query: str):
        """
        Función auxiliar que ejecuta la creación de una tabla en un hilo con su propia conexión y cursor.

        Esta función ejecuta una consulta SQL para crear una tabla en la base de datos. La creación de la tabla se realiza
        en un hilo separado para permitir la ejecución concurrente de múltiples tareas.

        Args:
            sql_query (str): La consulta SQL que crea la tabla en la base de datos.

        Returns:
            None: No retorna un valor. Si la tabla se crea correctamente, se imprime un mensaje de éxito,
            de lo contrario, se imprime un mensaje de error.
        """
        try:
            # Crear una nueva conexión y cursor dentro del hilo
            conn = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            cursor = conn.cursor()

            # Ejecutar la consulta SQL
            cursor.execute(sql_query)
            conn.commit()
            log_error("Tabla creada correctamente.")

            # Cerrar el cursor y la conexión después de ejecutar la consulta
            cursor.close()
            conn.close()

        except Exception as e:
            log_error(f"Error al crear la tabla: {e}")

    def create_tables_from_sql(self):
        """
        Crea todas las tablas a partir de las sentencias SQL definidas utilizando hilos para ejecución concurrente.

        Esta función crea varias tablas en la base de datos ejecutando las sentencias SQL correspondientes en hilos
        independientes, lo que permite la ejecución concurrente y mejora la eficiencia.

        Returns:
            None: No retorna ningún valor. Imprime un mensaje de éxito si todas las tablas se crean correctamente,
            o un mensaje de error si algo falla.
        """
        try:
            # Creamos los hilos para cada sentencia de creación de tabla
            log_error("Creando las tablas concurrentemente...")

            threads = [
                threading.Thread(target=self.create_table_thread, args=(create_Booking,)),
                threading.Thread(target=self.create_table_thread, args=(create_BookingPassenger,)),
                threading.Thread(target=self.create_table_thread, args=(create_PassengerJourneyCharge,)),
                threading.Thread(target=self.create_table_thread, args=(create_PassengerJourneyLeg,)),
                threading.Thread(target=self.create_table_thread, args=(create_PassengerJourneySegment,))
            ]

            # Iniciar todos los hilos
            for thread in threads:
                thread.start()

            # Esperar a que todos los hilos terminen
            for thread in threads:
                thread.join()

            log_error("Todas las tablas fueron creadas correctamente.")

        except Exception as e:
            log_error(f"Error al crear las tablas: {e}")

    def full_load_insert(self, table_name, csv_file, columns):
        """
        Realiza una carga completa de datos: elimina los registros existentes y luego inserta los nuevos datos.

        Esta función elimina los datos existentes en la tabla especificada y luego inserta los nuevos datos
        desde un archivo CSV.

        Args:
            table_name (str): El nombre de la tabla en la base de datos donde se insertarán los datos.
            csv_file (str): La ruta al archivo CSV que contiene los nuevos datos.
            columns (tuple): Una tupla con los nombres de las columnas de la tabla.

        Returns:
            None: No retorna un valor. Si la operación es exitosa, se imprime un mensaje de éxito,
            de lo contrario, se imprime un mensaje de error.
        """
        try:
            # Leer el archivo CSV en un DataFrame
            df = pd.read_csv(csv_file, sep='|', header=0, na_values=None)

            # Asegurarse de que el número de columnas coincida
            if len(df.columns) != len(columns):
                raise ValueError(
                    f"El número de columnas en el CSV no coincide con el número de columnas de la tabla {table_name}")

            placeholders = ', '.join(['%s'] * len(columns))
            insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

            conn = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            cursor = conn.cursor()

            # Insertar los nuevos datos en la tabla
            for _, row in df.iterrows():
                cursor.execute(insert_query, tuple(row))

            conn.commit()
            log_error(f"Datos insertados correctamente en la tabla {table_name}")

            cursor.close()
            conn.close()

        except Exception as e:
            log_error(f"Error al insertar los datos en {table_name}: {e}")

    def incremental_load_insert(self, table_name, csv_file, columns, key_column):
        """
         Realiza una carga incremental de datos: actualiza los registros existentes o inserta nuevos registros.

        Esta función actualiza los registros existentes en la tabla utilizando el `key_column` (como `business_key`
        o `hash`), o inserta nuevos registros si no existen.

        Args:
            table_name (str): El nombre de la tabla en la base de datos donde se insertarán los datos.
            csv_file (str): La ruta al archivo CSV que contiene los nuevos datos.
            columns (tuple): Una tupla con los nombres de las columnas de la tabla.
            key_column (str): El nombre de la columna que actúa como clave primaria o identificador único para la carga incremental.

        Returns:
            None: No retorna un valor. Si la operación es exitosa, se imprime un mensaje de éxito,
            de lo contrario, se imprime un mensaje de error.
        """
        try:
            # Leer el archivo CSV en un DataFrame
            df = pd.read_csv(csv_file, sep='|', header=0, na_values=None)

            # Asegurarse de que el número de columnas coincida
            if len(df.columns) != len(columns):
                raise ValueError(
                    f"El número de columnas en el CSV no coincide con el número de columnas de la tabla {table_name}")

            # Crear la sentencia SQL para el INSERT
            placeholders = ', '.join(['%s'] * len(columns))
            insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

            # Crear la sentencia SQL para la actualización (basada en la business_key)
            update_query = f"""
            UPDATE {table_name}
            SET {', '.join([f"{col} = EXCLUDED.{col}" for col in columns if col != key_column])}
            WHERE {key_column} = EXCLUDED.{key_column};
            """

            # Crear una nueva conexión y cursor para la inserción
            conn = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            cursor = conn.cursor()

            # Insertar los datos en la tabla, con la opción de actualización en caso de conflicto en la business_key
            for _, row in df.iterrows():
                # Usamos ON CONFLICT para manejar las actualizaciones de registros existentes
                cursor.execute(f"""
                INSERT INTO {table_name} ({', '.join(columns)})
                VALUES ({', '.join(['%s'] * len(columns))})
                ON CONFLICT ({key_column})
                DO UPDATE SET {', '.join([f"{col} = EXCLUDED.{col}" for col in columns if col != key_column])}
                """, tuple(row))

            # Commit para confirmar la transacción
            conn.commit()
            log_error(f"Datos insertados o actualizados correctamente en la tabla {table_name}")

            # Cerrar el cursor y la conexión después de ejecutar la consulta
            cursor.close()
            conn.close()

        except Exception as e:
            log_error(f"Error al insertar/actualizar los datos en {table_name}: {e}")

    def ask_user_for_load_type(self):
        """
        Pregunta al usuario cómo desea realizar la carga de datos (Full o Incremental).

        La función interactúa con el usuario para determinar si debe realizar una carga completa o incremental.

        Returns:
            str: La opción de carga seleccionada por el usuario, puede ser `'full'` o `'incremental'`.
        """
        log_error("Cómo deseas realizar la carga de datos?")
        log_error("1. Carga Full")
        log_error("2. Carga Incremental")

        choice = input("Selecciona 1 para Carga Full o 2 para Carga Incremental: ")

        if choice == '1':
            return 'full'
        elif choice == '2':
            return 'incremental'
        else:
            log_error("Opción inválida. Selecciona 1 para Carga Full o 2 para Carga Incremental.")
            return self.ask_user_for_load_type()  # Llamar recursivamente si la opción no es válida

    def insert_all_data(self):
        """
         Inserta todos los datos en las tablas correspondientes, eligiendo entre carga completa (full) o incremental
        según la selección del usuario.

        Esta función coordina la carga de datos en varias tablas de la base de datos. Primero, le pregunta al usuario si
        desea realizar una carga completa (donde se eliminan los datos existentes e insertan los nuevos) o una carga
        incremental (donde se actualizan los registros existentes o se insertan los nuevos). Para cada tabla, los datos
        se cargan desde archivos CSV específicos y se insertan utilizando las funciones adecuadas de carga (full o
        incremental).

        El tipo de carga se determina según la respuesta del usuario a través de la función `ask_user_for_load_type`.
        La carga de datos se realiza de manera eficiente utilizando las funciones `full_load_insert` e `incremental_load_insert`,
        dependiendo de la opción seleccionada.

        Args:
            None: Esta función no recibe parámetros directamente. Los parámetros necesarios, como las rutas de los archivos CSV
            y los nombres de las columnas, están definidos dentro de la función.

        Returns:
            None: La función no retorna un valor. En su lugar, imprime mensajes informativos sobre el progreso de la carga de datos.
        """
        # Definir las tablas y sus columnas
        load_type = self.ask_user_for_load_type()

        def string_to_tuple(string):
            return tuple(string.split(', '))

        tables_columns = {
            'public.Booking': string_to_tuple(os.getenv('TABLES_COLUMNS_BOOKING_NEW')),
            'public.BookingPassenger': string_to_tuple(os.getenv('TABLES_COLUMNS_BOOKINGPASSENGER_NEW')),
            'public.PassengerJourneyCharge': string_to_tuple(os.getenv('TABLES_COLUMNS_PASSENGERJOURNEYCHARGE')),
            'public.PassengerJourneyLeg': string_to_tuple(os.getenv('TABLES_COLUMNS_PASSENGERJOURNEYLEG')),
            'public.PassengerJourneySegment': string_to_tuple(os.getenv('TABLES_COLUMNS_PASSENGERJOURNEYSEGMENT'))
        }

        # Definir las rutas de los archivos CSV
        csv_files = {
            'public.Booking': os.getenv('SILVER_BOOKING_NEW'),
            'public.BookingPassenger': os.getenv('SILVER_PASSENGER_NEW'),
            'public.PassengerJourneyCharge': os.getenv('SILVER_CHARGE'),
            'public.PassengerJourneyLeg': os.getenv('SILVER_LEG'),
            'public.PassengerJourneySegment': os.getenv('SILVER_SEGMENT')
        }

        # Insertar datos en cada tabla
        for table, columns in tables_columns.items():
            if table in csv_files:
                if load_type == 'full':
                    self.full_load_insert(table, csv_files[table], columns)
                elif load_type == 'incremental':
                    self.incremental_load_insert(table, csv_files[table], columns, key_column='hash')