
import numpy as np
from imports import *
import get_klines
def just_crossed_up(df):
    macd = ta.macd(close=df['close'])
    condition_1 =  macd['MACDh_12_26_9'].iloc[-1] > 0 and macd['MACDh_12_26_9'].iloc[-2]< 0
    condition_2 =  macd['MACDh_12_26_9'].iloc[-2] > 0 and macd['MACDh_12_26_9'].iloc[-3]< 0
    return condition_1 or condition_2

def is_macd__going_down_on_daily(df):
    macd = ta.macd(close=df['close'])
    condition_1 =  macd['MACDh_12_26_9'].iloc[-1] < macd['MACDh_12_26_9'].iloc[-2] and macd['MACDh_12_26_9'].iloc[-2] > macd['MACDh_12_26_9'].iloc[-3] and ['MACDh_12_26_9'].iloc[-1] > 0 
    condition_2 =  macd['MACDh_12_26_9'].iloc[-1] < macd['MACDh_12_26_9'].iloc[-2] and macd['MACDh_12_26_9'].iloc[-2] < macd['MACDh_12_26_9'].iloc[-3] and  macd['MACDh_12_26_9'].iloc[-3] > macd['MACDh_12_26_9'].iloc[-4] and macd['MACDh_12_26_9'].iloc[-3] >0
    if condition_1 or condition_2:
        return True
    return False

def is_macd__going_up_on_daily(df):
    macd = ta.macd(close=df['close'])
    condition_1 =  macd['MACDh_12_26_9'].iloc[-1] > macd['MACDh_12_26_9'].iloc[-2] and macd['MACDh_12_26_9'].iloc[-2] < macd['MACDh_12_26_9'].iloc[-3] and ['MACDh_12_26_9'].iloc[-1] < 0 
    condition_2 =  macd['MACDh_12_26_9'].iloc[-1] > macd['MACDh_12_26_9'].iloc[-2] and macd['MACDh_12_26_9'].iloc[-2] > macd['MACDh_12_26_9'].iloc[-3] and  macd['MACDh_12_26_9'].iloc[-3] < macd['MACDh_12_26_9'].iloc[-4] and macd['MACDh_12_26_9'].iloc[-3] <0
    if condition_1 or condition_2:
        return True
    return False

def just_crossed_down(df):
    macd = ta.macd(close=df['close'])
    condition_1 =  macd['MACDh_12_26_9'].iloc[-1] < 0 and macd['MACDh_12_26_9'].iloc[-2]> 0
    condition_2 =  macd['MACDh_12_26_9'].iloc[-2] < 0 and macd['MACDh_12_26_9'].iloc[-3]> 0
    return condition_1 or condition_2


def already_up_going_down(df):
    macd = ta.macd(close=df['close'])
    return macd['MACDh_12_26_9'].iloc[-1]< macd['MACDh_12_26_9'].iloc[-2] and macd['MACDh_12_26_9'].iloc[-1] >0 


def already_down_going_up(df):
    macd = ta.macd(close=df['close'])
    return macd['MACDh_12_26_9'].iloc[-1]> macd['MACDh_12_26_9'].iloc[-2] and macd['MACDh_12_26_9'].iloc[-1]<0 
    


def stoc_signal_above_70(df):
    st= ta.stoch(high=df['high'],low=df['low'],close=df['close'])
    under_20= st['STOCHd_14_3_3'].iloc[-1] >80 and st['STOCHd_14_3_3'].iloc[-2]<80
    return under_20

def above_sma_200(df):
    df['sma200'] = ta.sma(close=df['close'],length=200)
    df['sma50'] = ta.sma(close=df['close'],length=50)
    up = df['sma200'].tail(5).is_monotonic_increasing and df['close'].iloc[-1]>df['sma200'].iloc[-1]
 
def ema_cross_up(df):
   df['ema9'] = ta.ema(close=df['close'],length=9)
   df['ema26'] = ta.ema(close=df['close'],length=26)
   crossed = df.ema9.iloc[-1]>df.ema26.iloc[-1] and df.ema9.iloc[-2]<df.ema26.iloc[-2]
   return crossed

def ema_cross_down(df):
    df['ema400'] = ta.ema(close=df['close'],length=9)
    df['ema100'] = ta.ema(close=df['close'],length=26)
    df['crossed_down'] = np.where(df['ema100'] < df['ema400'].shift(), True, False)
    s = df.crossed_down.tail(10).to_list()
    return True if any(s) else False
def above_sma_50(df):
    df['sma50'] = ta.sma(close=df['close'],length=50)
    up = df['sma50'].tail(5).is_monotonic_increasing 
 
    return up

def rsi_sloping_up(df):
    df['rsi'] = ta.rsi(close=df['close'],length=14)
    # slice = df['rsi'].tail(2).is_monotonic_increasing
    under_40 = df['rsi'].iloc[-2] <=70 and df['rsi'].iloc[-1] >70
    return under_40

def rsi_sloping_down(df):
    df['rsi'] = ta.rsi(close=df['close'],length=14)
    # slice = df['rsi'].tail(2).is_monotonic_increasing
    under_40 = df['rsi'].iloc[-2] >=70 and df['rsi'].iloc[-1] < 70
    return under_40

def bb_up(df):
    bba= ta.bbands(close=df['close'])
    return bba['BBU_5_2.0'].iloc[-1]>df['close'].iloc[-1]
def bb_down(df):
    bba= ta.bbands(close=df['close'])
    return bba['BBL_5_2.0'].iloc[-1]<df['close'].iloc[-1]
    
    
    
def pre_high(df):
    pv = df.tail(3).close.max()
    curr_close = df.close.iloc[-1]
    prev_close = df.close.iloc[-2]
    con = curr_close > pv #and prev_close < pv
    print(con)
    return con
def pre_low(df):
    pv = df.tail(3).close.min()
    curr_close = df.close.iloc[-1]
    prev_close = df.close.iloc[-2]
    con = curr_close < pv #and prev_close < pv
    print(con)
    return con
    
# x = get_klines.get_kline('BTC-USDT','1d')

# # # stoc_signal(x)
# z = ema_cross_down(x)
# print(z)
# s = ema_cross_up(x)
# print(s)

