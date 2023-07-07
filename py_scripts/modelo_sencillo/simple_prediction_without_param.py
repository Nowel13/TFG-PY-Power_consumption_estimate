import csv
import datetime
import holidays
import pandas as pd

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
def predict_data(days):
    date_to_predict = calculate_date(days)
    date_to_copy = date_to_predict - datetime.timedelta(days=7)
    while date_to_copy in dias_festivos:
        date_to_copy = date_to_copy - datetime.timedelta(days=7)
    if (date_to_copy-init_date).days < 195:
        return days
    else:
        return (date_to_copy - init_date).days 
   

# TODO: Debería de poder coger los resultados que he estado calculando en cada predicción en lugar de seguir cogiendo los datos
# de consumo de la columna de datos reales? Por ejemplo si ya he predicho el día 7-6, al calcular el 14-6 debería coger el dato ya predicho?
def get_data(row):
    day = predict_data(row['day'])
    hour = row['hour']
    # pred = data.loc[(data['day'] == day) & (data['hour'] == hour), 'prediction'].iloc[0]
    # if pred == False:
    pred = data.loc[(data['day'] == day) & (data['hour'] == hour), 'mean_kwh'].iloc[0]
    return pred

# Aquí comienza la predicción:

# Recogemos los datos previamente preparados:
# data = pd.read_csv("../../processed_files/AllData.txt", sep=' ')
data = pd.read_csv("../../processed_files/AllData2.txt", sep=' ')

# Creamos la nueva columna con las predicciones vacía:
data['prediction'] = False
# Aplicamos la función del modelo simple para predecir todas las fechas posibles del dataFrame:
data['prediction'] = data.apply(get_data, axis=1)

# data.to_csv("../../result_files/BasePrediction.txt", sep=" ", quoting=csv.QUOTE_NONE, escapechar=" ", index=False)
data.to_csv("../../result_files/BasePrediction2.txt", sep=" ", quoting=csv.QUOTE_NONE, escapechar=" ", index=False)