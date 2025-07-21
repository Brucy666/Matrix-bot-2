# gpt_reflex_loop.py
# GPT Reflex Loop: Reads sniper logs + prior GPT logic → reflects → adjusts → rewrites itself

import os
import json
import requests
from datetime import datetime
from openai import OpenAI

# ENV
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_OVERSEER_WEBHOOK = os.getenv("DISCORD_OVERSEER_WEBHOOK")
JOURNAL_FILE = "logs/trap_journal.csv"
ACTIVE_TRADES = "logs/active_trades.json"
CHAIN_LOG = "logs/gpt_overseer_chain.json"

client = OpenAI(api_key=OPENAI_API_KEY)

# Load prior GPT reflection
def load_prior_chain():
    try:
        with open(CHAIN_LOG, "r") as f:
            return json.load(f)
    except:
        return {
            "timestamp": "none",
            "learned": "none",
            "adjustment": {},
            "commitment": "none",
            "next_instruction": "none"
        }

# Build prompt to reflect
def build_reflex_prompt():
    journal = open(JOURNAL_FILE, "r").read()[-5000:] if os.path.exists(JOURNAL_FILE) else "(No journal)"
    trades = open(ACTIVE_TRADES, "r").read() if os.path.exists(ACTIVE_TRADES) else "(No trades)"
    memory = load_prior_chain()

    return f"""
You are GPT Reflex, a strategist who remembers past reasoning.

[PAST SELF]
Last insight: {memory.get("learned")}
Adjustments: {json.dumps(memory.get("adjustment", {}))}
Commitment: {memory.get("commitment")}

[JOURNAL]
{journal}

[ACTIVE TRADES]
{trades}

Now:
1. Reflect on recent sniper behavior
2. Identify what worked or failed
3. Suggest scoring or strategy adjustments
4. Recommit your sniper intent
5. Output this in structured JSON.
"""

# Call GPT
def run_reflex_loop():
    print("[Reflex] Thinking...")
    prompt = build_reflex_prompt()

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're a sniper AI evolving your strategy via self-reflection."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[GPT ERROR] {e}")
        return None

# Parse JSON from GPT
def parse_and_store_response(text):
    try:
        block = json.loads(text)
        with open(CHAIN_LOG, "w") as f:
            json.dump(block, f, indent=4)
        return block
    except Exception as e:
        print(f"[Reflex Parse Error] {e}")
        return None

# Discord log
def post_to_discord(reflection):
    content = f"""🧠 **GPT Reflex Loop Activated**

**Observation:** {reflection.get('learned')}
**Adjustment:** `{json.dumps(reflection.get('adjustment'))}`
**Commitment:** {reflection.get('commitment')}
**Next Step:** {reflection.get('next_instruction')}
⏱ {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
"""
    try:
        requests.post(DISCORD_OVERSEER_WEBHOOK, json={"content": content})
    except Exception as e:
        print(f"[Discord Error] {e}")

# Main loop
if __name__ == "__main__":
    print("[✓] Reflex loop running...")
    raw_response = run_reflex_loop()
    if raw_response:
        print("[✓] Reflex response received.")
        reflection = parse_and_store_response(raw_response)
        if reflection:
            post_to_discord(reflection)
