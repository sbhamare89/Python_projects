import nsepy
import datetime as dt
import pandas as pd
import requests
import concurrent.futures

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

#tickers = ["ALKEM","JSWENERGY","WABCOINDIA"]

ticker = "HEG"
conso = []
breakout = []


class NseIndia:

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        self.session = requests.Session()
        self.session.get("http://nseindia.com", headers=self.headers)

    def pre_market_data(self):
        pre_market_key = {"NIFTY 50": "NIFTY", "Nifty Bank": "BANKNIFTY", "Emerge": "SME", "Securities in F&O": "FO",
                          "Others": "OTHERS", "All": "ALL"}
        key = "All"   # input
        data = self.session.get(f"https://www.nseindia.com/api/market-data-pre-open?key={pre_market_key[key]}", headers=self.headers).json()["data"]
        new_data = []
        for i in data:
            new_data.append(i["metadata"])
        df = pd.DataFrame(new_data)
        return list(df['symbol'])
        #return df

    def live_market_data(self):
        live_market_index = {
            'Broad Market Indices': ['NIFTY 50', 'NIFTY NEXT 50', 'NIFTY MIDCAP 50', 'NIFTY MIDCAP 100',
                                     'NIFTY MIDCAP 150', 'NIFTY SMALLCAP 50', 'NIFTY SMALLCAP 100',
                                     'NIFTY SMALLCAP 250', 'NIFTY MIDSMALLCAP 400', 'NIFTY 100', 'NIFTY 200'],
            'Sectoral Indices': ["NIFTY AUTO", "NIFTY BANK", "NIFTY ENERGY", "NIFTY FINANCIAL SERVICES",
                                 "NIFTY FINANCIAL SERVICES 25/50", "NIFTY FMCG", "NIFTY IT", "NIFTY MEDIA",
                                 "NIFTY METAL", "NIFTY PHARMA", "NIFTY PSU BANK", "NIFTY REALTY",
                                 "NIFTY PRIVATE BANK"],
            'Others': ['Securities in F&O', 'Permitted to Trade'],
            'Strategy Indices': ['NIFTY DIVIDEND OPPORTUNITIES 50', 'NIFTY50 VALUE 20', 'NIFTY100 QUALITY 30',
                                 'NIFTY50 EQUAL WEIGHT', 'NIFTY100 EQUAL WEIGHT', 'NIFTY100 LOW VOLATILITY 30',
                                 'NIFTY ALPHA 50', 'NIFTY200 QUALITY 30', 'NIFTY ALPHA LOW-VOLATILITY 30',
                                 'NIFTY200 MOMENTUM 30'],
            'Thematic Indices': ['NIFTY COMMODITIES', 'NIFTY INDIA CONSUMPTION', 'NIFTY CPSE', 'NIFTY INFRASTRUCTURE',
                                 'NIFTY MNC', 'NIFTY GROWTH SECTORS 15', 'NIFTY PSE', 'NIFTY SERVICES SECTOR',
                                 'NIFTY100 LIQUID 15', 'NIFTY MIDCAP LIQUID 15']}

        indices = "Sectoral Indices"    # input
        key = "NIFTY METAL"     # input
        data = self.session.get(f"https://www.nseindia.com/api/equity-stockIndices?index={live_market_index[indices][live_market_index[indices].index(key)].upper().replace(' ','%20').replace('&', '%26')}", headers=self.headers).json()["data"]
        df = pd.DataFrame(data)
        return list(df["symbol"])
        return df


nse = NseIndia()

tickers = (nse.pre_market_data())
#tickers = (nse.live_market_data())


end_date = dt.datetime.today().strftime('%d%m%Y')
# checks for last 15 days history data
previous_date = dt.datetime.today() - dt.timedelta(days=100)
start_date = previous_date.strftime('%d%m%Y')
print('Current date :' + str(end_date))
print('Previous date :' + str(start_date))
format_str = '%d%m%Y'
date_start_obj = dt.datetime.strptime(start_date, format_str)
date_end_obj = dt.datetime.strptime(end_date, format_str)

#df = pd.DataFrame(nsepy.get_history(ticker, date_start_obj, date_end_obj))
#pprint.pprint(df[-5:])


# % change range of last close prices
def is_consolidating(df_obj,percentage=5):
    max_close = df_obj['Close'].max()
    min_close = df_obj['Close'].min()
#    print("{} : max close {} and min close {}".format(tick, max_close, min_close))
    threshold = 1 - (percentage / 100)
    if min_close > (max_close * threshold):
        return True

    return False
# % change range of last close prices
def is_breaking_out(df,percentage=5):
#    print(df)
    last_close = df[-1:]['Close'].values[0]
    
    if is_consolidating(df[:-1], percentage=percentage):
        recent_closes = df[1:-1]
        if last_close > recent_closes['Close'].max():
            return True
    
    return False

def gather(tick):
    df = nsepy.get_history(tick, date_start_obj, date_end_obj)
    if is_consolidating(df):
#        print("CONSOLIDATING : {} at {}".format(df['Symbol'].values[0], df['Prev Close'].values[0]))
        conso.append(df['Symbol'].values[0])
    if is_breaking_out(df):
#        print("BREAKOUT : {} at {}".format(df['Symbol'].values[0], df['Prev Close'].values[0]))
        breakout.append(df['Symbol'].values[0])
        

try:
    with concurrent.futures.ThreadPoolExecutor() as executer:
        executer.map(gather, tickers, chunksize=25)
except:
    pass

print("Below are list of tickers which are in consolidation\n")
print(conso)
print("Below are list of tickers which are in breakout\n")
print(breakout)