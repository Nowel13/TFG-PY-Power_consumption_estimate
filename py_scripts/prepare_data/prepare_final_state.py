import csv
import pandas as pd
import datetime
import holidays

init_date = datetime.datetime(year=2009, month=1, day=1, hour=0)
holiday_days = holidays.ES()

def calculate_date(days):
    # return (init_date + datetime.timedelta(days=int(row["day"]), hours=int(row["hour"]))).strftime("%Y-%m-%d,%H:%M:%S")
    return (init_date + datetime.timedelta(days=days)).strftime("%Y-%m-%d")

def is_holiday(day):
    return day in holiday_days

data = pd.read_csv("../../result_files/BasePrediction2.txt", sep=' ')

data["date"] = data["day"].apply(lambda x: calculate_date(x))
data["holiday"] = data["date"].apply(lambda x: is_holiday(x))

data.to_csv("../../result_files/transformed_data.txt", sep=" ", quoting=csv.QUOTE_NONE, escapechar=" ", index=False)
