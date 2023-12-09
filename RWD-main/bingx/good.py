from indicators import *
from get_klines import *

pd.options.mode.chained_assignment = None # default='warn'

def trend_following_strategy(symbol, timeframe, short_window=100, long_window=400):
 # Get the data
 data = get_kline(symbol, timeframe)

 # Calculate the moving averages
 data['short_mavg'] = data['close'].rolling(window=short_window).mean()
 data['long_mavg'] = data['close'].rolling(window=long_window).mean()

 # Create signals
 data['signal'] = 0.0
 data['signal'][short_window:] = np.where(data['short_mavg'][short_window:] > data['long_mavg'][short_window:], 1.0, 0.0)
 data['positions'] = data['signal'].diff()

 # Check the most recent signal
 most_recent_signal = data['positions'].iloc[-1]

 # Return True if the most recent signal is either long or short, and False otherwise
 return most_recent_signal != 0.0

# Test the strategy




def main(symbol):
    
    timeframes = ['15m','30m','2h','1h','4h','1d']
    for t in timeframes:
        s = trend_following_strategy(symbol, t)
        if s:
            send_to_telegram(f"{symbol} on {t} ++++")
            print(f" {symbol} on {t} +++++++++++++++++++++++++++++++++++++++++++++")

                        
        else:
            print(f'skip {symbol} on {t}')



tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=main)