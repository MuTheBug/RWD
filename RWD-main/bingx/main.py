from indicators import *
from get_klines import *

def main(symbol):
    timeframes = ['15m','30m','1h','2h','4h']
    timeframes = ['4h']
    for t in timeframes:
        above_sma200 = get_kline(symbol,'1d')
        above_200 = sma_200(above_sma200)
        df = get_kline(symbol,'4h')
        
        rsi_up = rsi_sloping_up(df)
        rsi_down = rsi_sloping_down(df)
        bb_downs = bb_down(df)
        bb_upss = bb_up(df)
        ma200 = sma_200(df)
        if above_200['up']:
            if rsi_up and  bb_downs:
                send_to_telegram(f"LONG {symbol} on {t}  ")

                            
                print(f'skip {symbol} on {t}')
        if above_200['down']:
            if rsi_down and bb_upss:
                send_to_telegram(f"SHORT {symbol} on {t}")
        else:
                print(f'skip {symbol} on 1 day')









tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=main)