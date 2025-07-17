from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
btc = cg.get_price(ids='bitcoin', vs_currencies='usd', include_market_cap='true', include_24hr_vol='true')

print("✅ BTC Market Data:", btc['bitcoin'])