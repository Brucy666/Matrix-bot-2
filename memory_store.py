import json
import os
import time
from datetime import datetime

MEMORY_PATH = "./memory_logs"

# Ensure memory directory exists
if not os.path.exists(MEMORY_PATH):
    os.makedirs(MEMORY_PATH)

def remember_trap(symbol, trade_data):
    """
    Save a trap detection to file.
    Filename includes the symbol and timestamp.
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"trap_{symbol.replace('/', '-')}_{timestamp}.json"
    path = os.path.join(MEMORY_PATH, filename)
    with open(path, "w") as f:
        json.dump(trade_data, f, indent=2)
    print(f"[MemoryStore] Trap saved: {filename}")

def load_all_traps():
    """
    Load all trap files from memory_logs folder.
    """
    traps = []
    for filename in os.listdir(MEMORY_PATH):
        if filename.endswith(".json"):
            with open(os.path.join(MEMORY_PATH, filename), "r") as f:
                traps.append(json.load(f))
    return traps

def filter_traps_by_symbol(symbol):
    """
    Return all traps matching the given symbol.
    """
    return [t for t in load_all_traps() if t.get("symbol") == symbol]

# Optional test mode
if __name__ == "__main__":
    dummy = {
        "symbol": "BTC-USDT",
        "score": 92,
        "reason": "RSI-V + VWAP Trap",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }
    remember_trap(dummy["symbol"], dummy)
    print("Loaded traps:", filter_traps_by_symbol("BTC-USDT"))
