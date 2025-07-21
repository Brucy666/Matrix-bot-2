# gpt_overseer.py
# Overseer AI: Evaluates sniper logs, trade activity, and generates reports for Discord

import os
import requests
from datetime import datetime
from openai import OpenAI

# ───── Environment ─────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_OVERSEER_WEBHOOK = os.getenv("DISCORD_OVERSEER_WEBHOOK")
LOG_FILE = "logs/trap_journal.csv"
ACTIVE_TRADES = "logs/active_trades.json"

client = OpenAI(api_key=OPENAI_API_KEY)

# ───── Utilities ─────
def read_log_file(path, fallback_message, limit_chars=None):
    try:
        with open(path, "r") as file:
            data = file.read()
            return data[-limit_chars:] if limit_chars else data
    except FileNotFoundError:
        return fallback_message

# ───── Prompt Builder ─────
def build_overseer_prompt():
    journal_section = read_log_file(LOG_FILE, "(No trap journal found)", limit_chars=5000)
    trades_section = read_log_file(ACTIVE_TRADES, "(No active trades)")

    return f"""
You are the GPT Overseer of a sniper trading system.

Your tasks:
1. Summarize which sniper trades triggered
2. Determine if they were valid entries
3. Flag any missed exits (e.g., RSI collapse, score decay, VWAP lost)
4. Suggest improvements to scoring or logic
5. Highlight top-performing signals or exchanges

[JOURNAL]
{journal_section}

[ACTIVE TRADES]
{trades_section}

Now return a short markdown-formatted report.
"""

# ───── GPT Analysis ─────
def run_overseer_analysis():
    prompt = build_overseer_prompt()
    print("[OVERSEER] Sending prompt to GPT...")

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are the senior strategist overseeing live sniper trade execution."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[!] GPT error: {e}")
        return f"**[OVERSEER ERROR]** {e}"

# ───── Discord Report ─────
def send_to_discord(content):
    payload = {
        "username": "GPT Overseer",
        "content": content
    }

    try:
        res = requests.post(DISCORD_OVERSEER_WEBHOOK, json=payload)
        if res.status_code in [200, 204]:
            print("[✓] Overseer report sent to Discord.")
        else:
            print(f"[!] Discord error {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[!] Failed to send to Discord: {e}")

# ───── Main ─────
if __name__ == "__main__":
    print("[✓] GPT Overseer initialized.")
    summary = run_overseer_analysis()
    send_to_discord(summary)
