from datetime import datetime
import pandas as pd
import requests
import numpy as np

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
        'limit':900,
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
        data['open'] = data.open.astype(float)
        data['volume'] = data.volume.astype(float)
        
    except ValueError:
        print('error in parsing')
        pass # skip row
    data['time'] =pd.to_datetime(data['time'],unit='ms')
    
    data['HA_Close'] = (data['open'] + data['high'] + data['low'] + data['close']) / 4

    ha_open = [ (data.iloc[0]['open'] + data.iloc[0]['close'])/2 ]
    for i in range(1, len(data.index)):
        ha_open.append((ha_open[i-1] + data.iloc[i]['HA_Close'])/2)
    data['HA_Open'] = np.array(ha_open)

    data['HA_High'] = data[['HA_Open','HA_Close','high']].max(axis=1)
    data['HA_Low'] = data[['HA_Open','HA_Close','low']].min(axis=1)
    # data.to_csv('file.csv')
    return data

