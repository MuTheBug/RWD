import numpy as np
import pandas as pd
from get_klines import get_kline
import send_to_telegram
import loop
import pandas_ta as ta
import get_sympols

# get_kline() returns a pd series with columns open, close, high, low, volume, and time

# I want a python code that calculate the renko bricks with the (atr/2 ) as a brick size

# then put the bricks as either True if green or False if red in a column in the same df        
# kline = get_kline() # Retrieves kline dataframe 
# get_renko(kline)

def renko_bricks(sym):
    df = get_kline(sym)
    df['atr'] = ta.atr(high=df['high'],low=df['low'],close=df['close'],length=14)
    brick_size = df['atr'].iloc[-1] / 2
    renko = [True]
    
    prev_brick = df.open[0]
    for close in df.close[1:]:
        if close > prev_brick + brick_size:
            renko.append(True)
            prev_brick += brick_size
        elif close < prev_brick - brick_size: 
            renko.append(False)
            prev_brick -= brick_size
        else:
            renko.append(renko[-1])
    
    # return renko
    if renko[-1] == renko[-2] and renko[-2]!=renko[-3]:
        print(f"{sym} is a good hit ++++++++++++++++")
    else:
        print(f"skip {sym}")

tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=renko_bricks)

