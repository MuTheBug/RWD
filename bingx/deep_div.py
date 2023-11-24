from imports import *
from get_klines import np

def sma200(data):
    
    data['sma200'] = ta.sma(close=data['close'],length=200)
    return data
def sma250(data):
    
    data['sma250'] = ta.sma(close=data['close'],length=250)
    return data
def sma20(data):
    
    data['sma20'] = ta.sma(close=data['close'],length=20)
    return data
def sma9(data):
    
    data['sma9'] = ta.sma(close=data['close'],length=9)
    return data
def sma26(data):
    
    data['sma26'] = ta.sma(close=data['close'],length=26)
    return data
def macd(data):
    macd = ta.macd(close=data['close'],fast=26,slow=50)
    return macd

def rsi(data):
    data['rsi'] = ta.rsi(close=data['close'],length=14)
    return data
def keltner(data):
    multiplier = 3  # The multiplier for the ATR

    # Calculate the Average True Range (ATR)
    atr = data['atr'].iloc[-1]
    # Calculate the Upper Channel
    upper_channel = data['high'] + (multiplier * atr)

    # Calculate the Middle Channel
    middle_channel = data['low'] - (multiplier * atr)

    # Calculate the Lower Channel
    lower_channel = data['low'] - (2 * multiplier * atr)
    data['lower_channel'] = lower_channel
    data['middle_channel'] = middle_channel
    data['third_kc'] = ((data['middle_channel'] - data['lower_channel']) / 2) + data['lower_channel']
    return data
def prixxxxxnt(df,sy,tf):
    counter = 0
    df = df.to_dict()
    for key, val in df.items():
        if val[899]:
            counter +=1
    if counter >= 3:
        print(f"{sy} has {counter} indicators as true on {tf}")
        for key, val in df.items():
            if val[899]:
                print(f"{counter} : {key}")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
            
    # print(df)
def deep_dip_strategy(sy):
    
    timeframes = ['1h','2h','4h']
    for tf in timeframes:
        df = get_kline(sy,tf)
        df = sma250(df)
        df = sma200(df)
        df = sma20(df)
        df = sma26(df)
        df = sma9(df)
        df['atr'] = ta.atr(close=df['close'],high=df['high'],low=df['low'],length=14) 

        df = rsi(df)
        mac = macd(df)
        kc = keltner(df)
        df['vol_signal'] = np.where((df['volume'].iloc[-2] > df['volume'].iloc[-3]> df['volume'].iloc[-4]), True, False)
        df['sma200_signal'] = np.where((df['sma200'].iloc[-3]>df['close'].iloc[-3] and df['sma200'].iloc[-2]<df['close'].iloc[-2] ),True,False)
        df['sma250_signal'] = np.where((df['sma250'].iloc[-3]>df['close'].iloc[-3] and df['sma250'].iloc[-2]<df['close'].iloc[-2] ),True,False)
        df['sma_cross_signal'] = np.where((df['sma9'].iloc[-3]<df['sma26'].iloc[-3] and df['sma9'].iloc[-2]>df['sma26'].iloc[-2] ),True,False)
        df['rsi_signal'] = np.where((df['rsi'].iloc[-3]<=30 and df['rsi'].iloc[-2]>70 ),True,False)
        df['rsi_oversold'] = np.where((df['rsi'].iloc[-2]<=30),True,False)
        df['rsi_over_50'] = np.where((df['rsi'].iloc[-2]<=50),True,False)
        df['rsi_overbought'] = np.where((df['rsi'].iloc[-2]>70),True,False)
        df['price_under_sma20'] = df['sma20']>df['close']
        df['atr_tp'] = df['atr_tp'] = df['close'] + (df['atr'] * 1.5)
        df['macd_signal'] = np.where((mac['MACDh_26_50_9'].iloc[-2] > 0 and mac['MACDh_26_50_9'].iloc[-3] <= 0), True, False)
        df['kc_signal'] = df['close'] <= df['third_kc']
        df['ha_signal'] = np.where(df['HA_Close'].iloc[-2] > df['HA_Close'].iloc[-3] and df['HA_Close'].iloc[-4] > df['HA_Close'].iloc[-2],True,False)
        selected_columns = df[['sma250_signal','vol_signal','rsi_oversold','price_under_sma20','macd_signal','kc_signal','rsi_over_50','sma200_signal','ha_signal']]
        
        selected_columns = selected_columns.tail(1)
        prixxxxxnt(selected_columns,sy,tf)
  
  
# deep_dip_strategy('BTC-USDT')      
tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=deep_dip_strategy)
