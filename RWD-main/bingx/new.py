from indicators import *
from get_klines import *

pd.options.mode.chained_assignment = None # default='warn'







def main(symbol):
    
    timeframes = ['15m','30m','2h','1h','4h','1d']
    for t in timeframes:
        data = get_kline(symbol, t)
        up = ema_cross_up(data)
        down = ema_cross_down(data)
        if up:
            send_to_telegram(f"Long {symbol} on {t} ++++")
            print(f"Long {symbol} on {t} +++++++++++++++++++++++++++++++++++++++++++++")

        elif down:
            send_to_telegram(f"Short {symbol} on {t} ++++")
            print(f"Short {symbol} on {t} +++++++++++++++++++++++++++++++++++++++++++++")

                        
        else:
            print(f'skip {symbol} on {t}')



tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=main)