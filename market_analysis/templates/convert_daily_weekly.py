import os
import pandas as pd
import datetime as dt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


for filename in os.listdir("daily_csv"):
    f = os.path.join("daily_csv", filename)
    
    if os.path.isfile(f):
        try:
            d_parser = lambda x: dt.datetime.strptime(x, '%Y-%m-%d')
            df = pd.read_csv(f, parse_dates=['Date'], date_parser=d_parser)
            df.set_index('Date', inplace=True)
            df = df.resample('W').agg({'Open': 'first', 'High':'max', 'Low':'min', 'Close': 'last', 'Deliverable Volume':'sum'})
            print(filename)
            print(df)
            break
        except:
            pass