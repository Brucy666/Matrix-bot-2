import os
import json
import requests
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DISCORD_WEBHOOK = os.getenv("DISCORD_OVERSEER_WEBHOOK")
MEMORY_FILE = "logs/reflex_memory.json"

MAX_DISCORD_LENGTH = 1900  # Discord safe limit per message

print("🧠 Reflex loop running...")

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def call_reflex(prompt):
    print("[Reflex] Thinking...")
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Reflex, the autonomous GPT agent who loops thoughts from sniper reports and macro behavior into future instructions."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("[!] Reflex Error:", e)
        return None

def chunk_message(msg, limit=MAX_DISCORD_LENGTH):
    lines = msg.split('\n')
    chunks = []
    current = ""
    for line in lines:
        if len(current) + len(line) + 1 < limit:
            current += line + "\n"
        else:
            chunks.append(current.strip())
            current = line + "\n"
    if current:
        chunks.append(current.strip())
    return chunks

def send_to_discord_blocks(text):
    chunks = chunk_message(text)
    for part in chunks:
        payload = {
            "username": "GPT Reflex",
            "content": f"**🌀 Reflex Report**\n\n{part}"
        }
        try:
            res = requests.post(DISCORD_WEBHOOK, json=payload)
            if res.status_code not in [200, 204]:
                print(f"[!] Discord send error {res.status_code}: {res.text}")
        except Exception as e:
            print(f"[!] Failed to send Reflex message: {e}")

if __name__ == "__main__":
    memory = load_memory()
    last_summary = memory.get("last_report", "No prior report")

    result = call_reflex(last_summary)
    if not result or len(result.strip()) < 10:
        print("[✘] Reflex output was empty.")
    else:
        memory["last_report"] = result
        save_memory(memory)
        send_to_discord_blocks(result)
        print("✅ Reflex loop complete.")
