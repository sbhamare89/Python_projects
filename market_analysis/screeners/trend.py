# for scanning different trendlines

import os
from numpy import float64, number
import pandas as pd
from decouple import config

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

#candal window size to check means
wsize = -20

uptrend = []
uptrend_broke = []
downtrend = []
downtrend_broke = []

for filename in os.listdir(config('CSV_DIR')):
    f = os.path.join(config('CSV_DIR'), filename)
    if os.path.isfile(f):
        try:
            df = pd.read_csv(f)
            filename = filename.split('.')[0]             
            HH1 = float(df.iloc[wsize:]['High'].to_frame().max())
            HH2 = float(df.iloc[wsize*2:wsize]['High'].to_frame().max())
            HH3 = float(df.iloc[wsize*3:wsize*2]['High'].to_frame().max())
            HH4 = float(df.iloc[wsize*4:wsize*3]['High'].to_frame().max())
            HH5 = float(df.iloc[wsize*5:wsize*4]['High'].to_frame().max())
            LC = float(df['Close'].tail(1).iloc[0])

            LH1 = float(df.iloc[wsize:]['Low'].to_frame().min())
            LH2 = float(df.iloc[wsize*2:wsize]['Low'].to_frame().min())
            LH3 = float(df.iloc[wsize*3:wsize*2]['Low'].to_frame().min())
            LH4 = float(df.iloc[wsize*4:wsize*3]['Low'].to_frame().min())
            LH5 = float(df.iloc[wsize*5:wsize*4]['Low'].to_frame().min())
            
            if (HH1 > HH2) and (HH2 > HH3) and (HH3 > HH4) and (HH4 > HH5):
                uptrend.append(filename)
                if (LC < HH3):
                    uptrend_broke.append(filename)

            if (LH1 < LH2) and (LH2 < LH3) and (LH3 < LH4) and (LH4 < LH5):
                downtrend.append(filename)
                if (LC > LH3):
                    downtrend_broke.append(filename)

        except:
            pass

print("-----------------------------------------------------------")

print("Down Trendlines : ")
print(downtrend)

print("-----------------------------------------------------------")

print("Down Trendlines broken : BULLISH ")
print(downtrend_broke)

print("-----------------------------------------------------------")

print("UP trendline Pattern : ")
print(uptrend)

print("-----------------------------------------------------------")

print("UP trendline Pattern broken : BEARISH ")
print(uptrend_broke)