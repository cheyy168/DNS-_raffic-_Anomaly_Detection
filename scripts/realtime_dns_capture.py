import glob
import os
import time
import csv
import re

LOG_DIR = r"D:\Year3\Y3T2\DNS_Traffic_Anomaly_Project\technitium-dns\data\dns_logs"
OUTPUT_CSV = r"D:\Year3\Y3T2\DNS_Traffic_Anomaly_Project\data\dns_realtime.csv"

def follow_log():
    while True:
        logs = sorted(glob.glob(os.path.join(LOG_DIR, "*.log")))
        if not logs:
            print("[!] No log files found, retrying in 5 seconds...")
            time.sleep(5)
            continue

        latest_log = logs[-1]
        print(f"[+] Monitoring: {latest_log}")

        with open(latest_log, "r", encoding="utf-8", errors="ignore") as f, \
             open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as out_csv:

            writer = csv.writer(out_csv)
            writer.writerow(["query"])
            f.seek(0, os.SEEK_END)  # start at end to capture new lines only

            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                match = re.search(r'Query\s+\S+\s+(\S+)', line)
                if match:
                    writer.writerow([match.group(1)])
                    print(f"[+] Captured: {match.group(1)}")

if __name__ == "__main__":
    follow_log()
