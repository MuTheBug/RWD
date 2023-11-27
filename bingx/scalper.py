import pandas as pd
from imports import *
from get_klines import np

import pandas as pd



def is_in_channel(df):
    support_touches = 0
    resistance_touches = 0
    
    for i in range(2, len(df)):
        if df.iloc[i, 3] < df.iloc[i-1, 3] and df.iloc[i, 3] < df.iloc[i-2, 3]:
            support_touches += 1
        if df.iloc[i, 2] > df.iloc[i-1, 2] and df.iloc[i, 2] > df.iloc[i-2, 2]:
            resistance_touches += 1
            
    return support_touches >= 3 and resistance_touches >= 3

 

def get_support(df):
    recent_lows = df[-20:]['low']
    return recent_lows.min()

def get_resistance(df):
    recent_highs = df[-20:]['high']
    return recent_highs.max()  

def is_at_support(df):
    support = get_support(df)
    current_price = df.iloc[-1]['close']
    return current_price == support
    
def is_at_resistance(df):
    resistance = get_resistance(df) 
    current_price = df.iloc[-1]['close']
    return current_price == resistance



def print_channel_info(df):
    support = get_support(df)
    resistance = get_resistance(df)  
    print(f"Support: {support}, Resistance: {resistance}")

def deep_dip_strategy(sy):

    for tf in ['15m','1h','2h','4h']:   
        df = get_kline(sy,tf)        
        if is_in_channel(df):
            if is_at_support(df) or is_at_resistance(df):
                print(f"{sy} at {tf}")
                print_channel_info(df)
 
            else:
                print(f'skip {sy}')
 
 
 
 
 
 
 
# deep_dip_strategy()
   
tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=deep_dip_strategy)