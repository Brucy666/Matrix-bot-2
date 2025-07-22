# cme_webhook_receiver.py

from fastapi import FastAPI, Request
from datetime import datetime
import json
import os
import requests

app = FastAPI()

DISCORD_WEBHOOK = os.getenv("DISCORD_OVERSEER_WEBHOOK")
LOG_FILE = "logs/cme_vsplit_alerts.txt"

@app.post("/cme")
async def receive_cme_alert(request: Request):
    try:
        body = await request.body()
        content = body.decode("utf-8").strip()

        # Timestamp
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        log_entry = f"[{timestamp}] {content}\n"

        # Log to file
        try:
            with open(LOG_FILE, "a") as f:
                f.write(log_entry)
        except Exception as log_err:
            print("[CME LOG ERROR]", log_err)

        # Format Discord message
        if content.startswith("{") or content.startswith("["):
            # JSON-style payload
            try:
                parsed = json.loads(content)
                pretty = json.dumps(parsed, indent=2)
                message = f"🟡 **CME JSON Alert**\n```json\n{pretty}```"
            except:
                message = f"🟡 CME Alert (raw JSON):\n```text\n{content}```"
        else:
            message = f"🟡 **CME Alert** `{content}`"

        # Send to Discord
        if DISCORD_WEBHOOK:
            requests.post(DISCORD_WEBHOOK, json={
                "username": "CME V-Alert",
                "content": message
            })

        return {"status": "received", "timestamp": timestamp}

    except Exception as e:
        return {"status": "error", "detail": str(e)}
