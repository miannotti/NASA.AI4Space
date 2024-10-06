import os
import pandas as pd


# Función para convertir valores numéricos a texto
def convert_numeric_to_text(df):
    # Convertir los valores numéricos a texto sin formato específico
    df['original_velocity_text'] = df['original_velocity'].apply(lambda x: f'{x:.25f}')

    # Aplicar el formato con 20 decimales a cada valor de la columna 'filtered_velocity'
    df['filtered_velocity_text'] = df['filtered_velocity'].apply(lambda x: f'{x:.25f}')

    return df


# Función para manejar los registros consecutivos en la columna 'prediction'
def optimize_prediction(df):
    for i in range(1, len(df)):
        if df.loc[i, 'prediction'] == 1 and df.loc[i - 1, 'prediction'] == 1:
            df.loc[i, 'prediction'] = 0
    return df


# Función para procesar todos los archivos CSV en un directorio
def process_directory(directory_path):
    # Recorrer recursivamente el directorio
    print("################################ Directorio:", directory_path)

    mseed_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.mseed')]
    print("################################ : archivo /t ", mseed_files)

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            print("################################ : archivo /t ", files)
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)

                # Leer el archivo CSV
                print(f"Procesando archivo: {file_path}")
                df = pd.read_csv(file_path)

                # Aplicar las funciones de procesamiento
                df = convert_numeric_to_text(df)
                df = optimize_prediction(df)

                # Seleccionar las columnas necesarias
                df_json = df[['minute', 'original_velocity_text', 'filtered_velocity_text', 'prediction']]
                print(df_json)


                # Generar el JSON
                json_output = df_json.to_json(orient='records', date_format='iso')

                # Guardar el archivo JSON
                output_json_path = file_path.replace('.csv', '.json')
                with open(output_json_path, 'w') as f:
                    f.write(json_output)

                print(f"Archivo JSON generado: {output_json_path}")


directory_path = r'/4.Etl/data/output_files_model/moon/S12_GradeB'  # Aquí puedes especificar tu directorio
process_directory(directory_path)
