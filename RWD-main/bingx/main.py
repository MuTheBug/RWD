from indicators import *
from get_klines import *

def main(symbol):
    timeframes = ['15m','30m','1h','2h','4h']
    for t in timeframes:
        df = get_kline(symbol,t)
        mac = macd_signal(df)
        ma200 = sma_200(df)
        if mac and ma200:
            rsi_direction = rsi_sloping_up(df)
            print(f"{symbol} on {t}  is rsi sloping up?:{rsi_direction} +++++++++++++++++++++++++++++++++++++++++++++++++++")
        else:
            print(f'skip {symbol} on {t}')









tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=main)