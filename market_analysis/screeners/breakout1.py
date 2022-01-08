import nsepy
import datetime as dt
import pandas as pd
import requests
import concurrent.futures
import os
from decouple import config

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

conso = []
breakout = []


# % change range of last close prices
def is_consolidating(df_obj,percentage=5):
    max_close = df_obj['Close'].max()
    min_close = df_obj['Close'].min()
    threshold = 1 - (percentage / 100)
    if min_close > (max_close * threshold):
        return True

    return False
# % change range of last close prices
def is_breaking_out(df,percentage=5):
    last_close = df[-1:]['Close'].values[0]
    if is_consolidating(df[:-1], percentage=percentage):
        recent_closes = df[1:-1]
        if last_close > recent_closes['Close'].max():
            return True
    
    return False

for filename in os.listdir(config('CSV_DIR')):
    f = os.path.join(config('CSV_DIR'), filename)
    if os.path.isfile(f):
        try:
            df = pd.read_csv(f)
            if is_consolidating(df):
                conso.append(df['Symbol'].values[0])
            if is_breaking_out(df):
                breakout.append(df['Symbol'].values[0])
        except:
            pass


print("Below are list of tickers which are in consolidation\n")
print(conso)
print("Below are list of tickers which are in breakout\n")
print(breakout)