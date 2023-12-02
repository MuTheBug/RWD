

from imports import *
from get_klines import np,pd


# def chech_trend(symbol):
#         hour= get_kline(symbol,'1h')
#         hour['sma100'] = ta.sma(close=hour['close'],length=200)
#         hour['above>100'] = hour['sma100'] >hour['close']
#         # print(hour)
#         rows = hour['above>100'].tail(3)
#         # print(rows)
#         res = rows.all()
#         if res:
#             return True
#         return False
	
def sto_over_80(df):

    st= ta.stoch(high=df['high'],low=df['low'],close=df['close'])
    on_15m= st['STOCHd_14_3_3'].iloc[-1]>80 #or st['STOCHd_14_3_3'].iloc[-1] > 80	    
    return on_15m
def kelt(df):
    kels = ta.kc(high=df['high'],low=df['low'],close=df['close'],length=20,scalar=3)
    low_third =  kels['KCLe_20_3.0'].iloc[-1] + ((kels['KCBe_20_3.0'].iloc[-1] - kels['KCLe_20_3.0'].iloc[-1])/1.5)
    return df['close'].iloc[-1] <= low_third

def ema_cross_up(df):
    df['ema26'] = ta.ema(close=df['close'],length=26)
    df['ema100'] = ta.ema(close=df['close'],length=100)
    return df['ema26'].iloc[-2]<df['ema100'].iloc[-2] and df['ema26'].iloc[-1]>df['ema100'].iloc[-1] 
def ema_cross_down(df):
    df['ema260'] = ta.ema(close=df['close'],length=9)
    df['ema1000'] = ta.ema(close=df['close'],length=26)
    return df['ema260'].iloc[-2]>df['ema1000'].iloc[-2] and df['ema260'].iloc[-1]<df['ema1000'].iloc[-1]

def is_above_200(df):
    df['sma250'] = ta.sma(close=df['close'],length=250)
    # print(df['sma250'])
    res = df['sma250'].iloc[-2]>df['close'].iloc[-2] and df['sma250'].iloc[-1]<df['close'].iloc[-1]

    return res
def deep_dip_strategy(symbol):
    """
    Main strategy function
    """
    timeframes=['3m','5m','15m','30m','1h']
    for timeframe in timeframes:
        df = get_kline(symbol, timeframe)
        res= is_above_200(df)
        sto = sto_over_80(df)
        if res and sto:
            print(f"Long {symbol} ++++++++++++++++++++++++++++++++++++++++++++++++++! on{timeframe}")
            send_to_telegram(f'long {symbol} ')
        else:
            print(f"skip {symbol}")


# deep_dip_strategy('ETH-USDT')
tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=deep_dip_strategy)
	
	