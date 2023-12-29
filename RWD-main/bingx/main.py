from get_sympols import get_symbols
from imports import *
from indicators import *


def main(symbol):
    daily = get_kline(symbol, '1d')
    four_hours = get_kline(symbol, '4h')

    long = is_up_trend(daily) and going_up(four_hours)
    short = is_down_trend(daily) and going_down(four_hours)
    if long:
        print(f'go long on {symbol}++++++++++++++++++++++++++++++++++++')
    elif short:
        print(f'go short on {symbol}+++++++++++++++++++++++++++++++++++')
    else:
        print(f'skip {symbol}')
    # sleep(1)


# main('BTC-USDT')
# print(get_kline('BTC-USDT','1d'))
tickers = get_symbols()

loop.call_me(tickers=tickers, name_of_method=main)
