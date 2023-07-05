import csv
import time
import sys
import datetime
import holidays
import pandas as pd
import sklearn

# De esta forma comprobamos si el dia elegido era un dia festivo en España:
# fecha in dias_festivos

# def add_day(date):
#     return date + datetime.timedelta(days=1)

# Para coger los datos de los 14 dias previos a los 3 dias anteriores al dado:
# def make_list(day):
#     days = (day - init_date).days
#     date_to_predict = calculate_date(days)
#     training_dates = []
#     for x in range(1,14):
#         new_date = (date_to_predict - datetime.timedelta(days=(3 + x)))
#         if new_date in dias_festivos:
#             if x < 7:
#                 new_date = new_date - datetime.timedelta(days=14)
#             else:
#                 new_date = new_date - datetime.timedelta(days=7)
#             if new_date.strftime("%Y-%m-%d") in training_dates:
#                 new_date = new_date - datetime.timedelta(days=7)
#         training_dates.append(new_date.strftime("%Y-%m-%d"))
#     return training_dates

# lista = make_list(fecha)

# training_days = []
# for i in lista:
#     training_days.append((datetime.datetime.strptime(i,"%Y-%m-%d").date() - init_date).days)

# print(training_days)

# Establecemos los días festivos para preparar los días a utilizar como prediccion:
dias_festivos = holidays.ES()

# Los datos comienzan a calcularse a partir del día 1 de enero del año 2009:
init_date = datetime.date(year=2009, month=1, day=1)

# A partir de este día podemos saber a qué día hace referencia cada uno de 
# los datos partiendo desde la fecha anteriormente iniciada:
def calculate_date(days):
    return init_date + datetime.timedelta(days=days)

# Escogemos el día del que sacaremos los datos para un primer intento 
# de predecir el consumo. Se busca el valor de todas las horas del mismo
# día de la semana anterior, si es fiesta, se sigue retrocediendo de 
# semana en semana hasta que no sea fiesta el día elegido:
def predict_data(day):
    days = (day - init_date).days
    date_to_predict = calculate_date(days)
    date_to_copy = date_to_predict - datetime.timedelta(days=7)
    while date_to_copy in dias_festivos:
        date_to_copy = date_to_copy - datetime.timedelta(days=7)
    return (date_to_copy - init_date).days 
   

# Aquí comienza la predicción:

# Recogemos los datos previamente preparados:
data = pd.read_csv("../processed_files/AllData.txt", sep=' ')

# Coger la ultima day del archivo de datos para saber si en el 
# bucle debo retroceder mas en el tiempo:
# max_date = data["day"]
# print(max_date)

param_date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()

# Elegimos una fecha aleatoria para realizar la predicción, en este
# caso, las dos semanas anteriores eran días festivos, por lo que se
# escogerá el consumo de hace 3 semanas: 
# fecha = calculate_date(372)
mae_list = []
for x in range(0,30):
    prediction_result = data[data["day"] == predict_data(param_date + datetime.timedelta(x))]
    real_result = data[data["day"] == ((param_date + datetime.timedelta(x)) -init_date).days]
    prediction = prediction_result[["mean_kwh","hour"]]
    reality = real_result[["mean_kwh","hour"]]
    lista_error = []
    for x in range(len(prediction)):
        lista_error.append(abs(prediction.iloc[x]["mean_kwh"] - reality.iloc[x]["mean_kwh"]))
    mae_list.append(sum(lista_error) / len(lista_error))

print(mae_list)
print(sum(mae_list) / len(mae_list))

# # Obtenemos el resultado de la predicción:
# prediction_result = data[data["day"] == predict_data(param_date)]
# real_result = data[data["day"] == (param_date-init_date).days]
# print(prediction_result[["mean_kwh","hour"]])
# print(real_result[["mean_kwh","hour"]])

# prediction = prediction_result[["mean_kwh","hour"]]
# reality = real_result[["mean_kwh","hour"]]
# lista_error = []
# for x in range(len(prediction)):
#     lista_error.append(abs(prediction.iloc[x]["mean_kwh"] - reality.iloc[x]["mean_kwh"]))

# # print(lista_error)
# print("MAE", param_date,"=>", sum(lista_error) / len(lista_error))
# # print(result[["mean_kwh","hour"]])