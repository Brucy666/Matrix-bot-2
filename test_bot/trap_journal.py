# test_bot/trap_journal.py

def log_sniper_event(event: dict):
    print("[TRAP LOG] Sniper Event Captured:")
    for key, value in event.items():
        print(f"  • {key}: {value}")
