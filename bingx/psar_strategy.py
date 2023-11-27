from imports import *
from get_klines import np


def deep_dip_strategy(sy):
    
    timeframes = ['15m','1h','2h','4h']
    # timeframes = ['1h']
    for tf in timeframes:
        df = get_kline(sy,tf)
        # returns open, close, high, low, volume prices
        # df = pd.read_csv('xxx.csv')
        # df = pd.DataFrame(df)
        macd_short = False#macd_rsi_strategy_short(df)
        macd_long = macd_rsi_strategy_long(df)
        psar = psar_stoch_strategy(df)
        inside = inside_bar_bullish(df)
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

        if inside==1:
            print(f"{sy} got a inside bullish bar on timeframe : {tf}")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
        if inside==2:
            print(f"{sy} got a inside Bearish bar on timeframe : {tf}")
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
    
        
def macd_rsi_strategy_short(df):
        df['rsi'] = ta.rsi(df['close'],length=14)
        macd = ta.macd(close=df['close'])
        df['MACD'] = macd['MACDh_12_26_9']
        df['close']= df['close']
        macd_beaish = df['MACD'].iloc[-1] < 0 and df['MACD'].iloc[-2] > 0
        rsi_bearish = df['rsi'].iloc[-1] < 70 or df['rsi'].iloc[-2] < 70 or df['rsi'].iloc[-3] < 70 
        return macd_beaish and rsi_bearish
    
        
def macd_rsi_strategy_long(df):
        df['rsi'] = ta.rsi(df['close'],length=14)
        macd = ta.macd(close=df['close'])
        df['MACD'] = macd['MACDh_12_26_9']
        df['close']= df['close']
        macd_beaish = df['MACD'].iloc[-1] > 0 and df['MACD'].iloc[-2] < 0
        rsi_bearish = df['rsi'].iloc[-1] < 35 or df['rsi'].iloc[-2] < 35 or df['rsi'].iloc[-3] < 30 
        return macd_beaish and rsi_bearish
    
    
    
def inside_bar_bullish(df):
    previous_high = df['high'].iloc[-4]  
    previous_low = df['low'].iloc[-4]

    current_high = df['high'].iloc[-3]
    current_low = df['low'].iloc[-3]  

    is_inside = (current_high < previous_high) & (current_low > previous_low)  

    # Identify breakouts
    if is_inside:
        upside_breakout = df['high'].iloc[-2] > current_high
        downside_breakout = df['low'].iloc[-2] < current_low
        
        if upside_breakout:
            return 1
            
        if downside_breakout: 
            return 2
    return 0
    
# deep_dip_strategy('BTC-USDT')
   
tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=deep_dip_strategy)
