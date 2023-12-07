from indicators import *
from get_klines import *
def identify_primary_trend(df):
    # Calculate Moving Averages (MAs)
    MA20 = df['close'].rolling(window=20).mean()
    MA50 = df['close'].rolling(window=50).mean()
    MA200 = df['close'].rolling(window=200).mean()

    # Determine primary trend based on MAs convergence/divergence
    if MA20.iloc[-1] > MA50.iloc[-1] > MA200.iloc[-1]:
        trend = 'Uptrend'
    elif MA20.iloc[-1] < MA50.iloc[-1] < MA200.iloc[-1]:
        trend = 'Downtrend'
    else:
        trend = 'Sideways'
    return trend

def identify_swing_opportunities(df, symbol):
    # Calculate support and resistance levels
    support_levels = df['close'].rolling(window=20).min()
    resistance_levels = df['close'].rolling(window=20).max()
    # print(support_levels)
    # print(resistance_levels)
    ds = get_kline(symbol,'1d')
    trend = identify_primary_trend(ds)

    if df['close'].iloc[-1] > resistance_levels.iloc[-1] and trend == 'Downtrend':
        send_to_telegram(f'Uptrend Breakout: {symbol}')
        print(f'Uptrend Breakout: {symbol}')
    elif df['close'].iloc[-1] < support_levels.iloc[-1] and trend == 'Uptrend':
        send_to_telegram(f'Downtrend Breakout: {symbol}')
        print(f'Downtrend Breakout: {symbol}')
    else:
        print(f'skip {symbol}')
    


def main(symbol):
    # Get historical data for the specified symbol
    df = get_kline(symbol)

 
    identify_swing_opportunities(df,symbol)



tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=main)
