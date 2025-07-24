# discord_alert.py
# Updated to support Echo V multi-timeframe signal display in Discord

import os
import requests
from datetime import datetime

def send_discord_alert(trap):
    webhook = os.getenv("DISCORD_WEBHOOK")
    if not webhook:
        print("[!] No webhook set.")
        return

    tf_echo_map = trap.get("multi_tf_echo", {})
    tf_lines = []
    for tf, signal in tf_echo_map.items():
        tf_lines.append(f"• {tf}: {signal}")
    
    tf_block = "\n".join(tf_lines) if tf_lines else "None"

    message = f"""
🛰️ **Echo V Alert**

📊 **{trap['symbol']}** – {trap['exchange']}

**Entry Price**
{trap['entry_price']}
**VWAP**
{trap['vwap']}
**RSI**
{trap['rsi']}
**Spoof Ratio**
{trap['spoof_ratio']}
**Echo V Signal**
{trap['rsi_status']}
**Score**
{trap['score']}
**Confidence**
{trap['confidence']}
**Reasons**
{', '.join(trap['reasons'])}

📡 **Multi-Timeframe Echo V**
{tf_block}

🕒 {trap['timestamp']}
"""

    payload = {
        "username": "Echo V Alert",
        "content": message
    }

    try:
        requests.post(webhook, json=payload)
    except Exception as e:
        print("[Webhook ERROR]", e)
