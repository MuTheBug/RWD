import ccxt
import pandas as pd
from apis import api_key, api_secret
bingx = ccxt.bingx({
        'apiKey': api_key,
    'secret': api_secret,
})
markets = bingx.load_markets()
fund = bingx.fetch_balance(params={'standard':'usdt'})
pdf = pd.DataFrame(fund['info']['data'])
print()