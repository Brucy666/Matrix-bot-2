# gpt_reflex.py
# Reflex loop for GPT-based self-monitoring agent

import os
import json
import time
import requests
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_OVERSEER_WEBHOOK = os.getenv("DISCORD_OVERSEER_WEBHOOK")

client = OpenAI(api_key=OPENAI_API_KEY)

def build_prompt():
    return (
        "You are the Reflex Commander of a live sniper AI system.\n"
        "Only reply with a valid JSON object using these keys:\n"
        "- summary: A 1-sentence high-level explanation\n"
        "- confidence: A numeric value from 0 to 10\n"
        "- macro_bias: One of 'Bullish', 'Bearish', or 'Neutral'\n"
        "- orders: A list of short bullet points (actions or alerts)"
    )

def run_reflex():
    prompt = build_prompt()
    print("[Reflex] Thinking...")

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": "Evaluate the sniper logs and macro data from today."
                }
            ]
        )

        raw = response.choices[0].message.content.strip()
        print("[Reflex] Raw Response:\n", raw)

        result = json.loads(raw)
        return result
    except Exception as e:
        print("[Reflex ERROR]", e)
        return None

def send_to_discord(report):
    message = f"**🤖 Reflex Report**\n\n"
    message += f"**Summary:** {report['summary']}\n"
    message += f"**Confidence:** `{report['confidence']}/10`\n"
    message += f"**Macro Bias:** `{report['macro_bias']}`\n"
    message += "**Orders:**\n" + "\n".join([f"- {o}" for o in report["orders"]])

    payload = {
        "username": "GPT Reflex",
        "content": message
    }

    try:
        requests.post(DISCORD_OVERSEER_WEBHOOK, json=payload)
        print("[✓] Reflex report sent to Discord.")
    except Exception as e:
        print("[!] Discord post failed:", e)

if __name__ == "__main__":
    print("[✓] Reflex loop running...")
    result = run_reflex()
    if result:
        send_to_discord(result)
