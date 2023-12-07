from indicators import *
from get_klines import *

def main(symbol):
    timeframes = ['15m','30m','1h','2h','4h']
    timeframes = ['15m','30m','2h','1h','4h','1d']
    for t in timeframes:
        above_sma200 = get_kline(symbol,'1d')
        above_200 = above_sma_200(above_sma200)
        df = get_kline(symbol,t)
        r = rsi_sloping_up(df)
        # ma50 = above_sma_50(df)
        macds = macd_signal(df)
        if above_200:
            if r:
                send_to_telegram(f"LONG {symbol} on {t}  ")

                            
                print(f'skip {symbol} on {t}++')

        else:
                print(f'skip {symbol} has no trend')









tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=main)