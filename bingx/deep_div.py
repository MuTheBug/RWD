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
def sma100(data):
    
    data['sma100'] = ta.sma(close=data['close'],length=100)
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
def stoch(data):
    stoch = ta.stoch(high=data['high'],low=data['low'],close=data['close'])
    data['STOCHd_14_3_3'] = stoch['STOCHd_14_3_3']
    data['STOCHk_14_3_3'] = stoch['STOCHk_14_3_3']
    return data
def p_sar(data):
    psar = ta.psar(high=data['high'],low=data['low'],close=data['close'])
    data['psar'] = psar['PSARs_0.02_0.2']
    return data
def prixxxxxnt(df,sy,tf):
    counter = 0
    df = df.to_dict()
    for key, val in df.items():
        if val[899]:
            counter +=1
            print(f"{sy} has {key} indicators as true on {tf}")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
            return True
    print(f"skip {sy} on {tf}")
    return False
    
    # print(df)
def deep_dip_strategy(sy):
    
    timeframes = ['1m','3m','5m','15m','1h','2h','4h']
    for tf in timeframes:
        df = get_kline(sy,tf)


        df = sma250(df)
        df = sma200(df)
        df = sma20(df)
        df = sma26(df)
        df = sma9(df)
        df = stoch(df)
        df = p_sar(df)
        df['atr'] = ta.atr(close=df['close'],high=df['high'],low=df['low'],length=14) 

        df = rsi(df)
        mac = macd(df)
        kc = keltner(df)
        df['vol_signal'] = np.where((df['volume'].iloc[-1] > df['volume'].iloc[-2]> df['volume'].iloc[-3]), True, False)
        df['sma200_signal'] = np.where((df['sma200'].iloc[-2]>df['close'].iloc[-2] and df['sma200'].iloc[-1]<df['close'].iloc[-1] ),True,False)
        df['sma250_signal'] = np.where((df['sma250'].iloc[-2]>df['close'].iloc[-2] and df['sma250'].iloc[-1]<df['close'].iloc[-1] ),True,False)
        df['sma_cross_signal'] = np.where((df['sma9'].iloc[-1]<df['sma26'].iloc[-1] and df['sma9'].iloc[-2]>df['sma26'].iloc[-2] ),True,False)
        df['rsi_signal'] = np.where((df['rsi'].iloc[-2]<=30 and df['rsi'].iloc[-1]>70 ),True,False)
        df['rsi_oversold'] = np.where((df['rsi'].iloc[-2]<=30),True,False)
        df['rsi_over_50'] = np.where((df['rsi'].iloc[-1]<=50),True,False)
        df['rsi_overbought'] = np.where((df['rsi'].iloc[-1]>70),True,False)
        df['price_under_sma20'] = df['sma20']>df['close']
        df['atr_tp'] = df['atr_tp'] = df['close'] + (df['atr'] * 1.5)
        df['macd_signal'] = np.where((mac['MACDh_26_50_9'].iloc[-1] > 0 and mac['MACDh_26_50_9'].iloc[-2] <= 0), True, False)
        df['macd_signal_short'] = np.where((mac['MACDh_26_50_9'].iloc[-1] < 0 and mac['MACDh_26_50_9'].iloc[-2] >= 0), True, False)
        
        df['kc_signal'] = df['close'] <= df['third_kc']
        df['ha_signal'] = np.where(df['HA_Close'].iloc[-2] > df['HA_Close'].iloc[-3] and df['HA_Close'].iloc[-4] > df['HA_Close'].iloc[-2],True,False)

        psar_stoch_strategy=(df['psar'].iloc[-2]> df['close'].iloc[-2])and (df['STOCHd_14_3_3'].iloc[-2]>70)
        ma_stoch_strategy=(df['STOCHd_14_3_3'].iloc[-1] > 70 ) and  (df['close'].iloc[-1] < df['sma100'].iloc[-1])

        macd_rsi_strategy_long= df['macd_signal'].iloc[-1] and df['rsi_oversold'].iloc[-1]
            
        macd_rsi_strategy_short=df['macd_signal_short'].iloc[-1] and df['rsi_overbought'].iloc[-1]
   
        
        selected_columns = [psar_stoch_strategy,ma_stoch_strategy,macd_rsi_strategy_long,macd_rsi_strategy_short]

        print(f'{sy}:  {selected_columns}  on {tf}')
            # send_to_telegram(f"{sy} on {tf}")
        
        # print(f"skip {sy} on {tf}")
        # prixxxxxnt(selected_columns,sy,tf)
        # print(selected_columns)
  
  
# deep_dip_strategy('BTC-USDT')   
   
tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=deep_dip_strategy)
