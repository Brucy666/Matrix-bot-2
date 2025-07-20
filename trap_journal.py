# trap_journal.py

import csv
import os
from datetime import datetime

JOURNAL_FILE = "logs/sniper_trap_log.csv"
os.makedirs("logs", exist_ok=True)

# Ensure the journal file exists with headers
if not os.path.exists(JOURNAL_FILE):
    with open(JOURNAL_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "entry_price", "vwap", "rsi", "score", "reasons"])

# ✅ This is the function expected by the sniper engine

def log_sniper_event(event):
    with open(JOURNAL_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            event["timestamp"],
            event["entry_price"],
            event["vwap"],
            event["rsi"],
            event["score"],
            "; ".join(event["reasons"])
        ])
    print(f"[TrapJournal] Logged sniper trap at {event['entry_price']} | Score: {event['score']} | Reasons: {event['reasons']}")

# Optional utility: read traps

def read_traps():
    traps = []
    if os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                traps.append(row)
    return traps

if __name__ == "__main__":
    # Example call for testing
    log_sniper_event({
        "timestamp": datetime.utcnow().isoformat(),
        "entry_price": 58250.12,
        "vwap": 58400.25,
        "rsi": 36.7,
        "score": 2.0,
        "reasons": ["RSI-V Split", "VWAP Retest"]
    })
    print(read_traps()[-1])
