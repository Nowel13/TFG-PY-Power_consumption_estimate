import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import RadiusNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import StackingRegressor
from sklearn.ensemble import VotingRegressor


def select_model(model_name):
    model = {}
    estimator_1 = RandomForestRegressor(n_estimators=100)
    estimator_2 = LinearRegression()
    estimator_3 = KNeighborsRegressor()
    n_estimators = 100
    n_neighbors = 5
    weights = 'distance'
    match model_name:
        case "ada_boost":
            model = AdaBoostRegressor(n_estimators = n_estimators)
        case "bagging":
            model = BaggingRegressor(n_estimators = n_estimators)
        case "extra_trees":
            model = ExtraTreesRegressor(n_estimators = n_estimators)
        case "gradient_boosting":
            model = GradientBoostingRegressor()
        case "k_neighbors":
            model = KNeighborsRegressor(n_neighbors = n_neighbors, weights = weights)
        case "linear_regression":
            model = LinearRegression()
        case "neural_network":
            model = MLPRegressor()
        case "radius_neighbors":
            model = RadiusNeighborsRegressor(radius=1)
        case "random_forest":
            model = RandomForestRegressor(n_estimators = n_estimators)
        case "stacking":
            model = StackingRegressor(estimators=[('lr', estimator_1), ('rf', estimator_2), ('r3', estimator_3)])
        case "voting":
            model = VotingRegressor(estimators=[('lr', estimator_1), ('rf', estimator_2), ('r3', estimator_3)])
        case _:
            model = RandomForestRegressor(n_estimators = n_estimators)
    return model

def main(model_name):
    data = pd.read_csv("data/final_files/final_data.txt", sep=' ')
    to_predict = pd.read_csv("data/final_files/to_predict.txt", sep=' ')
    ##############################################################
    ### Dividir datos entre variables independientes y targets ###
    ##############################################################

    # Creamos un array de numpy con la columna que se pretende predecir (llamada 'labels' o 'target'):
    labels = np.array(data['mean_kwh'])

    # Eliminamos del dataFrame las columnas que no se van a utilizar para el entrenamiento del modelo,
    # en este caso, la columna objectivo, y las columnas de dia y hora:
    features = data.drop(['mean_kwh', 'day', 'hour'], axis = 1)
    clean_to_predict = to_predict.drop(['day', 'hour'], axis = 1)

    # Guardamos los nombres de las columnas por si queremos mostrar los datos en gráficas:
    # feature_list = list(features.columns)
    # to_predict_list = list(to_predict.columns)

    # Con el nuevo dataFrame generado, creamos otro array de numpy para el entrenamiento:
    features_array = np.array(features)

    ################################################
    ### Dividir datos de entrenamiento y pruebas ###
    ################################################

    # Con ambos arrays, podemos hacer uso de sklearn dividir los datos en test y entrenamiento.
    # Se podría Utilizar un state definido (random_state=?) para que siempre nos genere los mismos datos y poder estudiar los resultados.
    train_features, test_features, train_labels, test_labels = train_test_split(features_array, labels, test_size = 0.25)

    # Seleccionamos el modelo a utilizar mediante los parámetros pasados a la función:
    model = select_model(model_name)

    # Entrenamos el modelo:
    model.fit(train_features, train_labels)

    # Realizamos las predicciones de los datos de test:
    predictions = model.predict(test_features)

    # Realizamos las predicciones de los datos esperados:
    real_predictions = model.predict(clean_to_predict)

    # Calculamos el error absoluto de todos los resultados de la predicción de test:
    errors = abs(predictions - test_labels)

    # Mostramos el MAE resultante de la media de todos los errores:
    print('Error absoluto medio (MAE):', np.mean(errors), 'kwh')

    # Calculamos la precisión del modelo:
    mape = 100 * (errors / test_labels)
    accuracy = 100 - np.mean(mape)

    print('Precisión del modelo:', accuracy, '%.')
    print('Precisión del modelo (2 decimales):', round(accuracy, 2), '%.')

    # Mostramos los resultados obtenidos para los 3 siguientes días:
    print(real_predictions)

    result_dataframe = pd.DataFrame(data={
        "day": to_predict['day'],
        "hour": to_predict['hour'],
        "prediction": real_predictions
    })
    
    # Modificamos el dataframe de resultados para ayudar a su muestra en el lado del front:
    result_dataframe = result_dataframe.pivot(index="hour", columns="day", values="prediction")

    # Escribimos los resultados de las predicciones en un csv:
    result_dataframe.to_csv('data/results/prediction.txt', sep=' ', quoting=csv.QUOTE_NONE, escapechar=' ', index=True)

    # Generamos la gráfica con los resultados de las predicciones:
    plt.figure()
    plt.plot(list(range(len(real_predictions))), real_predictions, 'b-', label="kwh")
    plt.xlabel('Hours from last day with data')
    plt.ylabel('Mean kwh for each user')
    plt.title(f'Predicted values for the next 3 days with {model_name}')
    plt.savefig('data/results/prediction.png')
