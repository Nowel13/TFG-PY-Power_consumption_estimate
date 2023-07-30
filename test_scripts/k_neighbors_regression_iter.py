import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
import time

# Con este script podemos comparar rápidamente qué parámetros son necesarios en la creación del modelo para optimizar
# los resultados obtenidos con las distintas variables:

maes = []
times = []
accuracys = []
n = [5, 6, 7, 8, 9]
typ = ["distance", "uniform"]

for u in n:
    for o in typ:
        for i in range(0,5):
            start_time = time.time()

            data = pd.read_csv("../data/final_files/final_data.txt", sep=' ')

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

            knn = KNeighborsRegressor(n_neighbors=u, weights=o)

            knn.fit(train_features, train_labels)

            predictions = knn.predict(test_features)

            errors = abs(predictions - test_labels)

            maes.append(np.mean(errors))

            mape = 100 * (errors / test_labels)
            
            accuracy = 100 - np.mean(mape)

            finish_time = time.time()

            times.append(finish_time - start_time)

            accuracys.append(accuracy)

        print("n_neighbors:", u, "weights:", o)

        print("mae")
        for a in maes:
            print(a)
        maes = []
        print("time")
        for a in times:
            print(a)
        times = []
        print("accuracy")
        for a in accuracys:
            print(a)
        accuracys = []
        print()
