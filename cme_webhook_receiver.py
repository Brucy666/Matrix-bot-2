# cme_webhook_receiver.py
from fastapi import FastAPI, Request
from datetime import datetime
import json
import requests

app = FastAPI()

# ✅ Hardcoded webhook (for GPT Overseer)
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1396891353367056434/90hJyCgxIWKsQN71_yCOGGPULIYOJILguZPBxORR4sH3w9vkv8D8ITEvw3IrdwCnHOyF"
LOG_FILE = "logs/cme_vsplit_alerts.txt"

@app.post("/cme")
async def receive_cme_alert(request: Request):
    try:
        body = await request.body()
        content = body.decode("utf-8").strip()

        # Timestamp
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        log_entry = f"[{timestamp}] {content}\n"

        # Save log
        try:
            with open(LOG_FILE, "a") as f:
                f.write(log_entry)
        except Exception as log_err:
            print("[CME LOG ERROR]", log_err)

        # Format message for Discord
        if content.startswith("{") or content.startswith("["):
            try:
                parsed = json.loads(content)
                pretty = json.dumps(parsed, indent=2)
                message = f"🟡 **CME JSON Alert**\n```json\n{pretty}```"
            except:
                message = f"🟡 CME Alert (raw JSON):\n```text\n{content}```"
        else:
            message = f"🟡 **CME Alert** `{content}`"

        # Send to Discord
        res = requests.post(DISCORD_WEBHOOK, json={
            "username": "CME V-Alert",
            "content": message
        })

        if res.status_code not in [200, 204]:
            print(f"[!] Discord POST FAILED: {res.status_code} {res.text}")

        return {"status": "received", "timestamp": timestamp}

    except Exception as e:
        print("[CME ERROR]", e)
        return {"status": "error", "detail": str(e)}
