import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2 import OperationalError
from psycopg2.extras import execute_values
from obspy import read  # Para manejar archivos MiniSEED
from concurrent.futures import ThreadPoolExecutor

# Define los parámetros de conexión
db_name = "nasa"
db_user = "nasa"
db_password = "8=Ghr1ObOh`(shm1"
db_host = "35.193.192.225"  # e.g., "localhost" o una dirección IP
db_port = "5432"  # Puerto por defecto de PostgreSQL es 5432


# Función para establecer la conexión con PostgreSQL
def create_connection():
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        return connection
    except OperationalError as e:
        print(f"Error al conectar: '{e}'")
        return None


# Función para limpiar los nombres de las columnas
def clean_column_names(df):
    # Renombra las columnas reemplazando caracteres problemáticos
    df.columns = df.columns.str.replace(r'[^\w\s]', '', regex=True)  # Elimina caracteres no alfanuméricos
    df.columns = df.columns.str.replace(' ', '_')  # Reemplaza espacios con guiones bajos
    return df


# Función para cargar un archivo .csv en la tabla 'eventos'
def load_csv_file_to_table(file_path, table_name='mars_eventos', batch_size=2000):
    connection = create_connection()
    if connection is None:
        print(f"No se pudo establecer la conexión para el archivo {file_path}")
        return

    try:
        # Lee el archivo utilizando pandas
        df = pd.read_csv(file_path)

        # Limpia los nombres de las columnas
        df = clean_column_names(df)

        # Agrega una columna para el nombre del archivo y el nombre del directorio
        df['file_name'] = os.path.basename(file_path)
        df['directory_name'] = os.path.basename(os.path.dirname(file_path))
        df['planet'] = "Mars"


        # Convierte el DataFrame en una lista de tuplas
        records = df.values.tolist()

        # Divide los datos en bloques (paquetes) de tamaño batch_size
        num_records = len(records)
        for i in range(0, num_records, batch_size):
            batch_records = records[i:i + batch_size]

            # Genera la consulta SQL para insertar los datos en la tabla
            columns = df.columns
            query = sql.SQL('INSERT INTO {table} VALUES %s').format(
                table=sql.Identifier(table_name),
                fields=sql.SQL(',').join(map(sql.Identifier, columns))
            )

            # Cursor para ejecutar la inserción en la tabla
            cursor = connection.cursor()

            # Ejecuta la inserción del bloque de datos
            execute_values(
                cursor, query.as_string(connection), batch_records
            )
            connection.commit()  # Hace commit después de cada inserción de lote
            print(f"Se ha insertado un paquete de {len(batch_records)} registros para el archivo {file_path}.")

        print(f"Archivo '{file_path}' cargado exitosamente.")
    except Exception as e:
        print(f"Error al cargar el archivo '{file_path}': {e}")
    finally:
        connection.close()


# Función para cargar un archivo .mseed en la tabla 'metadata'
def load_mseed_file_to_table(file_path, table_name='mars_metadata'):
    connection = create_connection()
    if connection is None:
        print(f"No se pudo establecer la conexión para el archivo {file_path}")
        return

    try:
        # Leer el archivo .mseed utilizando obspy
        st = read(file_path)

        # Extraer metadatos de cada Trace (traza)
        metadata_records = []
        for tr in st:
            metadata = (
                tr.stats.network,         # Network code
                tr.stats.station,         # Station code
                tr.stats.location,        # Location code
                tr.stats.channel,         # Channel code
                tr.stats.starttime.datetime,  # Start time
                tr.stats.endtime.datetime,    # End time
                tr.stats.sampling_rate,   # Sampling rate
                tr.stats.npts,            # Number of points
                os.path.basename(file_path),  # File name
                os.path.basename(os.path.dirname(file_path)),  # Directory name
                'Mars'  # Valor constante para la columna 'planet'
            )
            metadata_records.append(metadata)

        # Genera la consulta SQL para insertar los datos en la tabla metadata
        query = sql.SQL('INSERT INTO {table} (network, station, location, channel, start_time, end_time, sampling_rate, npts, file_name, directory_name, planet) VALUES %s').format(
            table=sql.Identifier(table_name)
        )

        # Cursor para ejecutar la inserción en la tabla
        cursor = connection.cursor()

        # Ejecuta la inserción del bloque de metadatos
        execute_values(
            cursor, query.as_string(connection), metadata_records
        )
        connection.commit()  # Hace commit después de cada inserción
        print(f"Se han insertado los metadatos del archivo {file_path} en la tabla '{table_name}'.")

    except Exception as e:
        print(f"Error al cargar el archivo '{file_path}': {e}")
    finally:
        connection.close()


# Función para cargar un archivo de catálogo en la tabla 'catalogs'
def load_catalog_file_to_table(file_path, table_name='mars_catalogs', batch_size=2000):
    connection = create_connection()
    if connection is None:
        print(f"No se pudo establecer la conexión para el archivo {file_path}")
        return

    try:
        # Lee el archivo de catálogo utilizando pandas
        df = pd.read_csv(file_path)
        df['mq_type'] = ''
        df['planet'] = 'Mars'

        # Convierte el DataFrame en una lista de tuplas
        records = df.values.tolist()

        # Divide los datos en bloques (paquetes) de tamaño batch_size
        num_records = len(records)
        for i in range(0, num_records, batch_size):
            batch_records = records[i:i + batch_size]

            # Genera la consulta SQL para insertar los datos en la tabla de catálogo
            columns = df.columns
            query = sql.SQL('INSERT INTO {table} VALUES %s').format(
                table=sql.Identifier(table_name),
                fields=sql.SQL(',').join(map(sql.Identifier, columns))
            )

            # Cursor para ejecutar la inserción en la tabla
            cursor = connection.cursor()

            # Ejecuta la inserción del bloque de datos
            execute_values(
                cursor, query.as_string(connection), batch_records
            )
            connection.commit()  # Hace commit después de cada inserción de lote
            print(f"Se ha insertado un paquete de {len(batch_records)} registros del archivo de catálogo {file_path}.")

        print(f"Archivo de catálogo '{file_path}' cargado exitosamente.")
    except Exception as e:
        print(f"Error al cargar el archivo '{file_path}': {e}")
    finally:
        connection.close()


# Función para cargar archivos .csv en paralelo utilizando hilos
def load_csv_files_concurrently(directory_path, file_extension='csv', batch_size=1000, max_workers=4):
    files_to_process = []

    # Recorre todos los archivos y subdirectorios en el directorio de manera recursiva
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(f'.{file_extension}'):
                file_path = os.path.join(root, file)  # Obtén la ruta completa del archivo
                files_to_process.append(file_path)   # Agrega el archivo a la lista de archivos a procesar

    # Usa ThreadPoolExecutor para procesar los archivos en paralelo
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(load_csv_file_to_table, file_path, 'eventos', batch_size) for file_path in files_to_process]

        # Wait for all futures (tasks) to complete
        for future in futures:
            try:
                future.result()
            except Exception as exc:
                print(f"El archivo produjo una excepción: {exc}")


# Función para cargar archivos de catálogo en paralelo utilizando hilos
def load_catalog_files_concurrently(directory_path, file_extension='csv', batch_size=1000, max_workers=4):
    files_to_process = []

    # Recorre todos los archivos y subdirectorios en el directorio de manera recursiva
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(f'.{file_extension}'):
                file_path = os.path.join(root, file)  # Obtén la ruta completa del archivo
                files_to_process.append(file_path)   # Agrega el archivo a la lista de archivos a procesar

    # Usa ThreadPoolExecutor para procesar los archivos en paralelo
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(load_catalog_file_to_table, file_path, 'catalogs', batch_size) for file_path in files_to_process]

        # Wait for all futures (tasks) to complete
        for future in futures:
            try:
                future.result()
            except Exception as exc:
                print(f"El archivo de catálogo produjo una excepción: {exc}")


# Function to load .mseed files in parallel using threads.
def load_mseed_files_concurrently(directory_path, file_extension='mseed', max_workers=4):
    files_to_process = []

    # Traverse all files and subdirectories in the directory recursively
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(f'.{file_extension}'):
                file_path = os.path.join(root, file)
                files_to_process.append(file_path)

    # Use ThreadPoolExecutor to process the files in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(load_mseed_file_to_table, file_path, 'metadata') for file_path in files_to_process]

        # Wait for all futures (tasks) to complete
        for future in futures:
            try:
                future.result()
            except Exception as exc:
                print(f"El archivo produjo una excepción: {exc}")






def dataset_load_mars():
    connection = create_connection()

    if connection:
        # Loading the event catalog
        catalog_directory_path = '../mars/training/catalogs'
        load_catalog_files_concurrently(catalog_directory_path, file_extension='csv', batch_size=1000, max_workers=4)

        # Load event metadata
        mseed_directory_path = '../mars/training/data'
        load_mseed_files_concurrently(mseed_directory_path, file_extension='mseed', max_workers=40)

        # Load files with details of daily measurements
        csv_directory_path = '../mars/training/data'
        load_csv_files_concurrently(csv_directory_path, file_extension='csv', batch_size=2000, max_workers=30)


