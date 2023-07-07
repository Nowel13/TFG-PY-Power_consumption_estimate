# Tratamiento de datos
# ==============================================================================
import pandas as pd
import numpy as np

# Gráficos
# ==============================================================================
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns

# Preprocesado y modelado
# ==============================================================================
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Configuración matplotlib
# ==============================================================================
plt.rcParams['image.cmap'] = "bwr"
#plt.rcParams['figure.dpi'] = "100"
plt.rcParams['savefig.bbox'] = "tight"
style.use('ggplot') or plt.style.use('ggplot')

# Configuración warnings
# ==============================================================================
import warnings
warnings.filterwarnings('ignore')


data = pd.read_csv("../processed_files/AllData2.txt", sep=' ')
# data = pd.read_csv("../result_files/BasePrediction2.txt", sep=' ')
fig, ax = plt.subplots(figsize=(6, 3.84))
data.plot(x='day', y='mean_kwh', c='firebrick', kind='scatter', ax=ax)
# data.plot(x='day', y='prediction', c='firebrick', kind='scatter', ax=ax)
ax.set_title('Distribucion tiempo kwh')
# ax.set_title('Distribucion tiempo kwh predicciones')
plt.figure(fig)
plt.show()
# corr_test = pearsonr(x = data['day'], y = data['mean_kwh'])
# print("Coef", corr_test[0])
# print("P-value", corr_test[1])

# X = data[['day']]
# y = data['mean_kwh']
# X_train, X_test, y_train, y_test = train_test_split(
#                                         X.values.reshape(-1,1),
#                                         y.values.reshape(-1,1),
#                                         train_size   = 0.8,
#                                         random_state = 1234,
#                                         shuffle      = True
#                                     )

# modelo = LinearRegression()
# modelo.fit(X = X_train.reshape(-1, 1), y = y_train)

# print("Intercept:", modelo.intercept_)
# print("Coeficiente:", list(zip(X.columns, modelo.coef_.flatten(), )))
# print("Coeficiente de determinación R^2:", modelo.score(X, y))

# predicciones = modelo.predict(X = X_test)
# print(predicciones[0:3,])

# rmse = mean_squared_error(
#         y_true  = y_test,
#         y_pred  = predicciones,
#         squared = False
#        )
# print("")
# print(f"El error (rmse) de test es: {rmse}")

# X_train, X_test, y_train, y_test = train_test_split(
#                                         X.values.reshape(-1,1),
#                                         y.values.reshape(-1,1),
#                                         train_size   = 0.8,
#                                         random_state = 1234,
#                                         shuffle      = True
#                                     )

# X_train = sm.add_constant(X_train, prepend=True)
# modelo2 = sm.OLS(endog=y_train, exog=X_train,)
# modelo2 = modelo2.fit()
# print(modelo2.summary())

# modelo2.conf_int(alpha=0.05)

# predicciones = modelo2.get_prediction(exog = X_train).summary_frame(alpha=0.05)
# predicciones.head(4)

# predicciones = modelo2.get_prediction(exog = X_train).summary_frame(alpha=0.05)
# predicciones['x'] = X_train[:, 1]
# predicciones['y'] = y_train
# predicciones = predicciones.sort_values('x')

# fig, ax = plt.subplots(figsize=(6, 3.84))

# ax.scatter(predicciones['x'], predicciones['y'], marker='o', color = "gray")
# ax.plot(predicciones['x'], predicciones["mean"], linestyle='-', label="OLS")
# ax.plot(predicciones['x'], predicciones["mean_ci_lower"], linestyle='--', color='red', label="95% CI")
# ax.plot(predicciones['x'], predicciones["mean_ci_upper"], linestyle='--', color='red')
# ax.fill_between(predicciones['x'], predicciones["mean_ci_lower"], predicciones["mean_ci_upper"], alpha=0.1)
# ax.legend()

# plt.figure(fig)
# plt.show()