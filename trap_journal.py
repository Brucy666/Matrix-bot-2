# trap_journal.py
# Logs sniper trap data to CSV

import csv
import os
from datetime import datetime

JOURNAL_FILE = "logs/trap_journal.csv"

# Ensure headers exist
if not os.path.exists(JOURNAL_FILE):
    with open(JOURNAL_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Timestamp", "Symbol", "Exchange", "Price", "VWAP", "RSI",
            "Score", "Confidence", "RSI_Status", "Echo_V_Status", "V_Score",
            "Spoof_Ratio", "Bias", "Trap_Type", "Macro_Bias", "Macro_Vsplits"
        ])

def log_sniper_event(data):
    row = [
        data.get("timestamp"),
        data.get("symbol"),
        data.get("exchange"),
        data.get("entry_price"),
        data.get("vwap"),
        data.get("rsi"),
        data.get("score"),
        data.get("confidence"),
        data.get("rsi_status"),
        data.get("echo_v_status", "None"),
        data.get("vsplit_score"),
        data.get("spoof_ratio"),
        data.get("bias"),
        data.get("trap_type"),
        data.get("macro_biases", ["None"])[0],
        " | ".join(data.get("macro_vsplit", []))
    ]

    with open(JOURNAL_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

    print(f"[Journal] Logged {data['symbol']} {data['trap_type']} | Score: {data['score']}")
