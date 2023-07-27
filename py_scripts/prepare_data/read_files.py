import os
import csv
import time
import numpy as np
import pandas as pd

# Lectura del documento, se pasa la ruta del archivo como parámetro:
def read_file(pathname):
    print("Comienza la lectura del archivo: ", pathname)
    start_read_time = time.time()
    data = pd.read_csv(
        pathname,
        sep=' ',
        header=None, 
        names=['MeterID', 'Time', 'kwh']
                    )
    finish_read_time = time.time()
    print("Ha tardado: ", finish_read_time - start_read_time, " en leer el archivo csv.")
    return data

# Transforma todos los datos de tiempo del archivo leído con la función definida anteriormente:
# Actualización: ----------------------
# Gracias a la vectorización, podemos aplicar la función a nivel de array en lugar de fila, lo
# que supone un aumento del rendimiento de prácticamente un 90%:
def transform_data(datos):
    start_time = time.time()
    datos['Time'] = np.where(datos['Time'] % 2 == 0, datos['Time'] - 1, datos['Time'])
    finish_time = time.time()
    print("Ha tardado: ", finish_time - start_time, " en transformar los datos de tiempo.")
    return datos

# Agrupamos los datos por usuario y marca de tiempo, para que se junten los pares de valores de cada hora.
# Añadimos a la agrupación los parámetros "sort=False" para mejorar el rendimiento de la función y 
# llamamos a reset_index() para mantener las columnas previas y que no se formen varios subíndices.
# Actualización: ---------------------
# Hemos añadido una columna "half_hours", la cual nos indica si se han agrupado 1 o 2 medias horas,
# de esta forma detectamos las horas incompletas de datos.
def group_data_per_user(datos):
    start_time = time.time()
    datos = datos.groupby(["MeterID","Time"], sort=False).agg(kwh=("kwh", "sum"), half_hours=("kwh","count")).reset_index()
    finish_time = time.time()
    print("ha tardado: ", finish_time - start_time, " en agrupar por usuario y marca de tiempo.")
    return datos


# Corrige los datos que cuentan con solo media hora multiplicando sus valores por 2
# y eliminamos la columna ahora que no es necesaria para liberar algo de memoria:
def prepare_column(datos):
    start_time = time.time()
    datos.loc[datos["half_hours"] == 1, "kwh"] *= 2
    datos = datos.drop(["half_hours"], axis=1)
    finish_time = time.time()
    print("ha tardado: ", finish_time - start_time, " en corregir los datos incompletos.")
    return datos

# Agrupamos los datos por marca de tiempo, de forma que se sumen todos los valores de kwh y el número de usuarios con registros
# de consumo en cada marca de tiempo:
def group_data_per_time(datos):
    start_time = time.time()
    datos = datos.groupby("Time").agg(sum_kwh=("kwh", "sum"), count_users=("kwh","count")).reset_index()
    finish_time = time.time()
    print("ha tardado: ", finish_time - start_time, " en agrupar por tiempo.")
    return datos


# Escribimos el dataFrame resultante en un csv para poder usarlo más tarde:
def write_on_csv(datos, name):
    start_time = time.time()
    datos.to_csv(name, sep=" ", quoting=csv.QUOTE_NONE, escapechar=" ", index=False)
    finish_time = time.time()
    print("Ha tardado: ", finish_time - start_time, " en escribir el archivo csv: ", name)


# Preparamos un nuevo documento de nombre "name", con todas las transformaciones anteriores para el archivo pasado en el pathname:
def prepare_file(pathname, name):
    datos = read_file(pathname)
    datos_transformados = transform_data(datos)
    datos_agrupados_por_usuario = group_data_per_user(datos_transformados)
    datos_arreglados = prepare_column(datos_agrupados_por_usuario)
    datos_finales = group_data_per_time(datos_arreglados)
    write_on_csv(datos_finales, name)


##########################################
################## MAIN ##################
##########################################

def main():
    path = 'data_files/'
    # Cuando deje de hacer pruebas, la lectura de ficheros deberá realizarse desde esta otra carpeta, 
    # que es donde se almacenan los archivos que se suban con la API (comentar la linea anterior y descomentar la siguiente):
    # path = 'files/'
    result_path = 'processed_files/'
    for root_folder, folders, files in os.walk(path):
        for file in files:
            prepare_file(path + file, result_path + file)
            print("Finished file: " + file)


##########################################
################ END MAIN ################
##########################################


##########################################
##########################################
##########################################
##########################################

# Código usado para llegar hasta el resultado anterior:

##########################################
##########################################
##########################################
##########################################



# for i in range(6):
#     pathname = "../../data_files/File" + str(i+1) + ".txt"
#     name = "../../processed_files/Archivo" + str(i+1) + ".txt"
#     prepare_file(pathname, name)

# Divide la columna tiempo en dos partes, los primeros 3 digitos indican el día y los dos últimos el tramo horario:
# Con esta opción tarda un poco menos que con la de abajo:
# def divide_time(time):
#     return time // 100, time % 100

# Tiene el mismo objetivo que la función anterior pero para datos que sean de tipo "string" en lugar de "integer":
# def divide_time_str(time):
#     str_time = str(time)
#     return int(str_time[:3]), int(str_time[3:])




# Dividimos las marcas de tiempo en dias y horas a partir de la columna "Time".
# (divide_time()) => Esta opción tarda menos que pasando los datos a string, dividiendolos y volviendolos a pasar a int.
# Además, existen registros de tiempo erróneos que superan las 24 horas de un día normal, por lo que filtramos para eliminar
# los datos que superen las 23:00(>47 en la columna "hour"):
# def divide_time_data(datos):
#     print("Divide la columna Time en dos subcolumnas con los días y las horas:")
#     start_time = time.time()
#     data = datos.copy(deep=True)
#     data[['day', 'hour']] = data['Time'].apply(lambda x: pd.Series(divide_time(x)))
#     filtered_data = data[data['hour'] <= 47]
#     finish_time = time.time()
#     print("Ha tardado: ", finish_time - start_time)
#     return filtered_data


# Misma opción pero pasando los datos de tiempo a string (resulta más lento a la hora de la ejecución):
# def divide_time_data_2(datos):
#     print("Divide la columna Time en dos subcolumnas con los días y las horas:")
#     start_time = time.time()
#     data = datos.copy(deep=True)
#     data[['day', 'hour']] = data['Time'].apply(lambda x: pd.Series(divide_time_str(x)))
#     finish_time = time.time()
#     print("Ha tardado: ", finish_time - start_time)
#     return data



# print("Agrupa los datos por usuario y tramo horario:")
# start_groupby_time = time.time()
# # Añadimos a la agrupación los parámetros "sort=False" para mejorar el rendimiento de la función y 
# # llamamos a reset_index() para mantener las columnas previas y que no se formen varios índices:
# datos_agrupados = datos.groupby(["MeterID","Time"], sort=False).sum().reset_index()
# finish_groupby_time = time.time()
# print("Acaba la agrupación de datos")
# print("Ha tardado: ", finish_groupby_time - start_groupby_time)


# print("Agrupa los datos por tramo horario y cuenta los usuarios que se han sumado en cada tramo:")
# start_finalize_time = time.time()
# datos_finales = datos_agrupados.groupby("Time").agg(sum_kwh=("kWh", "sum"), mean_kwh=("kWh","mean"), count_users=("kWh","count")).reset_index()
# finish_finalize_time = time.time()
# print("Acaba la agrupación final de datos")
# print("Ha tardado: ", finish_finalize_time - start_finalize_time)

# # print(datos_finales)

# print("Escribe el archivo de text con la agrupación final: ")

# start_writing_time = time.time()
# datos_finales.to_csv('prueba.txt', sep=" ", quoting=csv.QUOTE_NONE, escapechar=" ")
# finish_writing_time = time.time()

# print("Acaba la escritura del archivo: ")
# print("Ha tardado: ", finish_writing_time - start_writing_time)

# # print(data['MeterID'])
# # print(data)
# # print(datos_agrupados)

# # data[['day', 'hour']] = data['Time'].apply(lambda x: pd.Series(divide_time(x)))
# print("ACABA EL ARCHIVO DE PYTHON")

# # def calculate_agrupados(datos):
# #     start_transform_time = time.time()
# #     datos_agrupados = datos.groupby(["MeterID","Time"]).sum()
#     finish_transform_time = time.time()
#     print("ha tardado: ", finish_transform_time - start_transform_time)
#     print(datos_agrupados)
#     start_time = time.time()
#     datos_agrupados2 = datos.groupby(["MeterID","Time"], sort=False).sum()
#     finish_time = time.time()
#     print("ha tardado: ", finish_time - start_time)
#     print(datos_agrupados2)


# def calculate_agrupados_2(datos):
#     start_transform_time = time.time()
#     datos_agrupados = datos.groupby(["MeterID","Time"]).sum()
#     finish_transform_time = time.time()
#     print("ha tardado: ", finish_transform_time - start_transform_time)
#     print(datos_agrupados)
#     start_time = time.time()
#     datos_agrupados2 = datos.groupby(["MeterID","Time"], as_index=False).sum()
#     finish_time = time.time()
#     print("ha tardado: ", finish_time - start_time)
#     print(datos_agrupados2)


# def calculate_agrupados_3(datos):
#     start_transform_time = time.time()
#     datos_agrupados = datos.groupby(["MeterID","Time"]).sum()
#     finish_transform_time = time.time()
#     print("ha tardado: ", finish_transform_time - start_transform_time)
#     print(datos_agrupados)
#     start_time = time.time()
#     datos_agrupados2 = datos.groupby(["MeterID","Time"], sort=False, as_index=False).sum()
#     finish_time = time.time()
#     print("ha tardado: ", finish_time - start_time)
#     print(datos_agrupados2)


# def calculate_agrupados_4(datos):
#     start_transform_time = time.time()
#     datos_agrupados = datos.groupby(["MeterID","Time"]).sum()
#     finish_transform_time = time.time()
#     print("ha tardado: ", finish_transform_time - start_transform_time)
#     print(datos_agrupados)
#     start_time = time.time()
#     datos_agrupados2 = datos.groupby(["MeterID","Time"], sort=False).sum().reset_index()
#     finish_time = time.time()
#     print("ha tardado: ", finish_time - start_time)
#     print(datos_agrupados2)


# def calculate_agrupados_final(datos):
#     start_transform_time = time.time()
#     datos_finales = datos.groupby("Time").aggregate(['sum', 'mean', 'count'])
#     finish_transform_time = time.time()
#     print("ha tardado: ", finish_transform_time - start_transform_time)
#     print(datos_finales)
#     start_time = time.time()
#     datos_finales2 = datos.groupby("Time", as_index=False).aggregate(['sum', 'mean', 'count'])
#     finish_time = time.time()
#     print("ha tardado: ", finish_time - start_time)
#     print(datos_finales2)


# def calculate_agrupados_final_2(datos):
#     start_transform_time = time.time()
#     datos_finales = datos.groupby("Time").aggregate(['sum', 'mean', 'count'])
#     finish_transform_time = time.time()
#     print("ha tardado: ", finish_transform_time - start_transform_time)
#     print(datos_finales)
#     start_time = time.time()
#     datos_finales2 = datos.groupby("Time", sort=False).aggregate(['sum', 'mean', 'count'])
#     finish_time = time.time()
#     print("ha tardado: ", finish_time - start_time)
#     print(datos_finales2)


# def calculate_agrupados_final_3(datos):
#     start_transform_time = time.time()
#     datos_finales = datos.groupby("Time", as_index=False).aggregate(['sum', 'mean', 'count'])
#     finish_transform_time = time.time()
#     print("ha tardado: ", finish_transform_time - start_transform_time)
#     print(datos_finales)
#     start_time = time.time()
#     datos_finales2 = datos.groupby("Time", sort=False, as_index=False).aggregate(['sum', 'mean', 'count'])
#     finish_time = time.time()
#     print("ha tardado: ", finish_time - start_time)
#     print(datos_finales2)


# def calculate_agrupados_final_4(datos):
#     start_transform_time = time.time()
#     datos_finales2 = datos.groupby("Time", sort=False, as_index=False).aggregate(['sum', 'mean', 'count'])
#     finish_transform_time = time.time()
#     print("ha tardado: ", finish_transform_time - start_transform_time)
#     print(datos_finales)
#     start_time = time.time()
#     datos_finales2 = datos_agrupados.groupby("Time").agg(sum_kwh=("kWh", "sum"), mean_kwh=("kWh","mean"), count_users=("kWh","count")).reset_index()
#     finish_time = time.time()
#     print("ha tardado: ", finish_time - start_time)
#     print(datos_finales2)




# # datos_finales = datos_agrupados.groupby("Time").agg(sum=(pd.NamedAgg(column="kWh", aggfunc="sum")), mean=pd.NamedAgg(column="kWh", aggfunc="mean"), count=pd.NamedAgg(column="kWh", aggfunc="count"))
# datos_finales = datos_agrupados.groupby("Time").agg(sum=("kWh", "sum"), mean=("kWh","mean"), count=("kWh","count"))

