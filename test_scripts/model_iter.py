import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
import time

# Con este script podemos comparar rápidamente qué parámetros son necesarios en la creación del modelo para optimizar
# los resultados obtenidos con las distintas variables:

mean_maes = []
mean_times = []
mean_accuracys = []

maes = []
times = []
accuracys = []

n = [5, 6, 7, 8, 9]
typ = ["distance", "uniform"]

for u in n:
    for o in typ:
        for i in range(0,5):
            start_time = time.time()

            data = pd.read_csv("data/final_files/final_data.txt", sep=' ')

            labels = np.array(data['mean_kwh'])

            features = data.drop(['mean_kwh', 'day', 'hour'], axis = 1)

            features_array = np.array(features)

            train_features, test_features, train_labels, test_labels = train_test_split(features_array, labels, test_size = 0.25)

            knn = KNeighborsRegressor(n_neighbors=u, weights=o)

            knn.fit(train_features, train_labels)

            predictions = knn.predict(test_features)

            errors = abs(predictions - test_labels)

            finish_time = time.time()

            maes.append(np.mean(errors))

            mape = 100 * (errors / test_labels)
            
            accuracy = 100 - np.mean(mape)

            times.append(finish_time - start_time)

            accuracys.append(accuracy)

        print("n_neighbors:", u, "weights:", o)

        mean = np.mean(maes)
        maes = []
        print("mae")
        print("mean")
        print(mean)
        mean = np.mean(times)
        times = []
        print("time")
        print("mean")
        print(mean)
        mean = np.mean(accuracys)
        accuracys = []
        print("accuracy")
        print("mean")
        print(mean)
        print()
