

from imports import *
from get_klines import np,pd

pd.set_option('max_columns',None)

def chech_trend(symbol):
        hour= ichi(get_kline(symbol,'1h'))
        if hour:
            print(f'{symbol} is trending on 1 hour')
            return True
        two_hour= ichi(get_kline(symbol,'2h'))
        if two_hour:
            return True
        four_hour= ichi(get_kline(symbol,'4h'))
        if four_hour:
            return True
        return False

def ichi(df):
	ichi = ta.ichimoku(high=df['high'],low=df['low'],close=df['close'])
	#print(ichi[0].tail(30))
	df['cloud_a'] = ichi[0]['ISA_9']

	df['cloud_b'] = ichi[0]['ISB_26']

	df['conversion_line'] = ichi[0]['ITS_9']

	df['base_line'] = ichi[0]['IKS_26']

	df['lagging_span'] = ichi[0]['ICS_26']

	condition= df['cloud_b'].iloc[-1]<df['cloud_a'].iloc[-1]<df['base_line'].iloc[-1]<df['conversion_line'].iloc[-1]<df['close'].iloc[-1]
	return condition
	
def sto(df):
	st= ta.stoch(high=df['high'],low=df['low'],close=df['close'])
	return st['STOCHd_14_3_3'].iloc[-1]<20 or st['STOCHd_14_3_3'].iloc[-1] > 80
def deep_dip_strategy(symbol):
    """
    Main strategy function
    """
    timeframes = ['3m','5m','15m']

    for timeframe in timeframes:
        
        
        uptrend = chech_trend(symbol)
        if not uptrend:
            print(f'{symbol} is not trending')
            return False
        df = get_kline(symbol, timeframe)
        if sto(df):
            print(f"{symbol} at {timeframe}, hurp!")
            send_to_telegram(f'{symbol} at{timeframe}')
        else:
            print(f"skipt {symbol}")


#deep_dip_strategy('BTC-USDT')
tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=deep_dip_strategy)
	
	
