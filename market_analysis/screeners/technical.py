import talib
import os
from numpy import float64, number
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


for filename in os.listdir("daily_csv"):
    f = os.path.join("daily_csv", filename)
    if os.path.isfile(f):
        try:
            df = pd.read_csv(f)
            engulfing = talib.CDLENGULFING(df['Open'], df['High'], df['Low'], df['Close'])
            df['Engulfing'] = engulfing
            engulfing_days = df[df['Engulfing'] != 0 ]
            print(engulfing_days)
            break     
        except:
            pass