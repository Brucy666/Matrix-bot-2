# discord_alert.py (rewritten for RSI-V + Echo-V multi-timeframe tracking)

import requests
from datetime import datetime
import os

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")


def format_discord_alert(trade_data):
    symbol = trade_data.get("symbol", "N/A")
    exchange = trade_data.get("exchange", "Unknown")
    score = trade_data.get("score", 0)
    spoof = trade_data.get("spoof_ratio", 0)
    bias = trade_data.get("bias", "Unknown").capitalize()
    trap_type = trade_data.get("trap_type", "Unclassified")
    confidence = trade_data.get("confidence", 0)
    macro_bias = trade_data.get("macro_biases", ["Unclassified"])[0]
    macro_splits = trade_data.get("macro_vsplit", ["None"])
    echo_v = trade_data.get("echo_v", {})
    rsi_v = trade_data.get("rsi_vsplit", {})
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    emoji = "📉" if bias == "Below" else "📈"
    spoof_emoji = "🟢" if spoof < 0.3 else "🟠" if spoof < 0.6 else "🔴"
    confidence_emoji = "🧠" if confidence >= 8 else "⚠️" if confidence >= 5 else "💤"

    echo_lines = [f"• {tf}: {val}" for tf, val in echo_v.items()] or ["None"]
    rsi_v_lines = [f"• {tf}: {val}" for tf, val in rsi_v.items()] or ["None"]
    macro_v_lines = [f"• {entry}" for entry in macro_splits] or ["None"]

    return {
        "username": "QuickStrike Bot",
        "embeds": [
            {
                "title": f"🎯 Sniper Signal — {exchange}",
                "color": 0x00ffae if bias == "Above" else 0xff5555,
                "fields": [
                    {"name": "Symbol", "value": f"`{symbol}`", "inline": True},
                    {"name": "Bias", "value": f"{emoji} `{bias}`", "inline": True},
                    {"name": "Spoof Ratio", "value": f"{spoof_emoji} `{spoof:.3f}`", "inline": True},
                    {"name": "Trap Type", "value": f"`{trap_type}`", "inline": True},
                    {"name": "Confidence", "value": f"{confidence_emoji} `{confidence}/10`", "inline": True},
                    {"name": "Macro Bias", "value": f"`{macro_bias}`", "inline": True},
                    {"name": "Echo V Stack", "value": "```\n" + "\n".join(echo_lines) + "```", "inline": False},
                    {"name": "RSI-V Stack", "value": "```\n" + "\n".join(rsi_v_lines) + "```", "inline": False},
                    {"name": "Macro V-Splits", "value": "```\n" + "\n".join(macro_v_lines) + "```", "inline": False},
                    {"name": "Timestamp", "value": f"`{timestamp}`", "inline": False},
                ],
                "footer": {"text": "QuickStrike Sniper Feed"}
            }
        ]
    }


def send_discord_alert(trade_data):
    payload = format_discord_alert(trade_data)
    headers = {"Content-Type": "application/json"}

    try:
        res = requests.post(DISCORD_WEBHOOK, json=payload, headers=headers)
        if res.status_code in [200, 204]:
            print("[✓] Discord alert sent.")
        else:
            print(f"[!] Discord alert failed: {res.status_code}, {res.text}")
    except Exception as e:
        print(f"[!] Discord alert error: {e}")
