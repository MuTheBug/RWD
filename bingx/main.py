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
def calculate_sma(data):
     previous_sma = data['sma250'].iloc[-2]
     current_sma = data['sma250'].iloc[-1]
     previous_close = data['close'].iloc[-2]
     current_close = data['close'].iloc[-1]

     return (float(previous_sma) > float(previous_close)) and (float(current_sma) < float(current_close))
def sma_strategy(sy):
      timeFrames = ['5m','10m','15m']
      for tf in timeFrames:
        kline = get_kline(sy,timeframe=tf)
        sma = calculate_sma(kline)
        if sma:
            print(f"{sy} is a good trade ++++++++++++++++++++ on {tf}")
        else:
            print(f"skip {sy} on {tf}")
            # print('.')
            pass
def get_symbols():
        try:
            url= "https://open-api.bingx.com/openApi/swap/v2/quote/ticker"

            tickers = requests.get(url=url).json()['data']
            data = pd.DataFrame(tickers)['symbol']
            return data.to_list()
        
        except Exception as e:

            # print(e)
            pass




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



                        kline = get_kline(sy,timeframe='15m')
                        ich = calculate_ichi(kline)
                        fourth_res = ich['long_entry'].iloc[-1]



                        # kline = get_kline(sy,timeframe='5m')
                        # ich = calculate_ichi(kline)
                        # fifth_res = not ich['long_entry'].iloc[-1]
                        # kline = get_kline(sy,timeframe='3m')
                        # ich = calculate_ichi(kline)
                        # sixth_res = not ich['long_entry'].iloc[-1]

                        res = all([first_res,second_res,third_res,fourth_res])
                        if res:
                            print("\n"+sy + " is a good trade ++++++++++++++++++++")
                            # send_to_telegram(f'{sy}')
                        else:
                            print(f"skipping {sy}")
                            # print(".",end="")

                            pass
                        break
                    except Exception as e:
                        # print(e)
                        break

                
def ema_cross_strategy(sy):
    try:
      timeFrames = ['1m','5m','15m','4h','8h']
      for tf in timeFrames:
        kline = get_kline(sy,timeframe=tf)
        sma = calculate_ema_cross(kline)
        if sma:
            print(f"{sy} is a good trade ++++++++++++++++++++ on {tf}")
        else:
            # print(f"skip {sy} on {tf}")
            # print('\'')
            pass
    except ConnectionError :
        print("connection error")
    except KeyboardInterrupt as e:
        print(e)
            
def spans_cross(sy):

      timeFrames = ['1m','5m','15m','30m','1h','2h','4h','6h','8h','12h']
      for tf in timeFrames:
        kline = get_kline(sy,timeframe=tf)
        sma = calculate_ichi(kline)
        previous_conversion_line = sma['conversion_line'].iloc[-2]
        current_conversion_line = sma['conversion_line'].iloc[-1]
        previous_basis_line = sma['basis_line'].iloc[-2]
        current_basis_line = sma['basis_line'].iloc[-1]
        condition = (previous_conversion_line < previous_basis_line) and (current_conversion_line > current_basis_line)
        if condition:
            print(f"{sy} is a good trade ++++++++++++++++++++ on {tf}")
        else:
            print(f"skip {sy} on {tf}")
           
def rsi(sy):

      timeFrames = ['5m','3m','15m','1h','2h','4h']
      for tf in timeFrames:
        kline = get_kline(sy,timeframe=tf)
        sma = calculate_ichi(kline)
        previous_rsi= sma['rsi'].iloc[-2]
        current_rsi = sma['rsi'].iloc[-1]

        condition = (previous_rsi < 30) #and (current_rsi > 30)
        if condition:
            print(f"{sy} is a good trade ++++++++++++++++++++ on {tf}")
        else:
            # print(f"skip {sy} on {tf}")
            pass

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
    data['ema9'] = ta.ema(close=data['close'],length=9)
    data['ema26'] = ta.ema(close=data['close'],length=26)
    data['rsi'] = ta.rsi(close=data['close'],length=14)
    return data


def calculate_ema_cross(data):
    try:
        try:
            data['close'] = data['close'].astype(float) 
        except ValueError:
            pass # skip row
        data['ema50'] = ta.ema(close=data['close'],length=50)
        data['ema200'] = ta.ema(close=data['close'],length=200)
        before_50 = data['ema50'].iloc[-2]
        before_260 = data['ema200'].iloc[-2]
        now_200 = data['ema200'].iloc[-1]
        now_50 = data['ema50'].iloc[-1]

        res = (before_50 < before_260) and (now_50 > now_200)
        # res = now_9 > now_26
        return res
    except Exception as e:
        # print(e)
        pass

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
  
  
  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = [executor.submit(ema_cross_strategy, sy) for sy in tickers]
  
  for f in concurrent.futures.as_completed(results):
    f.result()
      
if __name__ == '__main__':
    while 1:
        try:
            tickers = get_symbols()
            main(tickers)
            print("sleeping a while... ")
            time.sleep(10)
        except KeyboardInterrupt as e:
            print("ok .. ending")
        except Exception as f:
            # print(f)
            pass
        












