# for scanning different patterns and trendlines, reversals

import os
import pandas as pd
import talib

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

LONG = []
SHORT = []
LConfirmed = []
SConfirmed = []

for filename in os.listdir("/home/xlr8/Documents/Python_projects/market_analysis/screeners/daily_csv"):
    f = os.path.join("daily_csv", filename)
    if os.path.isfile(f):
        try:
            df = pd.read_csv(f)
            filename = filename.split('.')[0]
            df['DeliverablePct'] = ( df['Deliverable Volume'] / df['Volume'] ) * 100
            df['ADL'] = talib.AD(df['High'],df['Low'],df['Close'],df['DeliverablePct'])
            df['OBV'] = talib.OBV(df['Close'],df['DeliverablePct'])
            df['EMA8'] = talib.EMA(df['Close'], timeperiod=8)
            df['EMA5'] = talib.EMA(df['Close'], timeperiod=5)
            df['Trade'] = df.apply(lambda x: 'LONG' if float(x['EMA8']) < float(x['EMA5']) else 'SHORT', axis=1)
            if df['Trade'].iloc[-1] != df['Trade'].iloc[-2]:
                if df['Trade'].iloc[-1] == 'LONG':
                    LONG.append(filename)
                    print(df,filename)
                    if df['ADL'].iloc[[-1]] > df['ADL'].iloc[[-2]]:
                        LConfirmed.append()
                if df['Trade'].iloc[-1] == 'SHORT':
                    SHORT.append(filename)
                    print(df,filename)
                    if df['ADL'].iloc[[-1]] < df['ADL'].iloc[[-2]]:
                        SConfirmed.append()
        except:
            pass
        
print("------------------------")
print("LONG Signal :")
print(LONG)

print("------------------------")
print("LONG Confirmed :")
print(LConfirmed)

print("------------------------")
print("SHORT Signal :")
print(SHORT)

print("------------------------")
print("Short Confirmed :")
print(LConfirmed)