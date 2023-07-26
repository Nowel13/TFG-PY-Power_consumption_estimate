import csv
import pandas as pd
import time

# Mejorado por vectorizacion:
# def divide_time(time):
#     return time // 100, (time % 100 - 1) // 2


# def divide_time_data(datos):
#     data = datos.copy(deep=True)
#     data[['day', 'hour']] = data['Time'].apply(lambda x: pd.Series(divide_time(x)))
#     return data


# De esta forma se realiza la operacion a nivel de array en lugar de a nivel de fila, optimizando notablemente el tiempo:
def divide_time_data(datos):
    data = datos.copy(deep=True)
    data['day'] = data['Time'] // 100
    data['hour'] = (data['Time'] % 100 - 1) // 2
    return data


data1 = pd.read_csv("../../processed_files/Archivo1.txt", sep=' ')
data2 = pd.read_csv("../../processed_files/Archivo2.txt", sep=' ')
data3 = pd.read_csv("../../processed_files/Archivo3.txt", sep=' ')
data4 = pd.read_csv("../../processed_files/Archivo4.txt", sep=' ')
data5 = pd.read_csv("../../processed_files/Archivo5.txt", sep=' ')
data6 = pd.read_csv("../../processed_files/Archivo6.txt", sep=' ')


start_time = time.time()
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
clean_data = final_data[final_data['hour'] <= 23]

# Si deseamos eliminar las columnas Time, count_users y sum_kwh, descomentar las siguiente linea, sino, comentarla:
clean_data = clean_data.drop(["Time", "count_users", "sum_kwh"], axis = 1)

finish_time = time.time()

print("finished in: ", finish_time - start_time)
clean_data.to_csv("../../processed_files/AllData.txt", sep=" ", quoting=csv.QUOTE_NONE, escapechar=" ", index=False)

# Si hemos comentado lo anterior, descomentar la ultima:
# Creamos un txt donde guardar los datos para no tener que calcularlos cada vez:
# clean_data.to_csv("../processed_files/AllData.txt", sep=" ", quoting=csv.QUOTE_NONE, escapechar=" ", index=False)