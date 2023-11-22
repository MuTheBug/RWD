from get_klines import get_kline
import send_to_telegram
import loop
import pandas_ta as ta
import get_sympols

def find_ascend(symbol):
    arr = get_kline(symbol,timeframe='15m')['close'].tolist()
    arr = arr[-10:-1]
    first_number = arr[0]
    last_number = arr[-1]
    msg = f"Go "
    percent = 0
    if first_number > last_number:
        percent = (first_number- last_number) / ((first_number + last_number) /2) * 100
        msg+=f"long on {symbol}"
    else:        
        percent = (last_number- first_number) / ((first_number + last_number) /2) * 100
        msg+=f"short on {symbol}"
    if percent > 5:
        print(msg + f" XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX with {percent}")
        send_to_telegram.send_to_telegram(msg)
    else:
        print(f'skip {symbol} of percent {percent}')

        

            
    




tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=find_ascend)


# get_kline() returns a pd series with columns open, close, high, low, volume, and time
# I want a python code that calculate the renko briks and print("good asset") if a new renko brick with
# different color is formed, otherwise it should print("skip")
