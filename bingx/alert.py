from datetime import datetime
import numpy as np
import requests
import pandas as pd

import pandas as pd
from sklearn.linear_model import LinearRegression


def get_kline(symbol="AVAX-USDT", timeframe="1h"):
    now = datetime.now()
    now_seconds = int(now.timestamp() * 1000)
    nine_days = 350 * 24 * 60 * 60 * 1000
    nine_days_ago = now_seconds - nine_days
    future = "/openApi/swap/v3/quote/klines"
    url = "https://open-api.bingx.com" + future
    params = {
        "symbol": f"{symbol}",
        "interval": timeframe,
        "limit": 400,
        "start_time": nine_days_ago,
        "end_time": now_seconds,
    }
    data = requests.get(url=url, params=params)
    data = data.json()["data"][::-1]
    data = pd.DataFrame(data)
    data["high"] = data.high.astype(float)
    data["low"] = data.low.astype(float)
    data['close'] = pd.to_numeric(data['close']) 
# returns columns open, close, high, low, volume, and time
    return data
print(get_kline("DOGE-USDT",timeframe='15m').tail(50))