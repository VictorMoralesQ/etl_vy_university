# Proyecto de Carga y Transformación de Datos

Este proyecto está diseñado para la carga, transformación y almacenamiento de datos en una base de datos PostgreSQL utilizando archivos CSV como fuente de datos. La solución está dividida en varias funciones y clases que permiten automatizar el proceso de transformación y carga de datos, así como manejar registros de errores y auditoría de los procesos.

## Funciones Principales

### 1. **`log_error(message: str)`**
   **Descripción:**
   - Registra un mensaje de error en un archivo de log, y si el archivo no existe, lo crea.
   - Utiliza el módulo `logging` para registrar los errores, y si ocurre un error adicional al escribir el archivo de log, lo maneja adecuadamente.
   
   **Por qué es importante:**
   - El registro de errores es fundamental en procesos automáticos para poder diagnosticar y solucionar problemas rápidamente.
   - La función asegura que los mensajes de error sean almacenados de manera persistente para su revisión futura, especialmente en un entorno de producción.

### 2. **`set_audit_columns(df: pd.DataFrame, source: str, extract_date: str, proc_type: str, path: str)`**
   **Descripción:**
   - Esta función agrega columnas de auditoría a un DataFrame, incluyendo la fecha de extracción (`extract_dt`), la fuente de los datos (`source`) y el tipo de procesamiento (`proc_status`).
   - Luego guarda el DataFrame actualizado en un archivo CSV con un nombre de archivo basado en la fuente, la fecha y el tipo de procesamiento.
   
   **Por qué es importante:**
   - Las columnas de auditoría son clave para realizar un seguimiento detallado de los procesos ETL (Extract, Transform, Load).
   - Permiten mantener un registro completo del origen y la fecha de los datos transformados, lo cual es útil para auditorías y depuración de procesos.
   - Garantiza que los datos transformados estén correctamente documentados antes de ser almacenados.

### 3. **`transform_source(source, info, results)`**
   **Descripción:**
   - Realiza el proceso de transformación de los datos de una fuente específica.
   - Lee los datos, limpia y filtra los mismos según el tipo de archivo, y realiza transformaciones adicionales si es necesario.
   - También genera una clave de negocio y un hash para cada fila de datos.
   - Después de la transformación, agrega las columnas de auditoría y guarda el archivo resultante.

   **Por qué es importante:**
   - Es una función esencial para el proceso ETL ya que transforma los datos de una forma que es adecuada para su posterior carga en una base de datos.
   - Permite manejar distintos tipos de datos de entrada (como CSV) y asegurar que las transformaciones sean aplicadas de manera consistente a través de diferentes fuentes de datos.

### 4. **`transform()`**
   **Descripción:**
   - Este es un proceso en paralelo que lanza hilos para transformar los datos de distintas fuentes de forma concurrente.
   - A medida que se procesan las fuentes de datos, se almacenan los resultados en un diccionario y se espera a que todos los hilos finalicen.

   **Por qué es importante:**
   - La paralelización mejora significativamente la eficiencia del proceso ETL al permitir que múltiples fuentes de datos sean transformadas al mismo tiempo.
   - Es útil cuando se trabaja con grandes volúmenes de datos y se necesita optimizar el tiempo de ejecución.

### 5. **`create_table_thread(self, sql_query: str)`**
   **Descripción:**
   - Crea una nueva tabla en la base de datos ejecutando una sentencia SQL dada. Este proceso se ejecuta en un hilo separado para permitir la creación de múltiples tablas de manera concurrente.
   
   **Por qué es importante:**
   - La capacidad de crear tablas en paralelo optimiza el tiempo de creación de la estructura en la base de datos.
   - Esto es útil cuando se están configurando múltiples tablas para un proyecto y se necesita asegurar que todas estén listas en el menor tiempo posible.

### 6. **`create_tables_from_sql(self)`**
   **Descripción:**
   - Crea todas las tablas necesarias a partir de las sentencias SQL definidas en un archivo, utilizando hilos para ejecutar las consultas de manera paralela.

   **Por qué es importante:**
   - Al igual que la función `transform()`, la creación paralela de tablas permite reducir el tiempo total de ejecución del proceso.
   - Esta función es clave para inicializar la base de datos antes de cargar los datos.

### 7. **`full_load_insert(self, table_name, csv_file, columns)`**
   **Descripción:**
   - Realiza una carga completa de los datos en una tabla, eliminando los datos existentes y luego insertando nuevos datos desde un archivo CSV.
   
   **Por qué es importante:**
   - Esta función es útil para cargar datos iniciales o para realizar una recarga total de los datos en la base de datos.
   - Eliminar y reemplazar datos garantiza que los datos en la base de datos sean siempre los más recientes.

### 8. **`incremental_load_insert(self, table_name, csv_file, columns, key_column)`**
   **Descripción:**
   - Realiza una carga incremental, donde los registros existentes se actualizan y los nuevos registros se insertan, basándose en una columna clave (como un `hash` o `business_key`).
   
   **Por qué es importante:**
   - Esencial para mantener los datos actualizados sin necesidad de realizar una carga completa cada vez.
   - La carga incremental es más eficiente ya que solo se actualizan o insertan los registros que han cambiado.

### 9. **`ask_user_for_load_type(self)`**
   **Descripción:**
   - Solicita al usuario que elija el tipo de carga (completa o incremental).
   
   **Por qué es importante:**
   - Permite al usuario elegir cómo quiere cargar los datos, proporcionando flexibilidad según el tipo de proceso necesario.
   - Es fundamental para automatizar el flujo de trabajo dependiendo de si es necesario realizar una carga completa o solo una actualización incremental.

### 10. **`insert_all_data(self)`**
   **Descripción:**
   - Inserta todos los datos en las tablas correspondientes, preguntando al usuario si desea hacer una carga completa o incremental y luego llamando a las funciones adecuadas para cada caso.

   **Por qué es importante:**
   - Es la función central para realizar la carga de datos en la base de datos después de la transformación.
   - Permite cargar los datos de manera eficiente y flexible, dependiendo de las necesidades del proyecto.

## Requisitos

- Python 3.12
- Librerías:
  - `requests`: para hacer peticiones HTTP a APIs o servicios externos.
  - `numpy`: para operaciones matemáticas y manipulación de arrays de alto rendimiento.
  - `pandas`: para la manipulación y análisis de datos, especialmente para trabajar con DataFrames y archivos CSV.
  - `SQLAlchemy`: para interactuar con bases de datos relacionales utilizando un ORM (Object Relational Mapper).
  - `psycopg2-binary`: para la conexión a bases de datos PostgreSQL desde Python.
  - `python-dotenv`: para cargar variables de entorno desde un archivo `.env` de manera sencilla.
  - `openpyxl`: para leer y escribir archivos Excel (XLSX).
  - `datetime`: para trabajar con fechas y horas en Python.
  - `json`: para trabajar con datos en formato JSON.
  - `hashlib`: para realizar operaciones de hashing como MD5, SHA-1, SHA-256, entre otros.
  - `threading`: para ejecutar múltiples hilos de manera concurrente en Python.

## Instalación

1. Levantar el contenedor de Docker con la base de datos PostgreSQL:
    ```bash
    docker-compose up -d
    ```

2. Instala las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```

3. Crea un archivo `.env` para definir las credenciales y parámetros de la base de datos:
    ```bash
    # .env
    DB_USER=usuario
    DB_PASSWORD=contraseña
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=nombre_base_datos
    ```

## Ejecución

Para ejecutar el proceso de carga y transformación de datos, simplemente llama a la función `load()` desde tu archivo principal o script:

```python
from etl.extract import extract
from etl.transform import transform
from etl.load import load

extract()
transform()
load()
