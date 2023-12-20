from get_sympols import get_symbols
from imports import *
from indicators import *
        
def long_on_one_day(symbol,four_hours,daily):
    x = just_crossed_up(daily)
    x1= already_down_going_up(four_hours)
    condition = x and x1
    if condition:
        print(f"go long on {symbol} on one day")
        send_to_telegram(f"go long on {symbol} on one day")
        return True
    else:
        return False
    
 
def short_on_one_day(symbol,four_hours,daily):
    y = just_crossed_down(daily)
    y1 = already_up_going_down(four_hours)
    condition = y and y1
    if condition:
        print(f"go short on {symbol} on one day")
        send_to_telegram(f"go short on {symbol} on one day")
        return True
    else:
        return False
  
def ema_with_mac(symbol, daily, four_hours):
    ema_cross = ema_cross_up(daily)
    four = already_down_going_up(four_hours)
    if  ema_cross:
        print(f"go long on {symbol} on one day EMA CROSS")
        send_to_telegram(f"go long on {symbol} on one day EMA CROSS")
        return True
    else:
        return False
        
def main(symbol):
    daily = get_kline(symbol,'1d')
    four_hours = get_kline(symbol,'4h')

    one = long_on_one_day(symbol,four_hours,daily)
    three = short_on_one_day(symbol,four_hours,daily)
    four = ema_with_mac(symbol,daily,four_hours)

    if not one and  not three and not four:
        print(f'skip {symbol}')
    # sleep(1)

        	
        
        
# main('BTC-USDT')           
# print(get_kline('BTC-USDT','1d'))


tickers = get_symbols()  

loop.call_me(tickers=tickers, name_of_method=main)