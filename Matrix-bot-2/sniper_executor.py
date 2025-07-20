import os
import json
import requests
from datetime import datetime

SCORE_THRESHOLD = 9.0
LOG_DIR = "logs/trades"
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_TRADE_WEBHOOK")

def simulate_trade(token, price, score, reason):
    print(f"📍 Simulated Trade Executed for {token}")
    return {
        "token": token,
        "entry_price": price,
        "score": score,
        "bias": reason.split()[1],
        "spoof_ratio": reason.split()[-1],
        "executed_at": datetime.utcnow().isoformat()
    }

def post_to_discord(entry):
    if not DISCORD_WEBHOOK_URL:
        print("⚠️ No webhook set.")
        return
    message = {
        "content": f"🎯 **Sniper Trade Executed**\nToken: `{entry['token']}`\nScore: `{entry['score']}` | Bias: `{entry['bias']}` | Spoof: `{entry['spoof_ratio']}`\nTime: `{entry['executed_at']}`"
    }
    requests.post(DISCORD_WEBHOOK_URL, json=message)

def log_trade(entry):
    os.makedirs(LOG_DIR, exist_ok=True)
    filename = f"{entry['token']}_{entry['executed_at'].replace(':','-')}.json"
    with open(os.path.join(LOG_DIR, filename), "w") as f:
        json.dump(entry, f, indent=2)
    print(f"✅ Trade Logged: {filename}")
    post_to_discord(entry)

def evaluate_and_execute(token_data):
    if token_data["score"] >= SCORE_THRESHOLD:
        result = simulate_trade(
            token=token_data["symbol"],
            price=token_data["price"],
            score=token_data["score"],
            reason=f"VWAP: {token_data['bias']} + Spoof: {token_data['spoof_ratio']}"
        )
        log_trade(result)
    else:
        print(f"⏭ Skipped {token_data['symbol']} — Score too low")
