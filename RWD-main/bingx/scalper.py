import pandas as pd
from imports import *
from get_klines import np





def get_support(dataframe):
    """
    Calculate support level
    """
    recent_lows = dataframe[-20:].low 
    support = recent_lows.min()
    return support

def get_resistance(dataframe):
    """
    Calculate resistance level
    """
    recent_highs = dataframe[-20:].high
    resistance = recent_highs.max()
    return resistance

def is_at_support(dataframe):
    """
    Check if price is at support level
    """
    support = get_support(dataframe)
    
    if dataframe.iloc[-1].close >= support and dataframe.iloc[-2].close >= support:
        return False
    
    if dataframe.iloc[-2].close < support and dataframe.iloc[-1].close > dataframe.iloc[-2].close:
        return True

    return False

def is_at_resistance(dataframe):
    """
    Check if price is at resistance level
    """
    resistance = get_resistance(dataframe)
    
    if dataframe.iloc[-1].close <= resistance and dataframe.iloc[-2].close <= resistance:
        return False
    
    if dataframe.iloc[-2].close > resistance and dataframe.iloc[-1].close < dataframe.iloc[-2].close:
        return True
    
    return False
def is_in_channel(df):
    support_touches = 0
    resistance_touches = 0
    
    for i in range(2, len(df)):
        if df.iloc[i, 3] < df.iloc[i-1, 3] and df.iloc[i, 3] < df.iloc[i-2, 3]:
            support_touches += 1
        if df.iloc[i, 2] > df.iloc[i-1, 2] and df.iloc[i, 2] > df.iloc[i-2, 2]:
            resistance_touches += 1
            
    return support_touches >= 3 and resistance_touches >= 3


def print_channel_info(dataframe):
    """
    Print support and resistance levels
    """
    support = get_support(dataframe)
    resistance = get_resistance(dataframe)
    print(f"Support: {support}, Resistance: {resistance}")

def deep_dip_strategy(symbol):
    """
    Main strategy function
    """
    timeframes = ['15m', '1h', '2h', '4h']
    
    for timeframe in timeframes:
        df = get_kline(symbol, timeframe)  
        if is_in_channel(df):
            if is_at_support(df) or is_at_resistance(df):
                print_channel_info(df)
            else:
                print(f"skipt {symbol}")
 
 
 
 
# deep_dip_strategy()
   
tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=deep_dip_strategy)