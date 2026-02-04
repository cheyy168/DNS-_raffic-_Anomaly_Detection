import pandas as pd
import math
from collections import Counter
from sklearn.ensemble import IsolationForest
import time

CSV_FILE = r"D:\Year3\Y3T2\DNS_Traffic_Anomaly_Project\data\dns_realtime.csv"

def entropy(s):
    probs = [n / len(s) for n in Counter(s).values()]
    return -sum(p * math.log2(p) for p in probs)

print("[+] Real-time DNS anomaly detection running...")

# Keep memory of processed queries to avoid duplicates
processed_rows = 0

while True:
    try:
        df = pd.read_csv(CSV_FILE)
        new_df = df.iloc[processed_rows:]
        if not new_df.empty:
            # feature extraction
            new_df["length"] = new_df["query"].apply(len)
            new_df["entropy"] = new_df["query"].apply(entropy)
            new_df["subdomains"] = new_df["query"].apply(lambda x: x.count("."))

            X = new_df[["length", "entropy", "subdomains"]]
            model = IsolationForest(contamination=0.15, random_state=42)
            new_df["anomaly"] = model.fit_predict(X)

            for _, row in new_df[new_df["anomaly"] == -1].iterrows():
                print(f"[ALERT] Suspicious DNS Query: {row['query']} | Entropy={row['entropy']:.2f}")

            processed_rows = len(df)
    except Exception as e:
        print(f"[!] Error: {e}")

    time.sleep(2)
