import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import datetime
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# data = pd.read_csv("../result_files/BasePrediction.txt", sep=' ')
# data = pd.read_csv("../result_files/BasePrediction2.txt", sep=' ')
data = pd.read_csv("../../result_files/transformed_data.txt", sep=' ')

###########################################
### Split data into features and labels ###
###########################################

# Creamos un array de numpy con la columna que se pretende predecir (llamada 'labels' o 'target'):
labels = np.array(data['mean_kwh'])

# Eliminamos del dataFrame las columnas que no se van a utilizar para el entrenamiento del modelo,
# en nuestro caso, solo necesitamos las columnas de Dia y Hora y la media de kwh:

features = data.drop(['mean_kwh', 'prediction', 'date'], axis = 1)

# En caso de querer escalar las variables utilizar la siguiente variable. En este caso no es útil:
# scale = StandardScaler()

# Guardamos los nombres de las columnas para más tarde:
feature_list = list(features.columns)

# Con el nuevo dataFrame generado, creamos otro array de numpy para el entrenamiento:
features_array = np.array(features)

#################################################
### Split data into training and testing sets ###
#################################################

# Con ambos arrays, podemos hacer uso de sklearn dividir los datos en test y entrenamiento.
# Utilizaremos un state definido para que siempre nos genere los mismos datos y poder estudiar los resultados:
train_features, test_features, train_labels, test_labels = train_test_split(features_array, labels, test_size = 0.25, random_state = 1)

###############################
##### MULTIPLE REGRESSION #####
###############################

rf = linear_model.LinearRegression()

rf.fit(train_features, train_labels)

predictions = rf.predict(test_features)

print("Coefficients: \n", rf.coef_)
# Obtenemos el error cuadrático medio, el cual nos indica lo siguiente:
# Si es cercano a 0, el modelo no representa una relación correcta entre variables.
# Si es cercano a 1, el modelo representa una relación acertada entre variables.
print("Mean squared error: %.2f" % mean_squared_error(test_labels, predictions))

# Los coeficientes que se aplican a las variables del modelo:
print("Coefficient of determination: %.2f" % r2_score(test_labels, predictions))

# Calculo de MAE y accuracy como en los demás modelos:
errors = abs(predictions - test_labels)

print('Mean Absolute Error (MAE):', np.mean(errors), 'kwh')

mape = 100 * (errors / test_labels)
accuracy = 100 - np.mean(mape)

print('Accuracy (2 decimales):', round(accuracy, 2), '%.')

print('Accuracy:', accuracy, '%.')