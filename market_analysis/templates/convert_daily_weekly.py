import os
import pandas as pd
import datetime as dt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


for filename in os.listdir("/home/xlr8/Documents/Python_projects/market_analysis/screeners/daily_csv"):
    f = os.path.join("/home/xlr8/Documents/Python_projects/market_analysis/screeners/daily_csv", filename)
    
    if os.path.isfile(f):
        try:
            d_parser = lambda x: dt.datetime.strptime(x, '%Y-%m-%d')
            df = pd.read_csv(f, parse_dates=['Date'], date_parser=d_parser)
            df.set_index('Date', inplace=True)
            df = df.resample('W').agg({'Open': 'first', 'High':'max', 'Low':'min', 'Close': 'last', 'Volume': 'sum' ,'Deliverable Volume':'sum'})
            df['DeliverablePct'] = ( df['Deliverable Volume'] / df['Volume'] ) * 100
            print(filename)
            print(df)
            break
        except:
            pass