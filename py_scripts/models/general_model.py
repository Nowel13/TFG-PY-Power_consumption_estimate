import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


def select_model(model_name, params):
    model = {}
    match model_name:
        case "random_forest":
            print(params)
        case "k_neighbors":
            print(params)
        case "voting":
            print(params)
    return model

def main(model_name, params):
    data = pd.read_csv("result_files/final_data.txt", sep=' ')
    to_predict = pd.read_csv("result_files/to_predict.txt", sep=' ')
    ###########################################
    ### Split data into features and labels ###
    ###########################################

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

    #################################################
    ### Split data into training and testing sets ###
    #################################################

    # Con ambos arrays, podemos hacer uso de sklearn dividir los datos en test y entrenamiento.
    # Se podría Utilizar un state definido (random_state=?) para que siempre nos genere los mismos datos y poder estudiar los resultados.
    train_features, test_features, train_labels, test_labels = train_test_split(features_array, labels, test_size = 0.25)

    model = select_model(model_name, params)


    # Entrenamos el modelo:
    model.fit(train_features, train_labels)

    # Realizamos las predicciones de los datos de test:
    predictions = model.predict(test_features)

    # Calculamos el error absoluto de todos los resultados de la predicción:
    errors = abs(predictions - test_labels)

    # Mostramos el MAE resultante de la media de todos los errores:
    print('Error absoluto medio (MAE):', np.mean(errors), 'kwh')

    # Calculamos la precisión del modelo:
    mape = 100 * (errors / test_labels)
    accuracy = 100 - np.mean(mape)

    print('Precisión del modelo:', accuracy, '%.')
    print('Precisión del modelo (2 decimales):', round(accuracy, 2), '%.')


    real_predictions = rf.predict(clean_to_predict)

    print(real_predictions)

    days = to_predict['day']
    hours = to_predict['hour']
    to_show = pd.DataFrame(data={
        "prediction": real_predictions
    })

    plt.figure()
    plt.plot(to_show.index, to_show['prediction'], 'b-', label="kwh")
    plt.xlabel('Hours from last day with data')
    plt.ylabel('Mean kwh for each user')
    plt.title('Predicted values for the next 3 days')
    plt.savefig('media/prediction.png')
