# discord_alert.py
import requests
import os
from datetime import datetime

DISCORD_WEBHOOK = os.getenv("TEST_DISCORD_WEBHOOK")

def send_discord_alert(trade_data):
    if not DISCORD_WEBHOOK:
        print("[!] No webhook set.")
        return

    symbol = trade_data.get("symbol", "N/A")
    status = trade_data.get("rsi_status", "None")
    price = trade_data.get("entry_price", 0)
    confidence = trade_data.get("confidence", 0)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    content = f"🧪 Test Sniper Signal\n**{symbol}** at `{price}`\nRSI Signal: `{status}`\nConfidence: `{confidence}`\n`{timestamp}`"

    try:
        res = requests.post(DISCORD_WEBHOOK, json={"content": content})
        if res.status_code in [200, 204]:
            print("[✓] Test alert sent to Discord.")
        else:
            print(f"[!] Discord error: {res.status_code}, {res.text}")
    except Exception as e:
        print(f"[!] Discord exception: {e}")
