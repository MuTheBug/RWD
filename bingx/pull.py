from apis import *
import pandas as pd
from datetime import datetime
import pandas_ta as ta
import requests


def foolproof_strategy(sy):
    timeframes = ['1m','3m','5m','15m','1h','2h','4h','8h','1d']
    # timeframes = ['1h']
    for tf in timeframes:
        data= get_kline(sy,timeframe=tf)
        try:
            data['close'] = data['close'].astype(float) 
        except ValueError:
            print('error in parsing')
            pass # skip row
        data['sma200'] = ta.sma(data['close'],length=200)
        data['sma50'] = ta.sma(data['close'],length=50)
        data['sma20'] = ta.sma(data['close'],length=20)
        data['sma10'] = ta.sma(data['close'],length=10)
        data['sma5'] = ta.sma(data['close'],length=5)
        data['sma'] = (data['sma200'] < data['sma50']) & (data['sma50'] < data['sma20']) & (data['sma20'] < data['sma10']) & (data['sma10'] < data['sma5'])
        data['rsi'] = ta.rsi(data['close'],length=14)
        macd = ta.macd(close=data['close'])
        pre_histogram = macd['MACDh_12_26_9'].iloc[-2]
        current_histogram = macd['MACDh_12_26_9'].iloc[-1]
        histogram_signal = pre_histogram <=0 and current_histogram >=0
        long = data['sma200'].iloc[-1]<data['sma50'].iloc[-1]<data['close'].iloc[-1] and data['close'].iloc[-1] <=data['sma20'].iloc[-1]
        long = data['sma200'].iloc[-1]<data['close'].iloc[-1] and data['rsi'].iloc[-1] <=30
        long = data['sma'].iloc[-1]
        if long:
            send_to_telegram(f'{sy} on {tf} rsi')
        else:
            print(f'skip {sy} on {tf}')

            

    
