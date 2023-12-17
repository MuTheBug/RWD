import pandas as pd
from datetime import datetime
import pandas_ta as ta
import requests
from get_klines import get_kline
pd.set_option('display.max_rows', None)
# asset = input("Please enter asset symbol: ")
# asset = asset.upper()
# asset+="-USDT"
# timeframe = input("Please enter timeframe: ")
# price = float(input("Please enter your open price: "))






def analyis_rsi(df):
    df['rsi'] = ta.rsi(close=df.close,length=14)
    rsi_now = df.rsi.iloc[-1]
    rsi_nows = df.rsi.iloc[-1]
    pre = df.rsi.iloc[-2]
    is_slopping_up = df.rsi.tail(2).is_monotonic_increasing
    is_slopping_down = df.rsi.tail(2).is_monotonic_decreasing
    
    if rsi_now>70 :
        rsi_now = "overbought"
    elif rsi_now<30:
        rsi_now = "oversold"
    else:
        rsi_now = "neutral"
    sloop = "it has no sloop"
    if is_slopping_up:
        sloop = "it is sloping up ↑"
    if is_slopping_down :
        sloop = "it is sloping down ↓"
        
    return {"rsi_now":rsi_now,"sloop":sloop,'current_value':rsi_nows,'pre_rsi':pre}
def analyis_sma(df,length):
    
    key_name = 'sma'+str(length)
    df[key_name] = ta.sma(close=df.close,length=length)
    rsi_now = df[key_name].iloc[-1].astype(float)
    is_slopping_up = df[key_name].tail(10).is_monotonic_increasing
    is_slopping_down = df[key_name].tail(10).is_monotonic_decreasing
    current_price = df['close'].iloc[-1].astype(float)
    rsi_case = ""
    if rsi_now<current_price:
        rsi_case = f"above the {key_name}"
    if rsi_now>current_price:
        rsi_case = f"under the {key_name}"
    # if rsi_now<current_price:
    #     rsi_now = f"below the {key_name}"
    sloop = "Sideways"
    if is_slopping_up:
        sloop = "it is sloping up ↑"
    if is_slopping_down :
        sloop = "it is sloping down ↓"
        
    return {"sma_now":rsi_case,"sloop":sloop}

def sr(df):
    close = df.close.iloc[-1]
    support = df.high.tail(50).min()
    resistance = df.high.tail(50).max()
    mea = df.close.tail(50).mean()
    return {'close':close,'support':support,'resistance':resistance, 'mean':mea}

symbol = 'BTC-USDT'
df1d= get_kline('BTC-USDT',timeframe='1d')
df12h= get_kline('BTC-USDT',timeframe='12h')
df8h= get_kline('BTC-USDT',timeframe='8h')
df4h= get_kline('BTC-USDT',timeframe='4h')

macd = ta.macd(close=df1d['close'])
macd1 = macd['MACDh_12_26_9'].iloc[-1]
prem1= macd['MACDh_12_26_9'].iloc[-2]
macd = ta.macd(close=df12h['close'])
macd2 = macd['MACDh_12_26_9'].iloc[-1]
prem2= macd['MACDh_12_26_9'].iloc[-2]

macd = ta.macd(close=df8h['close'])
macd3 = macd['MACDh_12_26_9'].iloc[-1]
prem3= macd['MACDh_12_26_9'].iloc[-2]

macd = ta.macd(close=df4h['close'])
macd4 = macd['MACDh_12_26_9'].iloc[-1]
prem4= macd['MACDh_12_26_9'].iloc[-2]

print("I am using macd cross to enter trades, I am using MACD cross, however it gives me contradicted signals on different timeframes, what should I do here is the macd info")
print("daily timeframe :"+ str(macd1) + "and the previous signal is: " + str(prem1))
print("12h timeframe :"+ str(macd1) + "and the previous signal is: " + str(prem2))
print("8h timeframe :"+ str(macd1) + "and the previous signal is: " + str(prem3))
print("4h timeframe :"+ str(macd1) + "and the previous signal is: " + str(prem4))



# sma_50 = analyis_sma(x,50)
# sma_250 = analyis_sma(x,250)
# rsi_ann = analyis_rsi(x)
# srv = sr(x)
# print(f'{symbol} current price is : {srv["close"]} ')
# print(f'{symbol} mean is : {srv["mean"]} ')
# print(f'{symbol} current resistance is : {srv["resistance"]} ')
# print(f'{symbol} current support is : {srv["support"]} ')
# print(f'{symbol} is {sma_50["sma_now"]} and {sma_50["sloop"]}')
# print(f'{symbol} is {sma_250["sma_now"]} and {sma_250["sloop"]}')
# print(f'{symbol} Rsi is {rsi_ann["rsi_now"]} and {rsi_ann["sloop"]}')
# print(f'Rsi is now {rsi_ann["current_value"]} and was {rsi_ann["pre_rsi"]}')
# price_data = get_kline('SAND-USDT','1d')
# returns data like :
#            open    close     high      low     volume       time   HA_Close       HA_Open       HA_High        HA_Low
# 0    34701.0  34491.5  35284.6  33877.3   17127.08 2021-06-28  34588.600  34596.250000  35284.600000  33877.300000
# 1    34493.5  35923.6  36601.5  34231.3   16705.51 2021-06-29  35312.475  34954.362500  36601.500000  34231.300000

# please write a network ai python script to predict the price of the asset and print the prediction