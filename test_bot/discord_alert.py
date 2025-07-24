# test_bot/discord_alert.py

import os
import requests
import json

# Load webhook URL from Railway environment
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def send_discord_alert(data: dict):
    if not DISCORD_WEBHOOK:
        print("[!] No webhook set. Skipping Discord alert.")
        return

    try:
        # Format alert content
        message = {
            "username": "Echo V Test Bot",
            "content": "📡 **Echo V Alert**",
            "embeds": [
                {
                    "title": f"📈 {data.get('symbol', 'Unknown')} – {data.get('exchange', 'Test')}",
                    "color": 3447003,  # Blue
                    "fields": [
                        {"name": "Entry Price", "value": str(data.get("entry_price", "N/A")), "inline": True},
                        {"name": "VWAP", "value": str(data.get("vwap", "N/A")), "inline": True},
                        {"name": "RSI", "value": str(round(data.get("rsi", 0), 2)), "inline": True},
                        {"name": "Spoof Ratio", "value": str(data.get("spoof_ratio", "N/A")), "inline": True},
                        {"name": "Echo V Signal", "value": data.get("rsi_status", "None"), "inline": True},
                        {"name": "Score", "value": str(data.get("score", "0.0")), "inline": True},
                        {"name": "Confidence", "value": str(data.get("confidence", "0.0")), "inline": True},
                        {"name": "Reasons", "value": "\n".join(data.get("reasons", [])) or "None", "inline": False}
                    ],
                    "footer": {
                        "text": f"⏱ {data.get('timestamp', '')}"
                    }
                }
            ]
        }

        # Send alert
        response = requests.post(DISCORD_WEBHOOK, json=message)
        if response.status_code != 204:
            print(f"[!] Discord webhook error: {response.status_code} - {response.text}")
        else:
            print("[✓] Discord alert sent.")

    except Exception as e:
        print(f"[Webhook ERROR] {e}")
