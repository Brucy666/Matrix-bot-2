# trap_journal.py
# Logs sniper trap entries to a CSV file for tracking + audit

import csv
import os
from datetime import datetime

LOG_FILE = "logs/trap_journal.csv"

# Ensure the journal file exists and has headers
def ensure_log_file():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Timestamp", "Symbol", "Exchange", "Price", "VWAP", "RSI", "Score",
                "Trap Type", "RSI Status", "VWAP Zone", "Echo V",
                "Spoof Ratio", "Bias", "Confidence",
                "Macro Bias", "Macro V-Splits", "Result"
            ])

# Write a new trap entry to the log
def log_sniper_event(data):
    ensure_log_file()

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.utcnow().isoformat(),
            data.get("symbol", "N/A"),
            data.get("exchange", "N/A"),
            data.get("entry_price", 0),
            data.get("vwap", 0),
            data.get("rsi", 0),
            data.get("score", 0),
            data.get("trap_type", "Unclassified"),
            data.get("rsi_status", "None"),
            data.get("vsplit_score", "None"),
            data.get("echo_v", "None"),
            data.get("spoof_ratio", 0),
            data.get("bias", "Unknown"),
            data.get("confidence", 0),
            data.get("macro_biases", [])[0] if data.get("macro_biases") else "Unclassified",
            "; ".join(data.get("macro_vsplit", [])) if data.get("macro_vsplit") else "None",
            data.get("result", "pending")
        ])

    print(f"[TrapJournal] Logged trap: {data.get('symbol')} | Score: {data.get('score')} | EchoV: {data.get('echo_v')}")

# Optional: Read past traps
def read_traps():
    ensure_log_file()
    traps = []
    with open(LOG_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            traps.append(row)
    return traps

# For direct test
if __name__ == "__main__":
    log_sniper_event({
        "symbol": "BTC/USDT",
        "exchange": "KuCoin",
        "entry_price": 58300.25,
        "vwap": 58240.00,
        "rsi": 43.5,
        "score": 3.2,
        "trap_type": "RSI-V + VWAP Trap",
        "rsi_status": "RSI V-Split",
        "vsplit_score": "VWAP Zone",
        "echo_v": "Bullish Echo V",
        "spoof_ratio": 1.8,
        "bias": "Below",
        "confidence": 7.5,
        "macro_biases": ["Strong Bull"],
        "macro_vsplit": ["1D: RSI V-Split (14.2)", "4H: RSI Collapse (10.1)"],
        "result": "pending"
    })

    print(read_traps()[-1])
