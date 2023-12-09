from renko import Renko
from imports import *

def cal_renk(df):
    df['atr'] = ta.atr(high=df['high'],low=df['low'],close=df['close'],length=14)
    r = Renko(df.atr.iloc[-1]/2,df['close'])
    r.create_renko()
    renks = pd.DataFrame(r.bricks)
    return renks

def sma10(df):
    df['sma10'] = ta.sma(df.close,length=10)
    return df


def main(symbol):
    
    timeframes = ['5m','15m','30m','2h','1h','4h','1d']
    for t in timeframes:
        df = get_kline(symbol, t)
        s = sma10(df)
        r = cal_renk(df)
        down=  s['sma10'].iloc[-1] > r.close.iloc[-1] and s['sma10'].iloc[-2] < r.close.iloc[-2] and r.type =='down'
        up=  s['sma10'].iloc[-1] < r.close.iloc[-1] and s['sma10'].iloc[-2] > r.close.iloc[-2] and r.type =='up'
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