x# trap_journal.py
# Logs sniper signal entries to file for historical analysis

import os
import csv
from datetime import datetime

LOG_FILE = "logs/trap_journal.csv"
FIELDNAMES = [
    "timestamp", "symbol", "exchange", "entry_price", "vwap", "rsi",
    "trap_type", "score", "confidence", "bias", "spoof_ratio", "rsi_status",
    "vsplit_score", "macro_vsplit", "macro_biases", "binance_bid_wall", "binance_ask_wall",
    "echo_v_status", "echo_v_tf_confluence", "price"
]

def log_sniper_event(trap):
    os.makedirs("logs", exist_ok=True)
    file_exists = os.path.isfile(LOG_FILE)

    row = {
        "timestamp": trap.get("timestamp", datetime.utcnow().isoformat()),
        "symbol": trap.get("symbol", "N/A"),
        "exchange": trap.get("exchange", "N/A"),
        "entry_price": trap.get("entry_price", 0),
        "vwap": trap.get("vwap", 0),
        "rsi": trap.get("rsi", 0),
        "trap_type": trap.get("trap_type", "N/A"),
        "score": trap.get("score", 0),
        "confidence": trap.get("confidence", 0),
        "bias": trap.get("bias", "N/A"),
        "spoof_ratio": trap.get("spoof_ratio", 0),
        "rsi_status": trap.get("rsi_status", "None"),
        "vsplit_score": trap.get("vsplit_score", "None"),
        "macro_vsplit": ",".join(trap.get("macro_vsplit", [])),
        "macro_biases": ",".join(trap.get("macro_biases", [])),
        "binance_bid_wall": trap.get("binance_bid_wall", 0),
        "binance_ask_wall": trap.get("binance_ask_wall", 0),
        "echo_v_status": trap.get("echo_v_status", "None"),
        "echo_v_tf_confluence": trap.get("echo_v_tf_confluence", "None"),
        "price": trap.get("price", 0)
    }

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
