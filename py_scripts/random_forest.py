import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# data = pd.read_csv("../result_files/BasePrediction.txt", sep=' ')
data = pd.read_csv("../result_files/BasePrediction2.txt", sep=' ')

###########################################
### Split data into features and labels ###
###########################################

# Creamos un array de numpy con la columna que se pretende predecir (llamada 'labels' o 'target'):
labels = np.array(data['mean_kwh'])

# Eliminamos del dataFrame las columnas que no se van a utilizar para el entrenamiento del modelo,
# en nuestro caso, solo necesitamos las columnas de Dia y Hora y la media de kwh:

# Si trabajamos con BasePrediction, usar la primera linea, si es BasePrediction2, la segunda:
# features = data.drop(['Time', 'sum_kwh', 'count_users', 'mean_kwh'], axis = 1)
features = data.drop(['mean_kwh'], axis = 1)

# Guardamos los nombres de las columnas para más tarde:
feature_list = list(features.columns)

# Con el nuevo dataFrame generado, creamos otro array de numpy para el entrenamiento:
features_array = np.array(features)

#################################################
### Split data into training and testing sets ###
#################################################

# Con ambos arrays, podemos hacer uso de sklearn dividir los datos en test y entrenamiento.
# Utilizaremos un state definido para que siempre nos genere los mismos datos y poder estudiar los resultados:
train_features, test_features, train_labels, test_labels = train_test_split(features_array, labels, test_size = 0.25, random_state = 5)

# Podemos comprobar que se han generado correctamente todas las variables con sus respectivos tamaños:
# print('Training Features Shape:', train_features.shape)
# print('Training Labels Shape:', train_labels.shape)
# print('Testing Features Shape:', test_features.shape)
# print('Testing Labels Shape:', test_labels.shape)

# Para poder utilizar una columna como comprobación o límite para saber si el modelo elegido va por buen camino o no,
# debemos de utilizar un modelo sencillo, como por ejemplo, usar el valor de la semana anterior (simple_prediction_without_param.py), para
# generar una nueva columna que nos dé algo donde fijarnos a la hora de evaluar el modelo:

# Podemos obtener todas las predicciones que realizamos mediante la predicción simple previa:
baseline_preds = test_features[:, feature_list.index('prediction')]
# Para calcular el error que tenemos de media en los 12864 datos:
baseline_errors = abs(baseline_preds - test_labels)

print('Average baseline error: ', np.mean(baseline_errors))
# El cual nos da un 0.06 kwh de error. Por lo que los nuevos modelos deben reducir este porcentaje de error.

########################
##### RANDOMFOREST #####
########################

rf = RandomForestRegressor(n_estimators = 1000, random_state = 5)

rf.fit(train_features, train_labels)
predictions = rf.predict(test_features)

errors = abs(predictions - test_labels)

print('Mean Absolute Error (MAE):', np.mean(errors), 'kwh')

mape = 100 * (errors / test_labels)
accuracy = 100 - np.mean(mape)

print('Accuracy (2 decimales):', round(accuracy, 2), '%.')

print('Accuracy:', accuracy, '%.')
