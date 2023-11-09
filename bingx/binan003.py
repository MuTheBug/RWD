from apis import *
import pandas as pd
from datetime import datetime
import pandas_ta as ta

# from bingX import BingX
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
        'limit':900,
        'start_time':nine_days_ago,
        'end_time':now_seconds,
    }
    data = requests.get(url=url,params=params).json()['data'][::-1]

    data = pd.DataFrame(data)
    data['time'] =pd.to_datetime(data['time'],unit='ms')
    data['sma250'] = ta.sma(data['close'],length=250)
    data['high'] = data.high.astype(float)
    data['low'] = data.low.astype(float)
    return data


def get_symbols():
        url= "https://open-api.bingx.com/openApi/swap/v2/quote/ticker"

        tickers = requests.get(url=url).json()['data']
        data = pd.DataFrame(tickers)['symbol']
        return data.to_list()




def ichi_strategy():
    while True:
        try:
            tickers = get_symbols()
            for sy in tickers:
                while True:
                    try:
                        # 1 Day timeframe
                        kline = get_kline(sy,timeframe='1d')
                        ich = calculate_ichi(kline)
                        first_res = ich['long_entry'].iloc[-1]
                        # 4 hours timeframe
                        kline = get_kline(sy,timeframe='4h')
                        ich = calculate_ichi(kline)
                        second_res = ich['long_entry'].iloc[-1]
                        # 1 hour timeframe
                        kline = get_kline(sy,timeframe='1h')
                        ich = calculate_ichi(kline)
                        vbp = ich['vpb'].iloc[-1]


                   
                        if first_res and second_res and vbp:
                            print(sy + " is a good trade ++++++++++++++++++++")
                            send_to_telegram(f'{sy}')
                        else:
                            print(f"skipping {sy}")
                        break
                    except Exception as e:
                        print(e)
                        break
        except Exception as e:
            print(e)
                
            




def calculate_ichi(data):

  # Calculate Ichimoku line values
  conversion_line = (data['high'].rolling(9).max() + data['low'].rolling(9).min()) / 2
  basis_line = (data['high'].rolling(26).max() + data['low'].rolling(26).min()) / 2  
  span_a = (conversion_line + basis_line) / 2
  span_b = (data['high'].rolling(52).max() + data['low'].rolling(52).min()) / 2

  # Add to dataframe
  data['conversion_line'] = conversion_line
  data['basis_line'] = basis_line
  data['span_a'] = span_a
  data['span_b'] = span_b
  data['span_a'] = pd.to_numeric(data['span_a']) 
  data['close'] = pd.to_numeric(data['close']) 
  data['long_entry'] = (data['close'] > data['span_a']) & (data['conversion_line'] > data['basis_line']) 

  # Ensure numeric columns
  data['conversion_line'] = pd.to_numeric(data['conversion_line'])
  data['basis_line'] = pd.to_numeric(data['basis_line'])
  data['close'] = pd.to_numeric(data['close'])
  data['span_a'] = pd.to_numeric(data['span_a'])

  # Define uptrend condition
  data['uptrend'] = (data['close'] > data['span_a']) & (data['conversion_line'] > data['basis_line'])

  # Pullbacks
  swing_high = data['high'].rolling(20).max()
  valid_pullback = data['low'] > span_a # Could also check span_b
  touch_span = data['low'] <= span_a
  no_break_span = data['low'] > span_a

  # Ideal pullback
  ideal_pullback = touch_span & no_break_span

  # Long and short entry rules
  data['vpb'] = ideal_pullback 
#   data['short_entry'] = ~data['uptrend'] & ideal_pullback

  # Exits here

  return data

def send_to_telegram(message):

    apiToken = API_TOKEN
    chatID = CHAT_ID
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    message = str(message)

    try:
        response = requests.post(
            apiURL, json={'chat_id': chatID, 'text': message, 'parse_mode': 'html'})
    except Exception as e:
        print(e)


ichi_strategy()
















def sma250_strategy():

    tickers = get_symbols()
    while True:
        for sy in tickers:
            while True:
                try:
                    data = get_kline(sy)
                    before_last_close = float(data['close'].iloc[-2])
                    last_close = float(data['close'].iloc[-1])
                    before_last_sma = float(data['sma250'].iloc[-2])
                    last_sma = float(data['sma250'].iloc[-1])

                    conditions = before_last_close<before_last_sma and last_close > last_sma
                    if conditions:
                        print(sy + " is a good trade ++++++++++++++++++++")
                    else:
                        print(f"skipping {sy}")
                    break
                except Exception as e:

                    break
