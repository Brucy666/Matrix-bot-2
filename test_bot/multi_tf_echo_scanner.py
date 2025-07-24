# multi_tf_echo_scanner.py
# Scans multiple timeframe KuCoin feeds for Echo V signals

from echo_v_engine import get_echo_v_signal

def get_multi_tf_echo_signals(tf_data_map):
    signals = []
    try:
        for tf, df in tf_data_map.items():
            if df is None or len(df) < 20:
                continue

            signal = get_echo_v_signal(df)
            status = signal.get("status")
            strength = signal.get("strength", 0)

            if status and status != "None":
                signals.append(f"{tf}: {status}")

        if signals:
            return ", ".join(signals)
        else:
            return "None"
    
    except Exception as e:
        print("[Multi-TF Echo ERROR]", e)
        return "Error"
