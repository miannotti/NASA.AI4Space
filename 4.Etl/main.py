import asyncio
import psycopg2

from fastapi import FastAPI, WebSocket
from psycopg2 import sql
from datetime import datetime, timedelta


# Configuración de la base de datos PostgreSQL
db_name = "nasa"
db_user = "nasa"
db_password = "8=Ghr1ObOh`(shm1"
db_host = "35.193.192.225"
db_port = "5432"  # Puerto predeterminado de PostgreSQL

# Crear una instancia de FastAPI
app = FastAPI()


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
    except psycopg2.OperationalError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None


# Función para obtener datos de la base de datos dentro de un rango de tiempo
def get_data_from_db(start_time, end_time):
    connection = create_connection()
    if connection is None:
        return []

    cursor = connection.cursor()

    # Consulta para obtener datos en el rango de tiempo especificado
    query = sql.SQL("""
        SELECT time_abs, time_rel, velocity, file_name, directory_name
        FROM eventos
        WHERE time_abs BETWEEN %s AND %s
        ORDER BY time_abs ASC;
    """)

    cursor.execute(query, (start_time, end_time))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    # Transformar los datos en un formato más fácil de enviar (convirtiendo time_abs a string)
    data = [{"time_abs": row[0].isoformat(),  # Convertir datetime a string en formato ISO
             "time_rel": row[1],
             "velocity": row[2],
             "file_name": row[3],
             "directory_name": row[4]} for row in rows]
    return data


# @4.Etl.get("/data")
# async def get_data():
#     moon = dataset_load_moon()
#     mars = dataset_load_mars()
#
#     mars_len = len(mars)
#
#     return {"Result": "All data has been procesed"}


# Endpoint WebSocket para simular datos en tiempo real basados en segmentos de tiempo
@app.websocket("/ws/realtime")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Define una fecha inicial (por ejemplo, 1970-01-19 20:00:00)
    start_time = datetime(1970, 1, 19, 20, 0, 0)

    # Define el incremento de tiempo (en minutos) para cada segmento de datos
    time_increment = timedelta(minutes=5)

    try:
        while True:
            # Define el tiempo final basado en el incremento
            end_time = start_time + time_increment

            # Obtener los datos de la base de datos para el rango de tiempo
            data = get_data_from_db(start_time, end_time)

            # Enviar los datos a través del WebSocket
            await websocket.send_json(data)

            # Mover el rango de tiempo para la siguiente iteración
            start_time = end_time

            # Esperar 2 segundos antes de enviar los siguientes datos (simulación de tiempo real)
            await asyncio.sleep(2)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()
