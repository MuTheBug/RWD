
from imports import *
import get_klines
def macd_signal(df):
    macd = ta.macd(close=df['close'])
    macd['signal'] = (macd['MACDh_12_26_9'] > 0) & (macd['MACDh_12_26_9'].shift(1) < 0)
    return macd['signal'].iloc[-1]

def stoc_signal_above_80(df):
    st= ta.stoch(high=df['high'],low=df['low'],close=df['close'])
    above_80= st['STOCHd_14_3_3'].iloc[-1] > 80
    return above_80

def stoc_signal_under_20(df):
    st= ta.stoch(high=df['high'],low=df['low'],close=df['close'])
    under_20= st['STOCHd_14_3_3'].iloc[-1] < 20
    return under_20

def sma_200(df):
    df['sma200'] = ta.sma(close=df['close'],length=200)
    df['sma50'] = ta.sma(close=df['close'],length=50)
    up = df['sma200'].tail(10).is_monotonic_increasing
    down = df['sma200'].tail(10).is_monotonic_decreasing
    
    x={'down':down,'up':up}
    return x

def rsi_sloping_up(df):
    df['rsi'] = ta.rsi(close=df['close'],length=14)
    # slice = df['rsi'].tail(2).is_monotonic_increasing
    under_40 = df['rsi'].iloc[-2] <=30 and df['rsi'].iloc[-1] > 30
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