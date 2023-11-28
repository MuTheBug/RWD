

from imports import *
from get_klines import np,pd


def chech_trend(symbol):
        hour= ichi(get_kline(symbol,'1h'))
        if hour:
            print(f'{symbol} is trending on 1 hour')
            return True
        two_hour= ichi(get_kline(symbol,'2h'))
        if two_hour:
            print(f'{symbol} is trending on 2 hour')
            return True
        four_hour= ichi(get_kline(symbol,'4h'))
        if four_hour:
            print(f'{symbol} is trending on 4 hour')
            return True
        return False

def ichi(df):
    high = df['high']
    low = df['low']
    close = df['close']
    
    # Tenkan-sen (Conversion Line)
    period9_high = high.rolling(window=6).max()
    period9_low = low.rolling(window=6).min()
    tenkan_sen = (period9_high + period9_low) / 2
    
    # Kijun-sen (Base Line)
    period26_high = high.rolling(window=13).max()
    period26_low = low.rolling(window=13).min()
    kijun_sen = (period26_high + period26_low) / 2
    
    # Senkou Span A (Leading Span A)
    senkou_a = ((tenkan_sen + kijun_sen) / 2).shift(26)
    
    # Senkou Span B (Leading Span B)
    period52_high = high.rolling(window=52).max()
    period52_low = low.rolling(window=52).min()
    senkou_b = ((period52_high + period52_low) / 2).shift(26)
    
    # Add to dataframe
    df['conversion_line'] = tenkan_sen 
    df['base_line'] = kijun_sen
    df['senkou_a'] = senkou_a
    df['senkou_b'] = senkou_b
    return df['conversion_line'].iloc[-3]<df['base_line'].iloc[-3] and df['conversion_line'].iloc[-2]>df['base_line'].iloc[-2] 
	
def sto_over_80(df):
	st= ta.stoch(high=df['high'],low=df['low'],close=df['close'])
	return st['STOCHd_14_3_3'].iloc[-1]>80 #or st['STOCHd_14_3_3'].iloc[-1] > 80	
def sto_under_20(df):
	st= ta.stoch(high=df['high'],low=df['low'],close=df['close'])
	return st['STOCHd_14_3_3'].iloc[-1]<20 #or st['STOCHd_14_3_3'].iloc[-1] > 80

def ema_cross_up(df):
    df['ema26'] = ta.ema(close=df['close'],length=26)
    df['ema100'] = ta.ema(close=df['close'],length=100)
    return df['ema26'].iloc[-2]<df['ema100'].iloc[-2] and df['ema26'].iloc[-1]>df['ema100'].iloc[-1] 
def ema_cross_down(df):
    df['ema260'] = ta.ema(close=df['close'],length=26)
    df['ema1000'] = ta.ema(close=df['close'],length=100)
    return df['ema260'].iloc[-2]>df['ema1000'].iloc[-2] and df['ema260'].iloc[-1]<df['ema1000'].iloc[-1] 
def deep_dip_strategy(symbol):
    """
    Main strategy function
    """
    timeframe='5m'
    df = get_kline(symbol, timeframe)
    if ema_cross_up(df) and sto_over_80(df):
        print(f"Long {symbol}!")
        send_to_telegram(f'Long {symbol}')
    if ema_cross_down(df) and sto_under_20(df):
        print(f"Short {symbol}!")
        send_to_telegram(f'Short {symbol}')
    else:
        print(f"skip {symbol}")


#deep_dip_strategy('BTC-USDT')
tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=deep_dip_strategy)
	
	