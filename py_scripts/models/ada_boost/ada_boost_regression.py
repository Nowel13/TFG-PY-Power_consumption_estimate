import pandas as pd
import numpy as np
from sklearn.ensemble import AdaBoostRegressor
from sklearn.model_selection import train_test_split

data = pd.read_csv("../../data/final_files/final_data.txt", sep=' ')

###########################################
### Split data into features and labels ###
###########################################

# Creamos un array de numpy con la columna que se pretende predecir (llamada 'labels' o 'target'):
labels = np.array(data['mean_kwh'])

# Eliminamos del dataFrame las columnas que no se van a utilizar para el entrenamiento del modelo,
# en este caso, la columna objectivo, y las columnas de dia y hora:
features = data.drop(['mean_kwh', 'day', 'hour'], axis = 1)

# Guardamos los nombres de las columnas por si queremos mostrar los datos en gráficas:
# feature_list = list(features.columns)

# Con el nuevo dataFrame generado, creamos otro array de numpy para el entrenamiento:
features_array = np.array(features)

#################################################
### Split data into training and testing sets ###
#################################################

# Con ambos arrays, podemos hacer uso de sklearn dividir los datos en test y entrenamiento.
# Se podría Utilizar un state definido (random_state=?) para que siempre nos genere los mismos datos y poder estudiar los resultados.
train_features, test_features, train_labels, test_labels = train_test_split(features_array, labels, test_size = 0.25)

# Construimos el modelo con los siguientes parámetros:
    # n_estimators = El número de estimadores que se van a utilizar

knn = AdaBoostRegressor(n_estimators=10)

knn.fit(train_features, train_labels)

predictions = knn.predict(test_features)

errors = abs(predictions - test_labels)

print('Error absoluto medio (MAE):', np.mean(errors), 'kwh')

mape = 100 * (errors / test_labels)
accuracy = 100 - np.mean(mape)

print('Precisión del modelo:', accuracy, '%.')

print('Precisión del modelo (2 decimales):', round(accuracy, 2), '%.')