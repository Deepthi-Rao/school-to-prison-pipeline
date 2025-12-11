#!/usr/bin/env python3
import os
import requests
from time import sleep

# Folder to save the downloads
OUTPUT_DIR = "2017-2018"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 50 states + DC + Puerto Rico
STATE_CODES = [
    "AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL",
    "GA","HI","ID","IL","IN","IA","KS","KY","LA","ME",
    "MD","MA","MI","MN","MS","MO","MT","NE","NV","NH",
    "NJ","NM","NY","NC","ND","OH","OK","OR","PA","PR",
    "RI","SC","SD","TN","TX","UT","VT","VA","WA","WV",
    "WI","WY"
]

BASE_URL = "https://eddataexpress.ed.gov/sites/default/files/data_files/CRDC_2017-18_{}.xlsx"

def download_state(state_code: str):
    url = BASE_URL.format(state_code)
    out_path = os.path.join(OUTPUT_DIR, f"CRDC_2017-18_{state_code}.xlsx")

    # Skip if already downloaded
    if os.path.exists(out_path):
        print(f"[SKIP] {state_code} already downloaded.")
        return

    print(f"[DOWNLOADING] {state_code} from {url} ...")
    try:
        resp = requests.get(url, stream=True, timeout=60, verify=False)
        if resp.status_code == 200:
            with open(out_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"[OK] Saved to {out_path}")
        else:
            print(f"[ERROR] {state_code}: HTTP {resp.status_code}")
    except Exception as e:
        print(f"[ERROR] {state_code}: {e}")

def main():
    for code in STATE_CODES:
        download_state(code)
        # Be polite to the server
        sleep(0.5)

if __name__ == "__main__":
    main()

