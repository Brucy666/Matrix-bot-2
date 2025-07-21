# gpt_overseer.py
# Overseer module to let GPT analyze the system's sniper logs, scores, and trade behavior

import os
import time
import json
import requests
from datetime import datetime

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_OVERSEER_WEBHOOK = os.getenv("DISCORD_OVERSEER_WEBHOOK")

LOG_FILE = "logs/trap_journal.csv"
ACTIVE_TRADES = "logs/active_trades.json"

from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Helper: Format prompt from journal + trade states
def build_prompt():
    journal = "[JOURNAL]\n"
    try:
        with open(LOG_FILE, "r") as f:
            journal += f.read()[-5000:]  # last 5000 chars
    except:
        journal += "(No trap journal found)"

    trades = "[ACTIVE TRADES]\n"
    try:
        with open(ACTIVE_TRADES, "r") as f:
            trades += f.read()
    except:
        trades += "(No active trades)"

    prompt = f"""
You are the GPT Overseer of a sniper trading system.
Review the recent sniper traps and active trade logs.

Your tasks:
1. Summarize which sniper trades triggered
2. Determine if they were valid entries
3. Note if any exits were missed (score decay, RSI collapse, VWAP loss, etc)
4. Suggest any improvements
5. Highlight high-performing signals or exchanges

{journal}

{trades}

Now provide a clear summary in Markdown.
"""
    return prompt

# GPT call
def run_overseer_analysis():
    prompt = build_prompt()
    print("[OVERSEER] Calling GPT...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are the strategist overseeing a live sniper trading system."},
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content.strip()
        print("[OVERSEER] GPT response received.")
        return result
    except Exception as e:
        return f"[OVERSEER ERROR] {e}"

# Send to Discord
def send_to_discord(message):
    payload = {
        "username": "GPT Overseer",
        "content": message
    }
    try:
        res = requests.post(DISCORD_OVERSEER_WEBHOOK, json=payload)
        if res.status_code in [200, 204]:
            print("[✓] Overseer report sent to Discord.")
        else:
            print(f"[!] Discord error {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[!] Discord post failed: {e}")

# Main
if __name__ == "__main__":
    summary = run_overseer_analysis()
    send_to_discord(summary)
