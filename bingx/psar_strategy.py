from imports import *
from get_klines import np


def deep_dip_strategy(sy):
    
    timeframes = ['1m','3m','5m','15m','1h','2h','4h']
    timeframes = ['1h']
    for tf in timeframes:
        df = get_kline(sy,tf)
        macd = macd_stoch_strategy(df)
        psar = psar_stoch_strategy(df)
        if macd:
            print(f"{sy} got a MACD Bearish on timeframe : {tf}")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
        if psar:
            print(f"{sy} got a Parbolic Sar Bearish on timeframe : {tf}")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
        else:
            print(f"skip {sy} on {tf}")

def psar_stoch_strategy(df):
        stoch = ta.stoch(high=df['high'],low=df['low'],close=df['close'])
        psar = ta.psar(high=df['high'],low=df['low'],close=df['close'])
        stoch['psr'] = psar['PSARs_0.02_0.2']
        stoch['close']= df['close']
        stoch['signal'] = np.where(stoch['STOCHd_14_3_3'] > 70) and (stoch['psr'] > stoch['close'])
        # print(psar)
        # print(stoch.tail(20))
        return stoch['signal'].iloc[-1] and not stoch['signal'].iloc[-2]
    
        
def macd_stoch_strategy(df):
        stoch = ta.stoch(high=df['high'],low=df['low'],close=df['close'])
        macd = ta.macd(close=df['close'])
        stoch['MACD'] = macd['MACDh_12_26_9']
        stoch['close']= df['close']
        macd_beaish = stoch['MACD'].iloc[-1] < 0 and stoch['MACD'].iloc[-2] > 0

        return stoch['STOCHd_14_3_3'].iloc[-1] >70 and macd_beaish
    

   
tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=deep_dip_strategy)
