from indicators import *
from get_klines import *

def main(symbol):
    timeframes = ['15m','30m','1h','2h','4h']
    timeframes = ['4h']
    for t in timeframes:
        above_sma200 = get_kline(symbol,'1d')
        df = get_kline(symbol,'4h')
        
        rs = rsi_sloping_up(df)
        ma200 = sma_200(df)
        if rs and ma200 and above_sma200:
            rsi_direction = rsi_sloping_up(df)
            send_to_telegram(f"{symbol} on {t} +++")
        else:
            print(f'skip {symbol} on {t}')









tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=main)