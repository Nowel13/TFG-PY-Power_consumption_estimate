import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

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

###############################
##### MULTIPLE REGRESSION #####
###############################

# Generamos el modelo:
rf = linear_model.LinearRegression()

rf.fit(train_features, train_labels)

predictions = rf.predict(test_features)

# Mostramos los coeficientes calculados que se aplican a las variables del modelo:
print("Coefficients: \n", rf.coef_)

# Obtenemos el error cuadrático medio, el cual nos indica lo siguiente:
# Si es cercano a 0, el modelo no representa una relación correcta entre variables.
# Si es cercano a 1, el modelo representa una relación acertada entre variables.
print("Mean squared error: %.4f" % mean_squared_error(test_labels, predictions))

# Coeficiente de determinación:
print("Coefficient of determination: %.4f" % r2_score(test_labels, predictions))

# Calculo de MAE y accuracy como en los demás modelos:
errors = abs(predictions - test_labels)

print('Error absoluto medio (MAE):', np.mean(errors), 'kwh')
print(np.mean(errors))

mape = 100 * (errors / test_labels)
accuracy = 100 - np.mean(mape)

print('Precisión del modelo:', accuracy, '%.')

print('Precisión del modelo (2 decimales):', round(accuracy, 2), '%.')