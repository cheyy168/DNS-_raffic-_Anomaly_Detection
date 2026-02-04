import os
import time
import re
import math
import pandas as pd
from collections import Counter
from sklearn.ensemble import IsolationForest

# --------------------------
# CONFIGURATION
# --------------------------
LOG_DIR = r"D:\Year3\Y3T2\DNS_Traffic_Anomaly_Project\technitium-dns\data\dns_logs\logs"
# Automatically pick the latest log file
OUTPUT_CSV = r"D:\Year3\Y3T2\DNS_Traffic_Anomaly_Project\data\dns_realtime.csv"

# Make sure output folder exists
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

# --------------------------
# UTILITY FUNCTIONS
# --------------------------
def entropy(s):
    """Calculate Shannon entropy of a string."""
    if not s:
        return 0
    probs = [n / len(s) for n in Counter(s).values()]
    return -sum(p * math.log2(p) for p in probs)

def extract_features(domain):
    """Return feature vector for anomaly detection."""
    return {
        "query": domain,
        "length": len(domain),
        "entropy": entropy(domain),
        "subdomains": domain.count(".")
    }

# --------------------------
# REAL-TIME LOG MONITOR
# --------------------------
def monitor_logs():
    # pick latest log file
    logs = sorted([f for f in os.listdir(LOG_DIR) if f.endswith(".log")])
    if not logs:
        print("No DNS logs found in", LOG_DIR)
        return

    logfile = os.path.join(LOG_DIR, logs[-1])
    print(f"[+] Monitoring DNS log: {logfile}")

    # keep track of already processed lines
    processed_lines = set()

    # initialize Isolation Forest model
    model = IsolationForest(contamination=0.15, random_state=42)

    while True:
        try:
            with open(logfile, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if line in processed_lines:
                        continue
                    processed_lines.add(line)

                    # extract domain query
                    match = re.search(r'Query\s+\S+\s+(\S+)', line)
                    if match:
                        domain = match.group(1)
                        # print realtime
                        print("[DNS]", domain)

                        # append to CSV
                        df = pd.DataFrame([extract_features(domain)])
                        if os.path.exists(OUTPUT_CSV):
                            df.to_csv(OUTPUT_CSV, mode='a', header=False, index=False)
                        else:
                            df.to_csv(OUTPUT_CSV, mode='w', header=True, index=False)

                        # Load CSV for anomaly detection
                        df_all = pd.read_csv(OUTPUT_CSV)
                        X = df_all[["length", "entropy", "subdomains"]]

                        # Fit model and predict
                        df_all["anomaly"] = model.fit_predict(X)

                        # Print only the latest query anomaly
                        if df_all.iloc[-1]["anomaly"] == -1:
                            print(f"[ALERT] Suspicious DNS: {domain} | Entropy={df_all.iloc[-1]['entropy']:.2f}")
        except FileNotFoundError:
            print(f"Log file not found yet: {logfile}")
        time.sleep(1)

# --------------------------
# MAIN
# --------------------------
if __name__ == "__main__":
    monitor_logs()
