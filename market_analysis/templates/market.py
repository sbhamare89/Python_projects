#!/usr/bin/python3.8
# Developed by refering : https://www.youtube.com/watch?v=WBoxb-V9Hm0
import nsepy
import concurrent.futures
import pandas as pd
import datetime
import sys
#from tabulate import tabulate
#import pprint
#pprint.pprint(nsepy.get_quote("tcs"))


symbols = ["KOTAKGOLD", "NIFTYBEES","JUNIORBEES","MON100","BANDHANBNK","HEG"]

def data(symbol):
    data_nse = nsepy.get_quote(symbol.replace("&","%26"))["data"][0]
    return {symbol.upper(): { "LTP": float(data_nse["lastPrice"].replace(",", "")),
                              "Change": float(data_nse["change"].replace(",", "")),
                              "%": float(data_nse["pChange"].replace(",", ""))
    } 
}

todays_day = datetime.date.today().isoweekday()

if todays_day > 0 or todays_day < 6:
    pass
else:
    print ("It's weekend today, market closed. Please re-run on Monday after 9.15 AM")
    sys.exit()

def get_multiple_stock_data(symbol_list):
    multiple_stocks = {}
    with concurrent.futures.ThreadPoolExecutor() as executer:
        results = executer.map(data, symbol_list)
        for i in results:
            for k, v in i.items():
                multiple_stocks[k] = v
    return multiple_stocks

while datetime.time(9,15) < datetime.datetime.now().time() < datetime.time(15,30):
    stocks_data = get_multiple_stock_data(symbols)
    df = pd.DataFrame(stocks_data).transpose()
    print (df)
    sys.exit()

if datetime.datetime.now().time() > datetime.time(15,30):
    print ("Wait till 9:20 AM !!!")
    sys.exit()
else:
    pass

#print(tabulate(df, headers = 'keys', tablefmt = 'psql'))