import pandas as pd
from imports import *
from get_klines import np

def stocha(df):
    stoch = ta.stoch(high=df['high'],low=df['low'],close=df['close'])
    stoch['rsi'] = ta.rsi(close=df['close'],length=14)
    if stoch['STOCHd_14_3_3'].iloc[-1]<20 and stoch['rsi'].iloc[-1] < 30:
        return True
    return False


def check_double_bottom(df):
    """Check for recent double bottom in OHLC dataframe"""
 
    # bottoms =df.low.tail(5)
    if len(df) < 5: 
        return False
    
    # Find bottoms 
    
    bottoms = df.iloc[-5:-1].loc[df.iloc[-5:-1].low == df.iloc[-5:-1].low.min()]    
    if len(bottoms) != 2:
        return False

    # Check approximate equality 
    if abs(bottoms.iloc[0].low - bottoms.iloc[1].low) > 0.1*abs(df.low.min()):  
        return False
    
    # Passed all checks
    return True

def check_bull_flag(df):
    """Check for recent bull flag pattern in OHLC dataframe"""
    if len(df) < 10:
        return False
    
    pole = df.iloc[-10:-5] 
    flag = df.iloc[-5:]
    
    if pole.close.pct_change()[-1] < 0.1: 
        return False
    
    if abs(flag.open.max() - flag.close.min()) > 0.3*abs(pole.close.max() - pole.close.min()):
        return False
    
    return True
def deep_dip_strategy(symbol):
    """
    Main strategy function
    """
    timeframes = ['1m','3m','5m','15m']
    
    for timeframe in timeframes:
        df = get_kline(symbol, timeframe)  
        if stocha(df):
            print(f"{symbol} at {timeframe}, hurrrrrrrrrrrrrrry upppppppppppppppppppppppp!")
        # if check_double_bottom(df):
        #     print(f"{symbol} DOUBlE BOTTOM {timeframe}, hurrrrrrrrrrrrrrry upppppppppppppppppppppppp!")
        # if check_bull_flag(df):
        #     print(f"{symbol} BULL FLAG {timeframe}, hurrrrrrrrrrrrrrry upppppppppppppppppppppppp!")
        else:
            print(f"skipt {symbol}")


# deep_dip_strategy('BTC-USDT')
tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=deep_dip_strategy)