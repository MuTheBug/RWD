from apis import *
import pandas as pd
from datetime import datetime
import pandas_ta as ta
import concurrent.futures
import requests
import time

def get_kline(symbol='IMX-USDT',timeframe='4h'):
    
    now = datetime.now()
    now_seconds = int(now.timestamp()*1000) 
    nine_days = 350 * 24 * 60 * 60 *1000
    nine_days_ago = now_seconds - nine_days
    future= "/openApi/swap/v3/quote/klines"
    url= "https://open-api.bingx.com"+future
    params={
        'symbol':f'{symbol}',
        'interval':timeframe,
        'limit':800,
        'start_time':nine_days_ago,
        'end_time':now_seconds,
    }
    data = requests.get(url=url,params=params)

    # print(data.url)
    data=data.json()['data'][::-1]
    
    data = pd.DataFrame(data)
    data['time'] =pd.to_datetime(data['time'],unit='ms')
    data['sma250'] = ta.sma(data['close'],length=250)
    data['high'] = data.high.astype(float)
    data['low'] = data.low.astype(float)
    # returns columns open, close, high, low, volume, and time
    return data

def foolproof_strategy(sy):
    timeframes = ['15m','1h','2h','4h','8h','1d']
    
    for tf in timeframes:
        data= get_kline(data,timeframe=tf)
        try:
            data['close'] = data['close'].astype(float) 
        except ValueError:
            print('error in parsing')
            pass # skip row
        data['sma200'] = ta.sma(data['close'],length=200)
        data['sma50'] = ta.sma(data['close'],length=50)
        data['sma20'] = ta.sma(data['close'],length=20)
        data['rsi'] = ta.rsi(data['close'],length=14)
        long = data['sma200'].iloc[-1]<data['sma50'].iloc[-1]<data['close'].iloc[-1] and data['rsi'].iloc[-1] <=30
        short = data['sma200'].iloc[-1]<data['sma50'].iloc[-1]<data['close'].iloc[-1] and data['rsi'].iloc[-1] <=70
        if long:
            print(f'long +++++++++++++++++ {sy} on {tf}')
        elif short:
            print(f'short ----------------- {sy} on {tf}')
        else:
            print('skip {sy} on {tf}')

            

def get_symbols():
        try:
            url= "https://open-api.bingx.com/openApi/swap/v2/quote/ticker"

            tickers = requests.get(url=url).json()['data']
            data = pd.DataFrame(tickers)['symbol']
            return data.to_list()
        
        except Exception as e:

            print("error in getting symbols")
            pass



    


def main(tickers):
  
  
  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = [executor.submit(foolproof_strategy, sy) for sy in tickers]
  
  for f in concurrent.futures.as_completed(results):
    f.result()
      
if __name__ == '__main__':
    while 1:
        try:
            tickers = get_symbols()
            main(tickers)
            print(tickers)
            print("sleeping a while... ")
            time.sleep(10)
        except KeyboardInterrupt as e:
            print("ok .. ending")
        except Exception as f:
            print(f)
            pass
        