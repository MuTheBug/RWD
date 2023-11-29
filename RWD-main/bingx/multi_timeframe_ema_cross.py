

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
	
def sto_over_80(symbol):
    df= get_kline(symbol,'15m')
    st= ta.stoch(high=df['high'],low=df['low'],close=df['close'])
    on_15m= st['STOCHd_14_3_3'].iloc[-1]>80 #or st['STOCHd_14_3_3'].iloc[-1] > 80	    
    dfs= get_kline(symbol,'1h')
    stx= ta.stoch(high=dfs['high'],low=dfs['low'],close=dfs['close'])
    on_1h= stx['STOCHd_14_3_3'].iloc[-2]<=23 or stx['STOCHd_14_3_3'].iloc[-1] <=23 or stx['STOCHd_14_3_3'].iloc[-3] <=23
    return on_15m and on_1h


def ema_cross_up(df):
    df['ema26'] = ta.ema(close=df['close'],length=9)
    df['ema100'] = ta.ema(close=df['close'],length=26)
    return df['ema26'].iloc[-2]<df['ema100'].iloc[-2] and df['ema26'].iloc[-1]>df['ema100'].iloc[-1] 
def ema_cross_down(df):
    df['ema260'] = ta.ema(close=df['close'],length=9)
    df['ema1000'] = ta.ema(close=df['close'],length=26)
    return df['ema260'].iloc[-2]>df['ema1000'].iloc[-2] and df['ema260'].iloc[-1]<df['ema1000'].iloc[-1] 
def deep_dip_strategy(symbol):
    """
    Main strategy function
    """
    timeframe='15m'
    df = get_kline(symbol, timeframe)
    trendy = sto_over_80(symbol)
    if ema_cross_up(df) and trendy:
        print(f"Short {symbol}!")
        send_to_telegram(f'Short {symbol}')
    # if ema_cross_down(df) and sto_under_20(df):
    #     print(f"Short {symbol}!")
    #     send_to_telegram(f'Short {symbol}')
    else:
        print(f"skip {symbol}")


# deep_dip_strategy('XRP-USDT')
tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=deep_dip_strategy)
	
	