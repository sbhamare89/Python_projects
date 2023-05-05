# for scanning different patterns and trendlines, reversals

import os
from numpy import float64, half, number
import pandas as pd
#from pandas.core.tools.datetimes import DatetimeScalarOrArrayConvertible
from decouple import config
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

#candal window size to check means
wsize = -50

triangle = []
double_top = []
double_bottom = []
rectangle_pattern = []
uptrend = []
uptrend_broke = []
downtrend = []
downtrend_broke = []
hns = []
ihns = []
risingtriangle = []
fallingtriangle = []

FRAME = "DAILY"
FRAME = "WEEKLY"

for filename in os.listdir(config('CSV_DIR')):
    f = os.path.join(config('CSV_DIR'), filename)
    if os.path.isfile(f):
        try:
            df = pd.read_csv(f)
            # if FRAME == "WEEKLY":
            #     df['Date'] = pd.to_datetime(df.index)
            #     df.set_index('Date', inplace=True)
            #     df = df.resample('W').agg({'Open': 'first', 'High':'max', 'Low':'min', 'Close': 'last', 'Volume': 'sum' ,'Deliverable Volume':'sum'})

            HH1 = float(df.iloc[wsize:]['High'].to_frame().max())
            HH2 = float(df.iloc[wsize*2:wsize]['High'].to_frame().max())
            HH3 = float(df.iloc[wsize*3:wsize*2]['High'].to_frame().max())
            HH4 = float(df.iloc[wsize*4:wsize*3]['High'].to_frame().max())
            HH5 = float(df.iloc[wsize*5:wsize*4]['High'].to_frame().max())
            LH1 = float(df.iloc[wsize:]['Low'].to_frame().min())
            LH2 = float(df.iloc[wsize*2:wsize]['Low'].to_frame().min())
            LH3 = float(df.iloc[wsize*3:wsize*2]['Low'].to_frame().min())
            LH4 = float(df.iloc[wsize*4:wsize*3]['Low'].to_frame().min())
            LH5 = float(df.iloc[wsize*5:wsize*4]['Low'].to_frame().min())
            LC = float(df['Close'].tail(1).iloc[0])
            
            filename = filename.split('.')[0]
           
            if ( HH1 < float( HH2 * 1.02 )) and ( HH1 > float ( HH2 * 0.98 )) and ( HH1 < float( HH3 * 1.02 )) and ( HH1 > float ( HH3 * 0.98 )) and ( HH1 < float( HH3 * 1.02 )) and ( HH1 > float ( HH3 * 0.98 )) and (LH1 > LH2 > LH3):
                risingtriangle.append(filename)
                
            if ( LH1 < float( LH2 * 1.02 )) and ( LH1 > float ( LH2 * 0.98 )) and ( LH1 < float( LH3 * 1.02 )) and ( LH1 > float ( LH3 * 0.98 )) and ( LH1 < float( LH3 * 1.02 )) and ( LH1 > float ( LH3 * 0.98 )) and (HH1 < HH2 < HH3):
                fallingtriangle.append(filename)
           
            if (HH1 > HH2) and (HH2 > HH3) and (HH3 > HH4) and (HH4 > HH5):
                uptrend.append(filename)
                if (LC < HH3):
                    uptrend_broke.append(filename)

            if (LH1 < LH2) and (LH2 < LH3) and (LH3 < LH4) and (LH4 < LH5):
                downtrend.append(filename)
                if (LC > LH3):
                    downtrend_broke.append(filename)
            
            if (HH1 < HH2) and (HH2 < HH3) and (LH1 > LH2) and (LH2 > LH3):
                triangle.append(filename)
                
            HH3 = float(df.iloc[wsize*4:wsize*2]['High'].to_frame().max())
            LC = df['Close'].tail(1).iloc[0]
                        
            if ( HH1 < float( HH2 * 1.02 )) and ( HH1 > float ( HH2 * 0.98 )) and ( HH2 > HH3 ):# and ( LC > HH2 ):
                double_top.append(filename)
                
            LH3 = float(df.iloc[wsize*4:wsize*2]['Low'].to_frame().min())
            HH = df['Open'].head(1).iloc[0]
                        
            if ( LH1 < float( LH2 * 1.02 )) and ( LH1 > float ( LH2 * 0.98 )) and ( LH2 < LH3 ):# and ( HH < LH2 ):
                double_bottom.append(filename)
           
            if ( HH1 < float( HH2 * 1.02 )) and ( HH1 > float ( HH2 * 0.98 )) and ( LH1 < float( LH2 * 1.02 )) and ( LH1 > float ( LH2 * 0.98 )):
                rectangle_pattern.append(filename)

            n1 = int(wsize/2)
            n2 = int(n1+wsize)
            n3 = int(n1+wsize*2)
            n4 = int(n1+n3)
            
            
            # RL = float(df.iloc[n2:n1]['Low'].to_frame().min())
            # LL = float(df.iloc[n4:n3]['Low'].to_frame().min())
            HH2 = float(df.iloc[n3:n1]['High'].to_frame().max())
            HH3 = float(df.iloc[wsize*3:wsize*2]['High'].to_frame().max())
            HH4 = float(df.iloc[wsize*4:wsize*2]['High'].to_frame().max())
            LH2 = float(df.iloc[wsize*2:n1]['Low'].to_frame().min())
            LH3 = float(df.iloc[n3:wsize*2]['Low'].to_frame().min())                        

            if ( HH1 < float ( HH2 * 0.95 )) and ( HH3 < float ( HH2 * 0.95 )) and ( LH2 < float ( LH1 * 1.02 )) and ( LH2 > float ( LH1 * 0.95 )) and ( LH2 < float ( LH1 * 1.02 )) and ( LH3 > float ( LH1 * 0.95 )) and ( HH3 < HH4):
                hns.append(filename)
                         
            # RH = float(df.iloc[n2:n1]['High'].to_frame().max())
            # LH = float(df.iloc[n4:n3]['High'].to_frame().max())
            LH2 = float(df.iloc[n3:n1]['Low'].to_frame().min())
            LH3 = float(df.iloc[wsize*3:wsize*2]['Low'].to_frame().min())
            LH4 = float(df.iloc[wsize*4:wsize*2]['Low'].to_frame().min())
            HH2 = float(df.iloc[n2:n1]['High'].to_frame().max())
            HH3 = float(df.iloc[n3:wsize*2]['High'].to_frame().max())                        
            
            if ( LH1 > float ( LH2 * 0.99 )) and ( LH3 > float ( LH2 * 0.99 )) and ( HH2 < float ( HH1 * 1.01 )) and ( HH2 > float ( HH1 * 0.99 )) and ( HH2 < float ( HH1 * 1.01 )) and ( HH3 > float ( HH1 * 0.99 )) and ( LH3 > LH4):
                ihns.append(filename)

        except:
            pass

print("-----------------------------------------------------------")

print("Triangle Pattern : ")
print(triangle)

print("-----------------------------------------------------------")

print("Rising triangle Pattern : ")
print(risingtriangle)

print("-----------------------------------------------------------")

print("Falling triangle Pattern : ")
print(fallingtriangle)

print("-----------------------------------------------------------")

print("Head and shoulder Pattern : Bearish")
print(hns)

print("-----------------------------------------------------------")

print("Inverted Head and shoulder Pattern : Bullish ")
print(ihns)

print("-----------------------------------------------------------")

print("Double top Pattern : ")
print(double_top)

print("-----------------------------------------------------------")

print("Double bottom Pattern : ")
print(double_bottom)

print("-----------------------------------------------------------")

print("Rectangle Pattern : ")
print(rectangle_pattern)

print("-----------------------------------------------------------")

print("Down Trendlines : ")
print(downtrend)

print("-----------------------------------------------------------")

print("Down Trendlines broken : BULLISH Reversal")
print(downtrend_broke)

print("-----------------------------------------------------------")

print("UP trendline Pattern : ")
print(uptrend)

print("-----------------------------------------------------------")

print("UP trendline Pattern broken : BEARISH Reversal")
print(uptrend_broke)
