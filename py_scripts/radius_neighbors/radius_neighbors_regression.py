import pandas as pd
import numpy as np
from sklearn.neighbors import RadiusNeighborsRegressor
from sklearn.model_selection import train_test_split

#### NEEDS TO CHECK ####

# data = pd.read_csv("../../result_files/transformed_data.txt", sep=' ')

# ###########################################
# ### Split data into features and labels ###
# ###########################################

# # Creamos un array de numpy con la columna que se pretende predecir (llamada 'labels' o 'target'):
# labels = np.array(data['mean_kwh'])

# # Eliminamos del dataFrame las columnas que no se van a utilizar para el entrenamiento del modelo,
# # en nuestro caso, solo necesitamos las columnas de Dia y Hora y la media de kwh:

# # Si trabajamos con BasePrediction, usar la primera linea, si es BasePrediction2, la segunda:
# features = data.drop(['mean_kwh', 'prediction', 'date'], axis = 1)

# # Guardamos los nombres de las columnas para más tarde:
# feature_list = list(features.columns)

# # Con el nuevo dataFrame generado, creamos otro array de numpy para el entrenamiento:
# features_array = np.array(features)

# #################################################
# ### Split data into training and testing sets ###
# #################################################

# # Con ambos arrays, podemos hacer uso de sklearn dividir los datos en test y entrenamiento.
# # Utilizaremos un state definido para que siempre nos genere los mismos datos y poder estudiar los resultados:
# train_features, test_features, train_labels, test_labels = train_test_split(features_array, labels, test_size = 0.80)

# rnn = RadiusNeighborsRegressor(radius=1.0)
# rnn.fit(train_features, train_labels)


# predictions = rnn.predict(test_features)

# errors = abs(predictions - test_labels)

# print('Mean Absolute Error (MAE):', np.mean(errors), 'kwh')

# mape = 100 * (errors / test_labels)
# accuracy = 100 - np.mean(mape)

# print('Accuracy (2 decimales):', round(accuracy, 2), '%.')

# print('Accuracy:', accuracy, '%.')