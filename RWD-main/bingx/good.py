import pandas as pd
import numpy as np
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

def get_kline(symbol, timeframe):
   data = pdr.get_data_yahoo(symbol, timeframe)
   return data

def calculate_rsi(data, window):
   delta = data['close'].diff()
   up, down = delta.copy(), delta.copy()
   up[up < 0] = 0
   down[down > 0] = 0
   average_gain = up.rolling(window).mean()
   average_loss = abs(down.rolling(window).mean())
   rs = average_gain / average_loss
   return 100 - (100 / (1 + rs))

def trend_following_strategy(symbol, timeframe, short_window=100, long_window=400, rsi_window=14):
   # Get the data
   data = get_kline(symbol, timeframe)

   # Calculate the moving averages
   data['short_mavg'] = data['close'].rolling(window=short_window).mean()
   data['long_mavg'] = data['close'].rolling(window=long_window).mean()

   # Calculate the RSI
   data['rsi'] = calculate_rsi(data, rsi_window)

   # Create signals
   data['signal'] = 0.0
   data['signal'][short_window:] = np.where(
       (data['short_mavg'][short_window:] > data['long_mavg'][short_window:]) &
       (data['rsi'][short_window:] < 30), 1.0, 0.0)
   data['positions'] = data['signal'].diff()

   # Check the most recent signal
   most_recent_signal = data['positions'].iloc[-1]

   # Return True if the most recent signal is either long or short, and False otherwise
   return most_recent_signal != 0.0

# Test the strategy
print(trend_following_strategy('BTC-UST', '1h'))
