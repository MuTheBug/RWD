import pandas as pd
from imports import *
from get_klines import np

def stocha(df):
    stoch = ta.stoch(high=df['high'],low=df['low'],close=df['close'])
    stoch['rsi'] = ta.rsi(close=df['close'],length=14)
    if stoch['STOCHd_14_3_3'].iloc[-1]<20 and stoch['rsi'].iloc[-1] < 30:
        return True
    return False
def deep_dip_strategy(symbol):
    """
    Main strategy function
    """
    timeframes = ['1m','3m','5m','15m']
    
    for timeframe in timeframes:
        df = get_kline(symbol, timeframe)  
        if stocha(df):
            print(f"{symbol} at {timeframe}, hurrrrrrrrrrrrrrry upppppppppppppppppppppppp!")
        else:
            print(f"skipt {symbol}")


# deep_dip_strategy('BTC-USDT')
tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=deep_dip_strategy)