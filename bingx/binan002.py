from apis import *
import pandas as pd
from datetime import datetime
import pandas_ta as ta
import concurrent.futures
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
    data = requests.get(url=url,params=params)

    # print(data.url)
    data=data.json()['data'][::-1]
    
    data = pd.DataFrame(data)
    data['time'] =pd.to_datetime(data['time'],unit='ms')
    data['sma250'] = ta.sma(data['close'],length=250)
    data['high'] = data.high.astype(float)
    data['low'] = data.low.astype(float)
    return data


def get_symbols():
        try:
            url= "https://open-api.bingx.com/openApi/swap/v2/quote/ticker"

            tickers = requests.get(url=url).json()['data']
            data = pd.DataFrame(tickers)['symbol']
            return data.to_list()
        
        except Exception as e:

            print(e)




def ichi_strategy(sy):


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
                        third_res = ich['long_entry'].iloc[-1]
                        greatest_level = ich['pullback_618'].iloc[-1]
                        if first_res and second_res and third_res and greatest_level:
                            print(sy + " is a good trade ++++++++++++++++++++")
                            send_to_telegram(f'{sy} is at 0.618')
                        else:
                            print(f"skipping {sy}")
                        break
                    except Exception as e:
                        print(e)
                        break

                
            


def calculate_ichi(data):
    conversion_line = (data['high'].rolling(9).max() + data['low'].rolling(9).min()) / 2
    basis_line = (data['high'].rolling(26).max() + data['low'].rolling(26).min()) / 2  
    span_a = (conversion_line + basis_line) / 2
    span_b = (data['high'].rolling(52).max() + data['low'].rolling(52).min()) / 2

    # Add Ichimoku columns
    data['conversion_line'] = conversion_line
    data['basis_line'] = basis_line 
    data['span_a'] = span_a
    data['span_b'] = span_b
    data['span_a'] = pd.to_numeric(data['span_a']) 
    data['close'] = pd.to_numeric(data['close']) 
    data['conversion_line'] = pd.to_numeric(data['conversion_line'])
    data['basis_line'] = pd.to_numeric(data['basis_line'])
    # Long entry
    data['long_entry'] = (data['close'] > data['span_a']) & (data['conversion_line'] > data['basis_line']) 

    # # Long exit 
    data['long_exit'] = (data['conversion_line'] < data['basis_line'])

    # # Short entry
    data['short_entry'] = (data['close'] < data['span_a']) & (data['conversion_line'] < data['basis_line'])

    # # Short exit
    data['short_exit'] = (data['conversion_line'] > data['basis_line']) 
    # Check if price is above Cloud (Kumo)
    data['price_above_cloud'] = data['close'] > data['span_a'] 

    # Check if conversion line is above basis line
    data['cline_above_bline'] = data['conversion_line'] > data['basis_line']

    # Check if span A is above span B 
    data['spanA_above_spanB'] = data['span_a'] > data['span_b']

    # Overall uptrend condition
    data['uptrend'] = (data['price_above_cloud'] & 
                    data['cline_above_bline'] &  
                    data['spanA_above_spanB'])
    swing_high = data['high'].rolling(20).max()
    swing_low = data['low'].rolling(20).min()
    swing = swing_high - swing_low
    level_236 = swing * 0.236
    level_382 = swing * 0.382
    level_618 = swing * 0.618
    data['pullback_236'] = data['low'] <= (swing_high - level_236)
    data['pullback_382'] = data['low'] <= (swing_high - level_382)
    level_50 = swing * 0.55 # 50% level
    data['pullback_50'] = data['low'] <= (swing_high - level_50) # 50% level
    data['pullback_618'] = data['low'] <= (swing_high - level_618) # 618 level
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


# ichi_strategy()


def main(tickers):
  
  
  with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(ichi_strategy, sy) for sy in tickers]
  
  for f in concurrent.futures.as_completed(results):
    f.result()
      
if __name__ == '__main__':
  tickers = get_symbols()

  main(tickers)












