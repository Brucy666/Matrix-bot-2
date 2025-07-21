# reflex_agent.py
# Reflex GPT Agent to analyze prior GPT messages and trigger re-prompts

import os
import json
import requests
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DISCORD_WEBHOOK = os.getenv("DISCORD_OVERSEER_WEBHOOK")
MEMORY_FILE = "logs/reflex_memory.json"

print("🧠 Reflex loop running...")

# Load last message from memory
def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# Save new message
def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Call GPT on last summary
def call_reflex(prompt):
    print("[Reflex] Thinking...")
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Reflex, the autonomous GPT agent who loops thoughts from sniper reports and scores into future logic."},
                {"role": "user", "content": prompt}
            ]
        )
        raw = response.choices[0].message.content.strip()
        print("[✓] Reflex response received.")
        return raw
    except Exception as e:
        print("[!] Reflex Error:", e)
        return None

# Format into markdown (cut to 2000 characters)
def format_discord_message(content):
    clean = content.strip()
    if len(clean) > 1900:
        clean = clean[:1900] + "\n\n⚠️ *(Truncated to fit Discord limit)*"
    return {
        "username": "GPT Reflex",
        "content": "**🌀 Reflex Report**\n\n" + clean
    }

# Main loop
if __name__ == "__main__":
    memory = load_memory()
    last_summary = memory.get("last_report", "No prior report")

    # Call GPT reflex loop
    reflex_result = call_reflex(last_summary)
    if not reflex_result:
        print("[✘] Reflex failed.")
        exit()

    # Store updated
    memory["last_report"] = reflex_result
    save_memory(memory)

    # Send to Discord
    payload = format_discord_message(reflex_result)
    try:
        res = requests.post(DISCORD_WEBHOOK, json=payload)
        if res.status_code in [200, 204]:
            print("🟢 Reflex report sent to Discord.")
        else:
            print(f"[!] Discord Error {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[!] Failed to post Reflex report: {e}")
