
from imports import *
from get_klines import get_kline
def macd_signal_up(df):
    macd = ta.macd(close=df['close'])
    return macd['MACDh_12_26_9'].iloc[-1] > 0 

def macd_signal_down(df):
    macd = ta.macd(close=df['close'])
    return macd['MACDh_12_26_9'].iloc[-1] < 0 

def macd_signal_up_crossing(df):
    macd = ta.macd(close=df['close'])
    return macd['MACDh_12_26_9'].iloc[-1] > macd['MACDh_12_26_9'].iloc[-2] and macd['MACDh_12_26_9'].iloc[-1] > 0

def macd_signal_down_crossing(df):
    macd = ta.macd(close=df['close'])
    return macd['MACDh_12_26_9'].iloc[-1] < macd['MACDh_12_26_9'].iloc[-2] and macd['MACDh_12_26_9'].iloc[-1] < 0

def macd_signal_up(df):
    macd = ta.macd(close=df['close'])
    return macd['MACDh_12_26_9'].iloc[-1] > 0 


def stoc_signal_under_20(df):
    st= ta.stoch(high=df['high'],low=df['low'],close=df['close'])
    under_20= st['STOCHd_14_3_3'].iloc[-1] < 20
    return under_20

def above_sma_200(df):
    df['sma200'] = ta.sma(close=df['close'],length=200)
    df['sma50'] = ta.sma(close=df['close'],length=50)
    up = df['sma200'].tail(5).is_monotonic_increasing and df['close'].iloc[-1]>df['sma200'].iloc[-1]
 
 
def ema_cross_up(df):
    df['ema400'] = ta.sma(close=df['close'],length=45)
    df['ema100'] = ta.sma(close=df['close'],length=15)
    up = df['ema100'].iloc[-1]>df['ema400'].iloc[-1]and df['ema100'].iloc[-2]<df['ema400'].iloc[-2]
 
    return up 
def ema_cross_down(df):
    df['ema400'] = ta.sma(close=df['close'],length=45)
    df['ema100'] = ta.sma(close=df['close'],length=15)
    down = df['ema100'].iloc[-1]<df['ema400'].iloc[-1]and df['ema100'].iloc[-2]>df['ema400'].iloc[-2]
 
    return down
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
    
# x = get_klines.load_from_file()

# # stoc_signal(x)
# z = sma_200(x)
# print(z)