from get_klines import get_kline
import send_to_telegram
import loop
import pandas_ta as ta
import get_sympols

def check_signal(symbol):
    timeframes = ['1m','5m','15m','1h','4h','8h']
    for tf in timeframes:
        asset_df = get_kline(symbol=symbol,timeframe=tf)
        asset_df['RSI'] = ta.rsi(close=asset_df['HA_Close'],length=14)
        signal = "skip"
        
        ha_close = asset_df['HA_Close'].iloc[-1]
        ha_close_1 = asset_df['HA_Close'].iloc[-2]
        ha_close_2 = asset_df['HA_Close'].iloc[-3]
        ha_close_3 = asset_df['HA_Close'].iloc[-4]
        ha_close_4 = asset_df['HA_Close'].iloc[-5]
        ha_close_5 = asset_df['HA_Close'].iloc[-6]
        ha_close_6 = asset_df['HA_Close'].iloc[-7]
        
        rsi = asset_df['RSI'].iloc[-1]
        prev_rsi = asset_df['RSI'].iloc[-2]
        
        condition= ha_close_6<ha_close_5<ha_close_4 < ha_close_3< ha_close_2 < ha_close_1 and (ha_close < ha_close_1)
        if condition:
            print(f'{symbol} +++++++++++++++++++++ on {tf}')
        else:
            print(f'skip {symbol}')
# check_signal('BTC-USDT')




tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=check_signal)