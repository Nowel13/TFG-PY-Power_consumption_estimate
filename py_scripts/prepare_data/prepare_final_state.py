import csv
import datetime
import holidays
import pandas as pd

# Este script recibe un parametro (int) a través del cual se elige cuántas variables independientes queremos utilizar para 
# las predicciones en un futuro.
# A partir de este int recibido, se generan ese número de columnas cogiendo los datos de los 3 + x días anteriores.

holiday_days = holidays.ES()

# Generamos una nueva columna en la que se sepa si el día elegido es festivo o no:
def calculate_holiday(days, init_date):
    return (init_date + datetime.timedelta(days=days)).strftime('%Y-%m-%d') in holiday_days

# Añadimos las x columnas al archivo de datos para el futuro estudio.
# Rellenamos los huecos sin datos con los valores reales de consumo eléctrico:
def add_days_columns(df, max):
    # Generamos una copia del dataframe para poder sacar los datos de los días anteriores.
    copy = df.copy(deep=True)
    # Inicializamos los datos en una primera instancia en dos días antes, de forma que al comenzar el bucle, la primera iteración
    # busque los datos de 3 días antes.
    copy['day'] += 2
    for i in range(0, max):
        # Cada día que aumentamos generamos los valores correspondientes de 'mean_kwh'
        copy['day'] += 1
        # Combinamos ambos dataframes para obtener los resultados correspondientes por día y hora.
        df = pd.merge(df, copy[['day','hour','mean_kwh']],  how='left', left_on=['day','hour'], right_on = ['day','hour'])
        # Renombramos las columnas resultantes para que no varíe la estructura.
        df = df.rename(columns={'mean_kwh_x': 'mean_kwh', 'mean_kwh_y': '{}_days_ago'.format(3+i)})
        # Rellenamos los huecos que se completan con valores NaN utilizando los datos reales de esa fecha, esto sucede solo al principio
        # de los datos, ya que no existen registros anteriores a los primeros.
        df['{}_days_ago'.format(3+i)] = df['{}_days_ago'.format(3+i)].fillna(df['mean_kwh'])
    # Devolvemos el resultado final:
    return df


def take_data_from(row, data, real_day):
    df = data[(data['day'] == row['day']-real_day)]
    return df[df['hour'] == row['hour']]['mean_kwh'].iloc[0]

def prepare_predictions(data, max, date):
    df = pd.DataFrame()
    days = []
    horas = pd.DataFrame({'hour': range(24)})
    for i in range(data.iloc[-1]['day']+1, data.iloc[-1]['day']+4):
        days.append(i)

    df['day'] = days
    df = df.assign(key=1).merge(horas.assign(key=1), on='key').drop('key', axis=1)
    df['holiday'] = df['day'].apply(lambda x: calculate_holiday(x, date))
    for i in range(0, max):
        df['{}_days_ago'.format(3+i)] = df.apply(lambda row: take_data_from(row, data, 3+i), axis=1)
    
    return df


def main(max_days_before, init_date):

    date = datetime.datetime(year=2009, month=1, day=1, hour=0)

    # Obtenemos los datos iniciales de 'AllData.txt':
    data = pd.read_csv('result_files/AllData.txt', sep=' ')

    # Computamos la columna 'holiday' con la funcion definida anteriormente (Se podría comprobar si al vectorizar reduce el tiempo de 
    # ejecución, pero ya de por sí tarda muy poco):
    data['holiday'] = data['day'].apply(lambda x: calculate_holiday(x, date))
    # data['holiday'] = np.where(calculate_holiday(data['day']), True, False)

    # Generamos el dataframe final con las nuevas columnas añadidas:
    final_data = add_days_columns(data, max_days_before)

    # Escribimos los resultados en el archivo 'final_data.txt' de forma que podamos utilizar los resultados más adelante en otros scripts:
    final_data.to_csv('result_files/final_data.txt', sep=' ', quoting=csv.QUOTE_NONE, escapechar=' ', index=False)


    to_predict_df = prepare_predictions(final_data, max_days_before, date)
    to_predict_df.to_csv('result_files/to_predict.txt', sep=' ', quoting=csv.QUOTE_NONE, escapechar=' ', index=False)
