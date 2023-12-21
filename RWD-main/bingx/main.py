from get_sympols import get_symbols
from imports import *
from indicators import *
        
def long_on_one_day(symbol,four_hours,daily):
    x = is_macd__going_up_on_daily(daily)
    x1 = just_crossed_up(four_hours)
    condition = x and x1
    if condition:
        print(f"go long on {symbol} on one day")
        send_to_telegram(f"go long on {symbol} on one day")
        return True
    else:
        return False
    
 
def short_on_one_day(symbol,four_hours,daily):
    y = is_macd__going_down_on_daily(daily)
    y1 = just_crossed_down(four_hours)
    condition = y and y1
    if condition:
        print(f"go short on {symbol} on one day")
        send_to_telegram(f"go short on {symbol} on one day")
        return True
    else:
        return False
  

        
def main(symbol):
    daily = get_kline(symbol,'1d')
    four_hours = get_kline(symbol,'4h')

    one = long_on_one_day(symbol,four_hours,daily)
    three = short_on_one_day(symbol,four_hours,daily)

    if not one and  not three:
        print(f'skip {symbol}')
    # sleep(1)

        	
        
        
# main('BTC-USDT')           
# print(get_kline('BTC-USDT','1d'))


tickers = get_symbols()  

loop.call_me(tickers=tickers, name_of_method=main)