from datetime import datetime
import pandas as pd
import requests


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
    try:
        data['close'] = data['close'].astype(float)
        data['high'] = data.high.astype(float)
        data['low'] = data.low.astype(float)
    except ValueError:
        print('error in parsing')
        pass # skip row
    data['time'] =pd.to_datetime(data['time'],unit='ms')

    return data