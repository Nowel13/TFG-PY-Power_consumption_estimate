import csv
import pandas as pd
import datetime

init_date = datetime.datetime(year=2009, month=1, day=1, hour=0)

def calculate_date(row):
    return (init_date + datetime.timedelta(days=int(row["day"]), hours=int(row["hour"]))).strftime("%Y-%m-%d,%H:%M:%S")

data = pd.read_csv("../result_files/BasePrediction2.txt", sep=' ')

data["date"] = data.apply(calculate_date, axis=1)
# data["day"] = data["day"].apply(lambda x: calculate_date(x))
data = data.drop(["hour", "day"], axis=1)

data.to_csv("../result_files/transformed_data.txt", sep=" ", quoting=csv.QUOTE_NONE, escapechar=" ", index=False)
