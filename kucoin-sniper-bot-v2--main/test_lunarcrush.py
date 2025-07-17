import requests

API_KEY = "your_lunarcrush_api_key"
res = requests.get(f"https://api.lunarcrush.com/v2?data=assets&key={API_KEY}&symbol=DOGE")
print("✅ LunarCrush:", res.json()['data'][0]['galaxy_score'])