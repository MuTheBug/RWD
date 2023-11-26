from imports import *
from get_klines import np


def deep_dip_strategy(sy):
    
    timeframes = ['1m','3m','5m','15m','1h','2h','4h']
    timeframes = ['1h']
    for tf in timeframes:
        df = get_kline(sy,tf)
        # df = pd.read_csv('xxx.csv')
        # df = pd.DataFrame(df)
        macd_short = macd_stoch_strategy_short(df)
        macd_long = macd_stoch_strategy_long(df)
        psar = psar_stoch_strategy(df)
        if macd_short:
            print(f"{sy} got a MACD Bearish on timeframe : {tf}")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
        if macd_long:
            print(f"{sy} got a MACD Bullish on timeframe : {tf}")
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
        stoch['psrS'] = ~psar['PSARs_0.02_0.2'].isna()
        stoch['psrL'] = ~psar['PSARl_0.02_0.2'].isna()
        stoch['close']= df['close']
        stoch['stoch>70'] = stoch['STOCHd_14_3_3']>70 
        
        psrSignall = stoch['psrS'].iloc[-1] == True and stoch['psrS'].iloc[-1] == False
        psrSignal = stoch['stoch>70'].iloc[-1] and psrSignall

        return psrSignal              
        # stoch['psr<close'] = stoch['psr'] < 
        # print(stoch.tail(20))
        # return (stoch['STOCHd_14_3_3'].iloc[-1] < 70 and stoch['psr'].iloc[-1] > stoch['close'].iloc[-1]) and (stoch['psr'].iloc[-2] < stoch['close'].iloc[-2])
    
        
def macd_stoch_strategy_short(df):
        stoch = ta.stoch(high=df['high'],low=df['low'],close=df['close'])
        macd = ta.macd(close=df['close'])
        stoch['MACD'] = macd['MACDh_12_26_9']
        stoch['close']= df['close']
        macd_beaish = stoch['MACD'].iloc[-1] < 0 and stoch['MACD'].iloc[-2] > 0

        return stoch['STOCHd_14_3_3'].iloc[-1] >70 and macd_beaish
    
        
def macd_stoch_strategy_long(df):
        stoch = ta.stoch(high=df['high'],low=df['low'],close=df['close'])
        macd = ta.macd(close=df['close'])
        stoch['MACD'] = macd['MACDh_12_26_9']
        stoch['close']= df['close']
        macd_beaish = stoch['MACD'].iloc[-1] > 0 and stoch['MACD'].iloc[-2] < 0

        return stoch['STOCHd_14_3_3'].iloc[-1] <33 and macd_beaish
    

# deep_dip_strategy('BTC-USDT')
   
tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=deep_dip_strategy)
