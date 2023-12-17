from indicators import *


def main(symbol):

    daily = get_kline(symbol,'1d')
    four_hours = get_kline(symbol,'4h')

    up = macd_signal_up(four_hours)
    up1 = macd_signal_down_crossing(daily)
    down = macd_signal_down(four_hours)
    down1 = macd_signal_up_crossing(daily)
    if up and up1:
        send_to_telegram(f"LONG {symbol} ++++")
        print(f"LONG {symbol}  +++++++++++++++++++++++++++++++++++++++++++++")

            
    elif down and down1:
        send_to_telegram(f"SHORT {symbol} ++++")
        print(f"SHORT {symbol}  +++++++++++++++++++++++++++++++++++++++++++++")

                        
    else:
        print(f'skip {symbol} ')


tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=main)