import os
import csv
import time
import pandas as pd

# Mejorado por vectorizacion:
# def divide_time(time):
#     return time // 100, (time % 100 - 1) // 2

# def divide_time_data(datos):
#     data = datos.copy(deep=True)
#     data[['day', 'hour']] = data['Time'].apply(lambda x: pd.Series(divide_time(x)))
#     return data


# De esta forma (vectorización) se realiza la operacion a nivel de array en lugar de a nivel de fila, optimizando notablemente el tiempo:
def divide_time_data(datos):
    data = datos.copy(deep=True)
    data['day'] = data['Time'] // 100
    data['hour'] = (data['Time'] % 100 - 1) // 2
    return data

# Para poder llamar al método desde la api hemos creado un método main que recorre todos los ficheros que haya en la carpeta "files":
def main():
    start_time = time.time()
    path = "files/"
    data = None
    for root_folder, folders, files in os.walk(path):
        for file in files:
            data_x = pd.read_csv(path + file, sep=' ')
            if data is None:
                data = data_x.copy(deep=True)
            else:
                data = pd.concat([data,data_x])

    # Agrupamos los consumos totales por fecha:
    datos_agrupados = data.groupby("Time").sum().reset_index()

    # Calculamos las medias respecto al total de consumo por tramo horario y la cantidad de 
    # usuarios registrados en cada tramo:
    datos_agrupados["mean_kwh"] = datos_agrupados["sum_kwh"] / datos_agrupados["count_users"]

    # Creamos dos columnas para tener a mano los datos referentes al día y a la hora:
    data = divide_time_data(datos_agrupados)

    # Eliminamos la ultima fila que contiene datos que no pertenecen al estudio:
    final_data = data.iloc[:-1]

    # Eliminamos las filas que contengan valores de tiempo que excedan los límites:
    clean_data = final_data[final_data['hour'] <= 23]

    # Si deseamos eliminar las columnas Time, count_users y sum_kwh, descomentar las siguiente linea, sino, comentarla:
    clean_data = clean_data.drop(["Time", "count_users", "sum_kwh"], axis = 1)

    finish_time = time.time()

    print("finished in: ", finish_time - start_time)
    clean_data.to_csv("result_files/AllData.txt", sep=" ", quoting=csv.QUOTE_NONE, escapechar=" ", index=False)
