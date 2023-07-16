import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import datetime
import matplotlib.pyplot as plt

# data = pd.read_csv("../../result_files/BasePrediction.txt", sep=' ')
# data = pd.read_csv("../../result_files/BasePrediction2.txt", sep=' ')
data = pd.read_csv("../../result_files/transformed_data.txt", sep=' ')

###########################################
### Split data into features and labels ###
###########################################

# Creamos un array de numpy con la columna que se pretende predecir (llamada 'labels' o 'target'):
labels = np.array(data['mean_kwh'])

# Eliminamos del dataFrame las columnas que no se van a utilizar para el entrenamiento del modelo,
# en nuestro caso, solo necesitamos las columnas de Dia y Hora y la media de kwh:

# Si trabajamos con BasePrediction, usar la primera linea, si es BasePrediction2, la segunda:
# features = data.drop(['Time', 'sum_kwh', 'count_users', 'mean_kwh'], axis = 1)
# features = data.drop(['mean_kwh'], axis = 1)
features = data.drop(['mean_kwh', 'prediction', 'date'], axis = 1)

# Guardamos los nombres de las columnas para más tarde:
feature_list = list(features.columns)

# Con el nuevo dataFrame generado, creamos otro array de numpy para el entrenamiento:
features_array = np.array(features)

#################################################
### Split data into training and testing sets ###
#################################################

# Con ambos arrays, podemos hacer uso de sklearn dividir los datos en test y entrenamiento.
# Utilizaremos un state definido para que siempre nos genere los mismos datos y poder estudiar los resultados:
train_features, test_features, train_labels, test_labels = train_test_split(features_array, labels, test_size = 0.25)

########################
##### RANDOMFOREST #####
########################

rf = RandomForestRegressor(n_estimators = 1000)

rf.fit(train_features, train_labels)
predictions = rf.predict(test_features)

errors = abs(predictions - test_labels)

print('Mean Absolute Error (MAE):', np.mean(errors), 'kwh')

mape = 100 * (errors / test_labels)
accuracy = 100 - np.mean(mape)

print('Accuracy (2 decimales):', round(accuracy, 2), '%.')

print('Accuracy:', accuracy, '%.')


# init_date = datetime.datetime(year=2009, month=1, day=1, hour=0)

# def calculate_date(row):
#     return init_date + datetime.timedelta(days=int(row["day"]))

# def prepare_data(hour_filter):
#     data1 = data[data["hour"]==hour_filter]
#     labels1 = np.array(data[data['hour']==hour_filter]['mean_kwh'])
#     true_dates = data1.apply(calculate_date, axis=1)
#     true_data = pd.DataFrame(data= {
#         "date": true_dates,
#         "kwh": labels1
#     })
#     test_days = test_features[:, feature_list.index('day')]
#     test_hours = test_features[:, feature_list.index('hour')]
#     test_data = pd.DataFrame(data= {
#         "day": test_days,
#         "hour": test_hours,
#         "prediction": predictions
#     })
#     test_data = test_data[test_data["hour"]==hour_filter]
#     test_data["date"] = test_data.apply(calculate_date, axis=1)
#     test_data = test_data.drop(["day","hour"], axis=1)
#     plt.figure()
#     plt.plot(true_data['date'], true_data['kwh'], 'b-', label = 'kwh')
#     plt.plot(test_data['date'], test_data['prediction'], 'ro', label = 'prediction')
#     plt.xticks(rotation = 60)
#     plt.legend()
#     plt.xlabel('Date')
#     plt.ylabel('Mean Kwh')
#     plt.title('Actual and Predicted Values')


# # Podemos mostrar los graficos de los valores de las 24 horas por separado, pero por cuestiones de consumo de memoria, mostraremos solo 5:
# for x in range(0,5):
#     prepare_data(x)

# plt.show()


