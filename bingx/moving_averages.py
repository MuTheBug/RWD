from get_klines import get_kline
import send_to_telegram
import loop
import pandas_ta as ta
import get_sympols

def get_signal(data):
    data['sma100'] = ta.sma(close=data['close'],length=100)
    data['sma50'] = ta.sma(close=data['close'],length=50)
    data['sma20'] = ta.sma(close=data['close'],length=20)
    data['res'] = (data['sma100']<data['sma50']) &(data['sma50']<data['sma20']) & (data['sma20']>data['close'])
    # print(data['res'].iloc[-1])
    return data['res'].iloc[-1]
def moving_averages(symbol):
    d1 = get_kline(symbol,'1d')
    h4 = get_kline(symbol,'4h')
    h1 = get_kline(symbol,'1h')
    m15 = get_kline(symbol,'15m')
    d1_res = get_signal(data=d1)
    h4_res = get_signal(data=h4)
    h1_res = get_signal(data=h1)
    m15_res = get_signal(data=m15)
    res = [d1_res]
    if all(res):
        print(f"{symbol} is a great option +++++++++++++++++++++++++++++++++++++")
    else:
        print(f"skip {symbol}")
    

    # print(arr)
THRESH_PERCENT = 15 # Threshold percentage 

def find_zigzag(symbol):
    arr = get_kline(symbol)['close'].tolist()

    n = len(arr)
    
    # Find relative highs and lows
    highs = [0]
    lows = []
    for i in range(1, n):
        pct_diff = abs(arr[i] - arr[i-1]) / arr[i-1] * 100
        if pct_diff > THRESH_PERCENT:
            if arr[i] > arr[i-1]:
                highs.append(i) 
            else:
                lows.append(i)
    
    # Check if alternating highs and lows         
    if len(highs) < 2 or len(lows) < 1: 
        return False    
    for i in range(1, len(highs)):
        if highs[i] < highs[i-1] or highs[i] < lows[i-1]:
            print(f"skip {symbol}")
            return False
            
    print(f"{symbol} is a great fuck ++++++++++++++++")
    return True

            
    

# arr = np.random.randint(0, 100, size=100)
# print(arr)
# if find_zigzag(arr):
#     print("Zigzag pattern found!")
# else:
#     print("No zigzag pattern.")


tickers = get_sympols.get_symbols()

loop.call_me(tickers=tickers, name_of_method=find_zigzag)


# get_kline() returns a pd series with columns open, close, high, low, volume, and time
# I want a python code that calculate the renko briks and print("good asset") if a new renko brick with
# different color is formed, otherwise it should print("skip")
