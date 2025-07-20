# api_status.py

import requests
import time

def check_status(url, label):
    try:
        r = requests.get(url, timeout=5)
        status = "✅ OK" if r.status_code == 200 else f"⚠️ {r.status_code}"
    except Exception as e:
        status = f"❌ Error: {str(e)}"
    return {"name": label, "value": status, "inline": True}

def get_all_status():
    return [
        check_status("https://api.kucoin.com/api/v1/status", "KuCoin API"),
        check_status("https://discord.com/api/v10", "Discord API"),
        check_status("https://api.coingecko.com/api/v3/ping", "CoinGecko API")
    ]

def display_to_discord():
    from discord_alert import send_discord_alert
    status_fields = get_all_status()
    send_discord_alert("🔍 API Health Report", {s['name']: s['value'] for s in status_fields})

if __name__ == "__main__":
    display_to_discord()
