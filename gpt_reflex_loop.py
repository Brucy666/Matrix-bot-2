# reflex_agent.py
# GPT Reflex Agent for Recursive AI Oversight

import os
import json
import time
import requests
from openai import OpenAI
from datetime import datetime

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_OVERSEER_WEBHOOK = os.getenv("DISCORD_OVERSEER_WEBHOOK")
client = OpenAI(api_key=OPENAI_API_KEY)

REFLEX_LOG = "logs/reflex_memory.json"

def read_last_reflex():
    try:
        with open(REFLEX_LOG, "r") as f:
            return json.load(f)
    except:
        return {}

def save_reflex_memory(data):
    try:
        with open(REFLEX_LOG, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[✘] Failed to save reflex memory: {e}")

def build_reflex_prompt(previous=None):
    base = "You are Reflex, a strategic AI overseeing a sniper trading system. Your job is to summarize recent performance, evaluate risk, macro alignment, confidence, and recommend adjustments.\n\n"

    if previous:
        base += f"Last Reflex Report:\n{json.dumps(previous, indent=2)}\n\n"
        base += "Reflect on that and generate an updated assessment."

    return base

def analyze_and_respond():
    previous = read_last_reflex()
    prompt = build_reflex_prompt(previous)

    print("[Reflex] Thinking...")
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Reflex AI. Analyze system performance and recommend adjustments."},
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message.content.strip()
        return result
    except Exception as e:
        return f"[Reflex Error] {e}"

def parse_json_summary(text):
    try:
        start = text.find("{")
        return json.loads(text[start:])
    except Exception as e:
        print(f"[✘] Reflex Parse Error: {e}")
        return {}

def send_to_discord(summary_text):
    payload = {
        "username": "GPT Reflex",
        "content": f"🧠 **Reflex Report**\n```json\n{summary_text}\n```"
    }
    try:
        res = requests.post(DISCORD_OVERSEER_WEBHOOK, json=payload)
        if res.status_code in [200, 204]:
            print("[✓] Reflex report sent to Discord.")
        else:
            print(f"[!] Discord Error {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[!] Discord post failed: {e}")

# Run Reflex Loop
if __name__ == "__main__":
    print("🔁 Reflex loop running...")
    result = analyze_and_respond()
    print("[✓] Reflex response received.")

    memory = parse_json_summary(result)
    if memory:
        save_reflex_memory(memory)
    send_to_discord(result)
