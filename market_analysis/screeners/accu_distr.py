# for scanning different patterns and trendlines, reversals

import os
import pandas as pd
import talib
from decouple import config
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

LONG = []
SHORT = []
LConfirmed = []
SConfirmed = []
trippeltop_pattern = []

#candal window size to check means
wsize = -10

for filename in os.listdir(config('CSV_DIR')):
    f = os.path.join(config('CSV_DIR'), filename)
    if os.path.isfile(f):
        try:
            df = pd.read_csv(f)
            filename = filename.split('.')[0]
            df['DeliverablePct'] = ( df['Deliverable Volume'] / df['Volume'] ) * 100
            df['ADL'] = talib.AD(df['High'],df['Low'],df['Close'],df['Volume'])
            df['OBV'] = talib.OBV(df['Close'],df['Volume'])
            df['EMA8'] = talib.EMA(df['Close'], timeperiod=8)
            df['EMA5'] = talib.EMA(df['Close'], timeperiod=5)
            df['Trade'] = df.apply(lambda x: 'LONG' if float(x['EMA8']) < float(x['EMA5']) else 'SHORT', axis=1)
            
            LC = float(df['ADL'].tail(1).iloc[0])
            
            
            if df['Trade'].iloc[-1] != df['Trade'].iloc[-2]:
                if df['Trade'].iloc[-1] == 'LONG':
                    LONG.append(filename)
                if df['Trade'].iloc[-1] == 'SHORT':
                    SHORT.append(filename)
                    
            if float(df['ADL'].iloc[[-1]]) > 0 and float(df['ADL'].iloc[[-2]]) < 0:
                LConfirmed.append(filename)
            if float(df['ADL'].iloc[[-1]]) < 0 and float(df['ADL'].iloc[[-2]]) > 0:
                SConfirmed.append(filename)
                
        except:
            pass
        
# print("------------------------")
# print("LONG Signal :")
# print(LONG)

print("------------------------")
print("LONG Confirmed :")
print(LConfirmed)

# print("------------------------")
# print("SHORT Signal :")
# print(SHORT)

print("------------------------")
print("Short Confirmed :")
print(LConfirmed)