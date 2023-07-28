import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor

data = pd.read_csv("../../result_files/final_data.txt", sep=' ')

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

##################
##### VOTING #####
##################

estimator_1 = RandomForestRegressor(n_estimators=100)
estimator_2 = LinearRegression()
estimator_3 = KNeighborsRegressor()

# Creamos el modelo de Voting:
mlp = VotingRegressor(estimators=[('lr', estimator_1), ('rf', estimator_2), ('r3', estimator_3)])

# Entrenamos el modelo:
mlp.fit(train_features, train_labels)

# Realizamos las predicciones de los datos de test:
predictions = mlp.predict(test_features)

# Calculamos el error absoluto de todos los resultados de la predicción:
errors = abs(predictions - test_labels)

# Mostramos el MAE resultante de la media de todos los errores:
print('Error absoluto medio (MAE):', np.mean(errors), 'kwh')

# Calculamos la precisión del modelo:
mape = 100 * (errors / test_labels)
accuracy = 100 - np.mean(mape)

print('Precisión del modelo:', accuracy, '%.')
print('Precisión del modelo (2 decimales):', round(accuracy, 2), '%.')

#################################
#################################
### Para mostrar las gráficas:###
#################################
#################################
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
