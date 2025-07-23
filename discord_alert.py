# discord_alert.py
import requests
from datetime import datetime
import os

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK") or "https://discord.com/api/webhooks/REPLACE_THIS"


def format_discord_alert(trade_data):
    symbol = trade_data.get("symbol", "N/A")
    exchange = trade_data.get("exchange", "Unknown")
    score = trade_data.get("score", 0)
    spoof = trade_data.get("spoof_ratio", 0)
    bias = trade_data.get("bias", "Unknown").capitalize()
    trap_type = trade_data.get("trap_type", "Unclassified")
    rsi_status = trade_data.get("rsi_status", "None")
    confidence = trade_data.get("confidence", 0)
    vsetup = trade_data.get("vsplit_score", "None")
    macro = trade_data.get("macro_biases", [])
    macro_summary = trade_data.get("macro_vsplit", [])
    echo_v = trade_data.get("echo_v_status", "None")
    echo_tf = trade_data.get("echo_v_tf_confluence", [])
    price = trade_data.get("price", "?")
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    # Emojis
    emoji = "📉" if bias == "Below" else "📈"
    spoof_emoji = "🟢" if spoof < 0.3 else "🟠" if spoof < 0.6 else "🔴"
    confidence_emoji = "🧠" if confidence >= 8 else "⚠️" if confidence >= 5 else "💤"
    rsi_emoji = {
        "RSI V-Split": "💥",
        "RSI Collapse": "🔥",
        "RSI Compression": "📡",
        "RSI Sync Up": "⬆️",
        "RSI Sync Down": "⬇️"
    }.get(rsi_status, "📊")
    v_emoji = "🔵" if "vwap" in str(vsetup).lower() else "🟣" if "split" in str(vsetup).lower() else "❌"
    echo_emoji = "✅" if echo_v != "None" else "❌"

    macro_bias_text = macro[0] if macro else "Unclassified"
    macro_bias_emoji = "🔺" if "Bull" in macro_bias_text else "🔻" if "Bear" in macro_bias_text else "➖"
    macro_v_text = "\n".join(f"• {line}" for line in macro_summary) or "None"
    echo_tf_text = "\n".join(echo_tf) if echo_tf else "None"

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
                    {"name": "RSI Signal", "value": f"{rsi_emoji} `{rsi_status}`", "inline": True},
                    {"name": "VWAP Setup", "value": f"{v_emoji} `{vsetup}`", "inline": True},
                    {"name": "Echo V", "value": f"{echo_emoji} `{echo_v}`", "inline": True},
                    {"name": "Confidence", "value": f"{confidence_emoji} `{confidence}/10`", "inline": True},
                    {"name": "Price", "value": f"`{price}`", "inline": True},
                    {"name": "Macro Bias", "value": f"{macro_bias_emoji} `{macro_bias_text}`", "inline": False},
                    {"name": "Macro V-Splits", "value": f"```\n{macro_v_text}```", "inline": False},
                    {"name": "Echo V TF Confluence", "value": f"```\n{echo_tf_text}```", "inline": False},
                    {"name": "Timestamp", "value": f"`{timestamp}`", "inline": False}
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
