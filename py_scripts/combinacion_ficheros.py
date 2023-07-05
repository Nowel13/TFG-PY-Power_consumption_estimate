import csv
import time
import pandas as pd


def divide_time(time):
    return time // 100, (time % 100 - 1) // 2


def divide_time_data(datos):
    data = datos.copy(deep=True)
    data[['Date', 'Hour']] = data['Time'].apply(lambda x: pd.Series(divide_time(x)))
    return data


data1 = pd.read_csv("../processed_files/Archivo1.txt", sep=' ')
data2 = pd.read_csv("../processed_files/Archivo2.txt", sep=' ')
data3 = pd.read_csv("../processed_files/Archivo3.txt", sep=' ')
data4 = pd.read_csv("../processed_files/Archivo4.txt", sep=' ')
data5 = pd.read_csv("../processed_files/Archivo5.txt", sep=' ')
data6 = pd.read_csv("../processed_files/Archivo6.txt", sep=' ')

# Unimos los datos de todos los ficheros de consumo:
data = pd.concat([data1, data2, data3, data4, data5, data6])

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
clean_data = final_data[final_data['Hour'] <= 23]

# Creamos un txt donde guardar los datos para no tener que calcularlos cada vez:
clean_data.to_csv("../processed_files/AllData.txt", sep=" ", quoting=csv.QUOTE_NONE, escapechar=" ", index=False)
