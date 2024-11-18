# VY University - Python Final Project

![overview](img/ETL_overview.png)

Este proyecto está diseñado para evaluar los conocimientos adquiridos en Python y su aplicación en el desarrollo de procesos ETL (Extract, Transform, Load). Utilizamos **Docker** y **Docker Compose** para desplegar servicios de **PostgreSQL**, un **API Fake** y por último ejecutar tus procesos en **Python**.

El objetivo del examen es implementar un proceso ETL en Python que integre múltiples fuentes de datos (API y datasets de diferentes formatos y extensiones). Los scripts de Python deben ser altamente parametrizables, facilitando la flexibilidad, escalabilidad y reutilización bajo distintos escenarios. 

¡Buena suerte!

---

## Índice

1. [Prerrequisitos](#1-prerrequisitos)
2. [Configuración y Estructura del Proyecto](#2-configuración-y-estructura-del-proyecto)
3. [Despliegue API](#3-despliegue-api)
4. [Fuentes de Datos](#4-fuentes-de-datos)
5. [Uso de Librerías](#5-uso-de-librerías)
6. [Extracción de Datos](#6-extracción-de-datos)
7. [Transformación de Datos](#7-transformación-de-datos)
8. [Carga de Datos en las Tablas de la Base de Datos](#8-carga-de-datos-en-las-tablas-de-la-base-de-datos)
9. [Requisitos Finales y Entregables](#9-requisitos-finales-y-entregables)
10. [Entrega y Live Demo](#10-entrega-y-live-demo)

---

## 1. Prerrequisitos

Antes de comenzar, asegúrate de tener instalados los siguientes programas en tu sistema:

- **Docker**: Puedes descargarlo e instalarlo desde [Docker](https://docs.docker.com/get-docker/).
- **Docker Compose**: Puedes encontrar las instrucciones de instalación en [Docker Compose](https://docs.docker.com/compose/install/).

**Opcional**:

- **Python 3.12**: Aunque la ejecución final del proceso se realizará en contenedores, contar con Python 3.12 instalado localmente te será útil para el desarrollo y pruebas locales previas. Puedes descargarlo desde [Python](https://www.python.org/downloads/).

---

## 2. Configuración y estructura del Proyecto

**2.1. Descarga el archivo del proyecto**:
   Descarga el archivo `vy-university-python-final-exam.zip` y extráelo en tu máquina local.

**2.2. Navega al directorio del proyecto**:
   Abre una terminal y cambia al directorio donde has descomprimido el archivo. Por ejemplo:
   ```bash
   cd path/to/vy-university-python-final-exam
   ```

**2.3. Estructura del Proyecto**:

   ```
   vy-university-python-final-exam
   ├── data
   │   ├── bronze
   │   ├── gold
   │   ├── silver
   │   └── source
   │       ├── PassengerJourneyCharge_202410211323.csv
   │       ├── PassengerJourneyLeg_202410211320.csv
   │       └── PassengerJourneySegment_202410211316.xlsx
   ├── deploy
   │   ├── api
   │   │   ├── .datasets
   │   │   ├── main.py
   │   ├── .env
   │   ├── docker-compose.yml
   │   ├── Dockerfile
   │   └── requirements.txt 
   ├── img
   │   └── ER Navitaire.jpg
   │   └── ETL_overview.png
   ├── log
   ├── python
   │   ├── etl
   │   │   ├── __init__.py
   │   │   ├── extract.py
   │   │   ├── load.py
   │   │   └── transform.py
   │   └── utils
   │       ├── __init__.py 
   │       └── utils.py 
   │   └──__init__.py   
   │   └── main.py
   ├── query 
   │   └── PostgreSQL
   │       ├── CREATE
   │       └── INSERT
   ├── .env
   ├── README.md
   ├── README_PROYECTO.md
   └── requirements.txt
   ```

---

## 3. Despliegue API

Para realizar el despliegue de la aplicación y la puesta en marcha del API y la base de datos, deberás seguir los siguientes pasos:

**3.1. Navega al directorio**

   Dentro de tu directorio `vy-university-python-final-exam`, accede a la carpeta `deploy`. Para ello, abre una terminal y cambia al directorio donde has descomprimido el archivo. Por ejemplo:

   ```bash
   cd path/to/vy-university-python-final-exam/deploy
   ```
   
**3.2. Despliegue del entorno**

   Para poner en marcha los servicios de base de datos, ejecuta el siguiente comando en tu terminal:

   ```bash   
   docker-compose up -d
   ```
   Este comando iniciará los contenedores en modo "detached", permitiéndote continuar utilizando la terminal.

**3.3. Verificar el funcionamiento de los servicios**

   Para asegurarte de que todos los contenedores están funcionando correctamente, puedes ejecutar:
   ```bash      
   docker-compose ps
   ```
   Esto te mostrará el estado de los contenedores iniciados por Docker Compose.

**3.4. Conexión a los servicios**

Una vez desplegados los contenedores, podrás acceder a los servicios correspondientes. Las credenciales para la conexión de la base de datos se encuentran en el archivo `.env` dentro del directorio `/vy-university-python-final-exam/deploy`. Una vez que los contenedores estén desplegados, podrás crear la conexión correspondiente a la base de datos usando la herramienta de tu preferencia y probar la API y su funcionamiento con Postman.

---

## 4. Fuentes de Datos

Este proyecto incluye varias fuentes de datos que serán utilizadas para el proceso ETL. Se detallan a continuación las principales fuentes, incluidas una API y archivos en diferentes formatos que deberán ser procesados en Python siguiendo las instrucciones para cada capa de datos.

### 4.1. Fuente de Datos - API FastAPI

La **API FastAPI** proporciona información relacionada con reservas (`Booking`) y pasajeros asociados a esas reservas (`BookingPassenger`). Es importante el uso de parámetros como `limit` y `offset` para controlar la cantidad de datos devueltos y la paginación.

#### **URL de la API**

La API está disponible localmente en la siguiente dirección:

```bash
http://localhost:8000
```
#### Endpoints a utilizar

Puedes encontrar la documentación de la api en http://localhost:8000/docs.

##### Endpoint 1: `/booking`
Obtiene información sobre las reservas.

- **Método HTTP:** `GET`
  - **Parámetros opcionales:**
    - `limit` (entero): Número máximo de registros a devolver. Valor por defecto: 1000.
    - `offset` (entero): Número de registros a omitir desde el inicio. Valor por defecto: 0.

**Ejemplo de solicitud:**

```bash
GET http://localhost:8000/booking?limit=100&offset=0
```
##### Endpoint 2: `/booking/passenger`

Obtiene información sobre los pasajeros asociados a las reservas.

- **Método HTTP:** `GET`
- **Parámetros opcionales:**
  - `limit` (entero): Número máximo de registros a devolver. Valor por defecto: 1000.
  - `offset` (entero): Número de registros a omitir desde el inicio. Valor por defecto: 0.

**Ejemplo de solicitud:**

```bash
GET http://localhost:8000/booking/passenger?limit=100&offset=0
```

#### Cómo Conectarse y Extraer Datos

1. **Iniciar el servidor de la API:**  
   Validar que el servidor FastAPI en `localhost:8000` este corriendo antes de realizar cualquier solicitud.

2. **Realizar solicitudes a los endpoints:**  
   Puedes utilizar herramientas como `curl`, **Postman**, o un navegador para realizar solicitudes `GET` a los endpoints especificados.

3. **Control de los parámetros `limit` y `offset`:**  
   Utiliza los parámetros `limit` y `offset` para gestionar la cantidad de datos obtenidos y la paginación.
   - `limit`: Define cuántos registros se devolverán en la solicitud.
   - `offset`: Controla desde qué registro se comienza a contar.
4. **Procesamiento de los datos:**  
   Una vez que hayas obtenido los datos de la API, debes procesarlos en Python y guardarlos en un solo archivo segun la uri que estes consultando. Elemplo si estas consultando la uri `/booking` debes guardar los datos en un archivo llamado `Booking_(Fecha de la extraccion)_extracted.csv` en la carpeta `data/bronze` siguiendo el resto de requisitos que te indican para los datos de la capa bronze. Por otra parte si el uri es `/booking/passenger` debes guardar los datos en un archivo llamado `BookingPassenger_(Fecha de la extraccion)_extracted.csv` en la carpeta `data/bronze` siguiendo el resto de requisitos que te indican para los datos de la capa bronze.

### 4.2 Fuente de datos - Archivos de la carpeta de data

El proyecto también incluye una carpeta llamada `data/source`, que contiene archivos en diversos formatos. Estos archivos deben ser procesados en Python como parte del proceso ETL. Es importante que los scripts de Python sean parametrizables, permitiendo ajustar configuraciones como el tipo de archivo, separadores, manejo de valores nulos, entre otros.

### Consideraciones

- **Múltiples formatos de archivo:** La implementación debe ser capaz de procesar archivos en formato **CSV**, **Excel (.xls, .xlsx)**, entre otros.
- **Parámetros configurables:** Al procesar los archivos, se deben tener en cuenta parámetros como:
- **Separador:** Para archivos CSV, el separador de columnas puede variar (`,` o `;`, entre otros).
- **Manejo de nulos:** Especifica cómo manejar valores nulos en los datos.
- **Encabezados:** Indica si el archivo contiene encabezados.
- **Ejecución de contenedores efímeros:** Una vez obtenidos los datos de la API, debes procesarlos en Python y guardarlos en un único archivo por fuente en la carpeta `data/source`, y en la carpeta `data/bronze` siguiendo los requisitos para la capa bronze. El nombre del archivo debe reflejar la **URI** consultada, por ejemplo:

  •	Si la URI es `/booking`, el archivo se nombrará `Booking_(Fecha de la extracción).csv.

  •	Si la URI es `/booking/passenger`, el archivo se nombrará `BookingPassenger_(Fecha de la extracción).csv`.

---

## 5. Uso de Librerías
En este proyecto, se permite utilizar cualquier librería externa que consideres útil, además de las librerías nativas de Python. Sin embargo, se recomienda el uso de las siguientes librerías, que facilitarán la manipulación de datos y el desarrollo de los procesos ETL:

- **pandas:** Ideal para la manipulación de datos en Python, con soporte para archivos **CSV** y **Excel**.
- **openpyxl:** Librería recomendada para leer y escribir archivos de Excel en Python.

Recuerda que es importante que cualquier librería externa que utilices se indique en el archivo `requirements.txt` para asegurar la correcta instalación de dependencias.

---

## 6. Extracción de datos

El objetivo de esta etapa es obtener datos desde las fuentes especificadas (APIs o archivos). La fase de extracción debe encargarse de conectarse a la fuente de datos, descargar o leer los datos y almacenarlos en un formato intermedio para su posterior procesamiento. Es recomendable que el script `extract.py` gestione esta etapa, permitiendo obtener los datos de diferentes fuentes de manera parametrizable.

### Consideraciones:

6.1. **Fecha y hora de extracción**: Al leer y cargar los datos, se debe agregar una columna con la fecha y hora de la extracción para registrar cuándo se obtuvieron los datos. La columna sera llamada `extract_dt`.

6.2. **Fuente de los datos**: Es necesario incluir un campo que indique la fuente de los datos. Por ejemplo, si los datos se cargaron desde el archivo "XXX" o desde la API "YYY", este valor debe ser reemplazado por el correspondiente. La columna sera llamada `source`.

6.3. **Estado de procesamiento**: Indica el estado actual del registro dentro del flujo ETL, como “extracted”, “transformed” o “loaded”. La columna sera llamada `proc_status`.

6.4. **Conservación de columnas originales**: El archivo debe conservar las columnas originales y agregar las nuevas solicitadas.

6.5. **Formato del archivo**: Los datos procesados deben ser guardados en un archivo CSV utilizando el separador "|".

6.6. **Nombre del archivo**: El archivo resultante debe tener un nombre descriptivo que indique la fuente y la palabra "extracted". Por ejemplo: `PassengerJourneyCharge_202410211323_extracted.csv`.

Una vez que se han leído y procesado los datos, los archivos resultantes de la extracción deben depositarse en la carpeta `data/bronze`.

---

## 7. Transformación de Datos

En esta etapa se deben implementar las transformaciones necesarias, tales como limpieza de datos, manejo de valores nulos o transformaciones específicas según el formato de los datos. La transformación debe asegurar que los datos sean consistentes y adecuados para ser cargados en la base de datos de destino. Se recomienda que las transformaciones se implementen en el script `transform.py`, separando la lógica de negocio de las otras etapas.

Es importante destacar que este proceso debe leer los archivos de la capa previa que se encuentran en la dirección `data/bronze`, los cuales son el resultado de la etapa de extracción.

### Transformaciones a realizar:

**7.1. Limpieza de datos:**  
   Eliminar valores nulos o aplicar reglas de manejo de los mismos, como imputación o eliminación de filas/columnas incompletas.

**7.2. Normalización:**  
   Estandarizar formatos de fechas, tipos de datos, y otros aspectos que aseguren consistencia en el conjunto de datos.

**7.3. Creación de claves de negocio:**  
   Generar una business key basada en una combinación de atributos clave, que permitirá identificar de manera única cada registro en el sistema de destino.

**7.4. Generación de hash:**  
   Crear un hash para el resto de las columnas con el objetivo de implementar una estrategia de carga incremental o full, comparando registros y detectando cambios o actualizaciones en los datos.


Una vez que se han leído y procesado los datos, y aplicadas las transformaciones pertinentes, los archivos resultantes deben depositarse en la carpeta `data/silver` para su posterior procesamiento en la etapa de carga.

### Otras sugerencias para esta etapa:
- **Validación de datos:** Implementar verificaciones adicionales para asegurar que los datos transformados cumplen con las expectativas y reglas de negocio antes de ser cargados en la base de datos.
- **Optimización de datos:** Aplicar técnicas para mejorar la eficiencia de las cargas posteriores, como compresión de archivos, particionamiento, o eliminación de redundancias innecesarias.
- **Control de versiones de datos:** Llevar un registro de los cambios y versiones de los archivos transformados, lo que ayudará a rastrear y auditar las modificaciones en el conjunto de datos a lo largo del tiempo.

---

## 8. Carga de datos en las Tablas de la Base de Datos

### Descripción General

En esta etapa se deben leer los archivos procesados y limpios que se encuentran en la carpeta `data/silver`, y cargar estos datos en las tablas correspondientes de la base de datos. El objetivo es que el modelo final sea capaz de responder a diferentes KPI del negocio.

### Pasos a Seguir

8.1. **Lectura de Archivos:**  
   Leer los archivos en `data/silver`, que ya han sido transformados, y mapearlos a las tablas correspondientes en la base de datos.

8.2. **Validación de Estructura:**  
   Verificar que los archivos tienen la estructura correcta, con las columnas y formatos adecuados, antes de proceder a la carga.

8.3. **Inserción en Tablas:**  
   - **Carga Full:** Eliminar los datos existentes y cargar los nuevos registros.
   - **Carga Incremental:** Actualizar registros existentes e insertar los nuevos registros, utilizando la business key o el hash generado.

8.4. **Manejo de Errores:**  
   Registrar y gestionar posibles conflictos como duplicados o errores de integridad referencial.

8.5. **Logs de Carga:**  
   Mantener un registro de la operación de carga, con información sobre registros insertados, actualizados y errores.


---

## 9. Requisitos Finales y Entregables

**9.1. La aplicación debe funcionar correctamente y estar parametrizada.**  
   La aplicación debe poder ser ejecutada en cualquier ordenador que contenga el entorno y los requerimientos necesarios para su ejecución. Además, se evaluará el uso de buenas practicas de programación y el uso de librerias de python.

**9.2. Separación de Etapas**

   Es necesario que el proceso se divida en tres etapas principales: **extracción**, **transformación** y **carga**. Cada una de estas etapas debe ser independiente y ejecutarse de manera modular. La aplicación principal (por ejemplo, `main.py`) debe recibir un parámetro que indique cuál de las etapas se desea ejecutar.

   - **Extracción**: Obtener los datos de las fuentes especificadas.
   - **Transformación**: Aplicar las reglas de negocio y preparar los datos.
   - **Carga**: Insertar los datos en la base de datos.

   Si no se especifica ninguna etapa, la aplicación debe ejecutar todas las etapas de manera secuencial (extracción, transformación y carga). Esto mejora la flexibilidad y permite ejecutar solo las partes necesarias del proceso según los requisitos específicos de cada caso.

   **Ejemplo de uso:**

   ```bash
   python main.py --stage source_extractor     # Ejecuta solo la extracción
   python main.py --stage transform_methods   # Ejecuta solo la transformación
   python main.py --stage load        # Ejecuta solo la carga
   python main.py   # Ejecuta todas las etapas por defecto (extracción, transformación y carga)
   ``` 

**9.3. Seguridad**

Asegúrate de que las credenciales de acceso, como contraseñas o tokens, no se expongan directamente en el código o en los logs. Utiliza variables de entorno o un gestor de secretos para mantener la seguridad de los datos sensibles.

**9.4. Eficiencia**

Asegúrate de que la aplicación pueda manejar grandes volúmenes de datos sin perder rendimiento. Implementa estrategias como:
- **Paginación:** Utiliza parámetros como `limit` y `offset` para controlar la cantidad de datos procesados en cada ejecución.
- **Paralelización:** Aprovecha múltiples procesos o hilos para mejorar el rendimiento.
- **Compresión de datos:** Comprime los archivos grandes cuando sea necesario para mejorar la eficiencia en la transmisión y el almacenamiento de los datos.

**9.5. Logging y auditoría**

Implementa un sistema de logging para registrar toda la traza de la ejecución del proyecto. Los archivos generados durante la ejecución deben depositarse en la carpeta `logs`. Es importante que los logs incluyan:
- **Errores**
- **Advertencias**
- **Eventos clave del proceso de ETL (Extracción, Transformación, Carga)**

Esto ayudará a identificar posibles problemas durante la ejecución y facilitará la auditoría del sistema.

**9.6. Documentación**

La documentación es clave en el desarrollo de software y en la implementación de procesos ETL. Asegúrate de documentar:
- El código de la aplicación.
- El proceso ETL.
- La configuración de la aplicación.

Es necesario completar el archivo `README_PROYECTO.md` con toda la información necesaria para la correcta ejecución del proyecto.

**9.7. Pruebas**

Realiza pruebas exhaustivas para asegurarte de que el proyecto se ejecuta correctamente y cumple con los requerimientos solicitados. Las pruebas deben cubrir:
- Funcionalidad básica de la aplicación.
- Rendimiento con grandes volúmenes de datos.
- Manejo de errores y excepciones.


## 10. Entrega y Live Demo

### 10.1 Entrega

El envío del proyecto debe realizarse en un archivo comprimido en formato `.zip`, que contenga todos los archivos necesarios para ejecutar el proyecto. El nombre del archivo debe seguir este formato:  
`vy-university-python-final-exam-<nombre-apellidos>.zip`

El archivo comprimido debe enviarse a las siguientes direcciones de correo: 
- Jesús Serrano: jesus.serrano@col.vueling.com
- Shamuel Manrique: shamuel.manrique@col.vueling.com
- Yu Ting Hu: yu_ting.hu@col.vueling.com
- Fernando Martínez: fernando.martinezm@col.vueling.com

El asunto del correo debe ser:
`Entrega Final - vy-university-python-final-<nombre-apellidos>`  

### 10.2 Live Demo
Se espera que los estudiantes realicen una **Live Demo** del proyecto en la que se ejecuten en vivo las etapas de extracción, transformación y carga (ETL) utilizando los datos provistos y el entorno configurado.

#### Requisitos para la Demo
**1. Preparación del Entorno**: La demo debe iniciar con el entorno configurado correctamente (contendores de Docker y Docker Compose en funcionamiento).
   
**2. Ejecución de las Etapas del ETL**:
   - **Extracción**: Demostrar la obtención de datos desde las fuentes especificadas (API y archivos locales).
   - **Transformación**: Aplicar las reglas de negocio y ajustes necesarios, mostrando cómo se estructuran los datos.
   - **Carga**: Insertar los datos transformados en la base de datos, explicando brevemente las estrategias de carga (full o incremental).

**3. Ejecución Secuencial**: Ejecutar el proceso completo desde el script `main.py` con el siguiente comando:
   ```bash
   python main.py
   ```
   Esto debe demostrar que las tres etapas (extracción, transformación y carga) funcionan de manera integrada.

**4. Manejo de Errores y Logs**: Explicar cómo el sistema maneja errores y registra los eventos en la carpeta logs.

**5.Explicación de Resultados**: Una vez finalizado el proceso, mostrar los datos cargados en la base de datos y explicar cómo estos datos podrían ser utilizados para responder a KPIs o preguntas de negocio específicas.

#### Duración de la Live Demo
La Live Demo durará aproximadamente 20 minutos. Durante la misma, es posible que se te hagan preguntas sobre el código, las decisiones técnicas tomadas, y cualquier problema o solución relevante para el proceso ETL.

Además, durante esta Live Demo, es posible que se te proporcionen nuevos datos de prueba para ejecutar el proceso en vivo.

