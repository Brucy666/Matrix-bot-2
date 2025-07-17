import requests

CRYPTO_PANIC_KEY = "72dd1c711c36581b3addcf0b3821a35d6f06cf9b"
COINDESK_KEY = "da74be7a7b5bae106a5994c0d5cfd4ea0467b586152c4da277296fc133b866ba"

# Test CryptoPanic
panic_url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_PANIC_KEY}&kind=news"
res = requests.get(panic_url)
try:
    print("✅ CryptoPanic:", res.json()['results'][0]['title'])
except Exception as e:
    print("⚠️ CryptoPanic error:", res.json())

# Test CoinDesk
coindesk_url = f"https://production.api.coindesk.com/v2/news?apikey={COINDESK_KEY}"
res2 = requests.get(coindesk_url)
try:
    print("✅ CoinDesk:", res2.json()['data'][0]['headline'])
except Exception as e:
    print("⚠️ CoinDesk error:", res2.json())