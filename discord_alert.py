# discord_alert.py
# Enhanced Discord alert sender with V-Split summary injection

import requests
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Utility to post alert to Discord with rich embed
def send_discord_alert(trap):
    if not WEBHOOK_URL:
        print("[x] Discord webhook URL not configured.")
        return

    symbol = trap.get("symbol", "?")
    exchange = trap.get("exchange", "?")
    price = trap.get("entry_price", "?")
    rsi = trap.get("rsi", "?")
    score = trap.get("score", 0)
    confidence = trap.get("confidence", 0)
    bias = trap.get("bias", "?")
    trap_type = trap.get("trap_type", "?")
    reasons = trap.get("reasons", [])
    spoof = trap.get("spoof_ratio", 0)
    rsi_status = trap.get("rsi_status", "None")
    vsplit_type = trap.get("vsplit_type", "None")
    vsplit_strength = trap.get("vsplit_strength", 0.0)
    vsplit_score = trap.get("vsplit_score", "None")

    summary = f"**🔥 Sniper Entry [{symbol}]**\n"
    summary += f"Exchange: {exchange} | Bias: **{bias}**\n"
    summary += f"Trap Type: `{trap_type}`\n"
    summary += f"Score: `{score}` | Confidence: `{confidence}`\n"
    summary += f"VWAP Score: `{vsplit_score}`\n"
    summary += f"RSI Status: `{rsi_status}`\n"
    if vsplit_type != "None":
        summary += f"V-Split Type: **{vsplit_type}** | Δ: `{vsplit_strength}`\n"
    summary += f"RSI: `{rsi}` | Price: `{price}`\n"
    summary += f"Reasons: {', '.join(reasons)}"

    payload = {"content": summary}

    try:
        res = requests.post(WEBHOOK_URL, json=payload, timeout=5)
        if res.status_code != 204:
            print(f"[x] Discord webhook error: {res.status_code}")
    except Exception as e:
        print(f"[x] Discord alert exception: {e}")
