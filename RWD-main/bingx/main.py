from indicators import *
from get_klines import *

def main(symbol):

    daily = get_kline(symbol,'1d')
    four_hours = get_kline(symbol,'4h')

    d = macd_signal(daily)
    f = macd_signal(four_hours)
    if d and not f:
    
        send_to_telegram(f"LONG {symbol} ++++")
        print(f"LONG {symbol}  +++++++++++++++++++++++++++++++++++++++++++++")

                        
    else:
        print(f'skip {symbol} ')

       








tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=main)