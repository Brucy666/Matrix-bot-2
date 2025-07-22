# cme_webhook_receiver.py
from fastapi import FastAPI, Request
import json
from datetime import datetime
import requests
import os

app = FastAPI()

DISCORD_WEBHOOK = os.getenv("DISCORD_OVERSEER_WEBHOOK")
LOG_FILE = "logs/cme_vsplit_alerts.txt"

@app.post("/cme")
async def receive_cme_alert(request: Request):
    body = await request.body()
    payload = body.decode("utf-8")

    # Log alert with timestamp
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {payload}\n")

    # Optional Discord forward
    requests.post(DISCORD_WEBHOOK, json={
        "username": "CME V-Alert",
        "content": f"🟡 CME Alert: `{payload.strip()}`"
    })

    return {"status": "received"}
