from get_klines import  pd,requests
def get_symbols():
        try:
            url= "https://open-api.bingx.com/openApi/swap/v2/quote/ticker"

            tickers = requests.get(url=url).json()['data']
            data = pd.DataFrame(tickers)['symbol']
            return data.to_list()
        
        except Exception as e:

            print("error in getting symbols")
            pass


