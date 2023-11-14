from datetime import datetime
import numpy as np
import requests
import pandas as pd


# class Alert:
#     pair = 'BTC-USDT'
#     pairs = {}
#     url = "https://open-api.bingx.com/openApi/swap/v2/quote/price"
#     params = {
#         'symbol' : pair,
#     }
#     def __init__(self):
#         try:
#             request = requests.get(url=self.url,params=self.params)
#             price = float(request.json()['data']['price'])
#             print(price)
#         except Exception as e:
#             print(e)
import pandas as pd
from sklearn.linear_model import LinearRegression
def get_kline(symbol='AVAX-USDT',timeframe='15m'):
    now = datetime.now()
    now_seconds = int(now.timestamp()*1000) 
    nine_days = 350 * 24 * 60 * 60 *1000
    nine_days_ago = now_seconds - nine_days
    future= "/openApi/swap/v3/quote/klines"
    url= "https://open-api.bingx.com"+future
    params={
        'symbol':f'{symbol}',
        'interval':timeframe,
        'limit':400,
        'start_time':nine_days_ago,
        'end_time':now_seconds,
    }
    data = requests.get(url=url,params=params)
    data=data.json()['data'][::-1]  
    data = pd.DataFrame(data)
    data['high'] = data.high.astype(float)
    data['low'] = data.low.astype(float)
    # returns columns open, close, high, low, volume, and time
    return data

df = get_kline()

# Get last 20 rows
recent_df = df.tail(20)

# Get top 5 high prices 
highs = recent_df['high'].nlargest(5).tolist()

# Empty list to store trendline data
trendlines = [] 

# Loop through pairs of highs
for i in range(len(highs)-1):

  x1 = [i].reshape(-1, 1)
  x2 = [i+1].reshape(-1, 1)
  
  y1 = [highs[i]] 
  y2 = [highs[i+1]]

  X = np.concatenate((x1, x2), axis=0)
  Y = y1 + y2

  # Rest of code...
  
  # Predict for a future 100 periods
  x_future = [[i+2], [i+3], ..., [i+100]]
  y_pred = regr.predict(x_future)
  
  # Add to list
  trendlines.append(y_pred)
  
# Concatenate all trendlines  
trendline_values = np.concatenate(trendlines)
print(trendline_values)

