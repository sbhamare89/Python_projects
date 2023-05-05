# if you are running this programm first time kindly install all required modules in python3 from requirments.txt file
# after that edit .env file and make necessary changes in path to store your daily downloaded csv files


import nsepy
import datetime as dt
import pandas as pd
import requests
import concurrent.futures
from decouple import config
#import time, schedule

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

tickers = ["ALKEM", "TCS", "WABCOINDIA", "INFY"]

end_date = dt.datetime.today().strftime('%d%m%Y')
previous_date = dt.datetime.today() - dt.timedelta(days=500)
start_date = previous_date.strftime('%d%m%Y')
print('Current date :' + str(end_date))
print('Previous date :' + str(start_date))
format_str = '%d%m%Y'
date_start_obj = dt.datetime.strptime(start_date, format_str)
date_end_obj = dt.datetime.strptime(end_date, format_str)

class NseIndia:

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        self.session = requests.Session()
        self.session.get("http://nseindia.com", headers=self.headers)

        pre_market_key = {"NIFTY 50": "NIFTY", "Nifty Bank": "BANKNIFTY", "Emerge": "SME", "Securities in F&O": "FO",
                          "Others": "OTHERS", "All": "ALL"}
        key = "All"   # input
        data = self.session.get(f"https://www.nseindia.com/api/market-data-pre-open?key={pre_market_key[key]}", headers=self.headers).json()["data"]
        new_data = []
        for i in data:
            new_data.append(i["metadata"])
        df = pd.DataFrame(new_data)
        tickers = list(df['symbol'])
        # tickers = ["TCS"]
        def gather(symbol):
            
            FRAME = "Daily"
#            FRAME = "Weekly"
            tick = symbol.upper().replace(' ','%20').replace('&', '%26')
            df = nsepy.get_history(tick, date_start_obj, date_end_obj)
            df = df.drop(['Series','Prev Close','Last','VWAP','Turnover','Trades','%Deliverble'], axis=1)
#            df = df['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Deliverable Volume']
            if FRAME == "Weekly":
                df['Date'] = pd.to_datetime(df.index)
                df.set_index('Date', inplace=True)
                df = df.resample('W').agg({'Open': 'first', 'High':'max', 'Low':'min', 'Close': 'last', 'Volume': 'sum' ,'Deliverable Volume':'sum'})
#            df.to_csv("/home/xlr8/Documents/Python_projects/market_analysis/screeners/daily_csv/{}.csv".format(symbol.upper()))
            df.to_csv(config('CSV_DIR') + "/{}.csv".format(symbol.upper()))
            print("Saved data for {}".format(symbol.upper()))
        
        try:
            with concurrent.futures.ThreadPoolExecutor() as executer:
                executer.map(gather, tickers, chunksize=25)
        except:
            pass

nse = NseIndia()
