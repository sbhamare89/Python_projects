import yfinance as yf
import talib
import copy
import pandas as pd

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

symbol = "TATAMOTORS.NS"

df = yf.Ticker(symbol).history(period="5y", interval="1d")

df["MA_SLOW"] = talib.MA(df['Close'], timeperiod=10)
df["MA_FAST"] = talib.MA(df['Close'], timeperiod=50)
df["RSI_14"] = talib.RSI(df['Close'], timeperiod=14)

symbol_trade = []
trade = {"Symbol": None, "Buy/Sell": None, "Entry": None, "Entry Date": None, "Exit": None, "Exit Date": None}
position = None

for i in df.index:
    if df["MA_FAST"][i] > df["MA_SLOW"][i] and df["RSI_14"][i] > 70 and position != "Buy":
        if trade["Symbol"] is not None:
            trade["Exit"] = df["Close"][i]
            trade["Exit Date"] = i
            symbol_trade.append(copy.deepcopy(trade))
        if position is not None:
            trade["Symbol"] = symbol
            trade["Buy/Sell"] = "Buy"
            trade["Entry"] = df['Close'][i]
            trade["Entry Date"] = i
        position = "Buy"
        print(trade)
        
        
    
    if df["MA_FAST"][i] < df["MA_SLOW"][i] and df["RSI_14"][i] < 30 and position != "Sell":
        if trade["Symbol"] is not None:
            trade["Exit"] = df["Close"][i]
            trade["Exit Date"] = i
            symbol_trade.append(copy.deepcopy(trade))
        if position is not None:
            trade["Symbol"] = symbol
            trade["Buy/Sell"] = "Sell"
            trade["Exit"] = df['Close'][i]
            trade["Exit Date"] = i
        postion = "Sell"
        
        print(trade)
print(symbol_trade)