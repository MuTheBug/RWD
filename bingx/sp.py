import pandas as pd
from datetime import datetime
import pandas_ta as ta
import requests

asset = input("Please enter asset symbol: ")
asset = asset.upper()
asset+="-USDT"
timeframe = input("Please enter timeframe: ")
price = float(input("Please enter your open price: "))


def get_kline(symbol='IMX-USDT',timeframe='4h',pr=0.0):
    
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
    try:
        data['close'] = data['close'].astype(float) 
    except ValueError:
        print('error in parsing')
        pass # skip row
    data['time'] =pd.to_datetime(data['time'],unit='ms')
    data['sma250'] = ta.sma(data['close'],length=250)
    data['high'] = data.high.astype(float)
    data['low'] = data.low.astype(float)
    data['atr'] = ta.atr(high=data['high'],low=data['low'],close=data['close'],length=14)
    atr = data['atr'].iloc[-1]

    tp = pr + (atr * 1.5)
    
    sl = pr - (atr * 1)
    print("TAKE PROFIT:")
    print(tp)
    print("STOP LOSS:")
    print(sl)
    


get_kline(asset,timeframe=timeframe,pr=price)