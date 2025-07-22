# okx_discord_feed.py

import os
import requests
from datetime import datetime

DISCORD_OKX_WEBHOOK = os.getenv("DISCORD_OKX_WEBHOOK")

def send_okx_snapshot_alert(data):
    if not DISCORD_OKX_WEBHOOK:
        print("[OKX ALERT] No webhook configured.")
        return

    message = f"""
**📡 OKX Feed Update**
`{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}`

**Price:** `${data['price']}`
**Volume:** `{data['volume']}`
**Top Bid:** `{data['top_bid']}`
**Top Ask:** `{data['top_ask']}`
"""

    payload = {
        "username": "OKX Feed Monitor",
        "content": message.strip()
    }

    try:
        res = requests.post(DISCORD_OKX_WEBHOOK, json=payload)
        if res.status_code in [200, 204]:
            print("[✓] OKX snapshot sent to Discord.")
        else:
            print(f"[!] Discord error {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[!] Failed to send OKX snapshot: {e}")
