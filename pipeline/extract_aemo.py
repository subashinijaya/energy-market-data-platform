"""
extract_aemo.py
----------------
Downloads AEMO Historical Demand (HistDemand) daily files from NEMWEB,
unzips them, filters for SA1 region only, and saves clean CSVs into
data/raw/.

Author: Anne Subashini Sritharan
Project: energy-market-data-platform
"""

import requests
import zipfile
import io
import pandas as pd
from datetime import date, timedelta
import os

# ---------- SETTINGS ----------
BASE_URL = "https://nemweb.com.au/Reports/Current/HistDemand/"
OUTPUT_FOLDER = "data/raw"
REGION_FILTER = "SA1"        # South Australia only
DAYS_TO_PULL = 7             # start small, scale up later

# ---------- SETUP ----------
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def get_file_list():
    """
    Fetch the HistDemand folder page and pull out all .zip filenames.
    """
    print("Fetching file list from NEMWEB...")
    response = requests.get(BASE_URL)
    response.raise_for_status()

    # crude but effective: pull filenames ending in .zip
    lines = response.text.split('"')
    zip_files = [line for line in lines if line.endswith(".zip")]

    # NEMWEB sometimes gives the full path (e.g. /Reports/CURRENT/HistDemand/xxx.zip)
    # instead of just the filename — strip it down to filename only
    zip_files = [f.split("/")[-1] for f in zip_files]

    return zip_files


def download_and_extract(zip_filename):
    """
    Download one zip file, extract the CSV inside it, and return
    it as a pandas DataFrame (filtered for SA1 only).
    """
    url = BASE_URL + zip_filename
    print(f"Downloading: {zip_filename}")

    response = requests.get(url)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        csv_name = z.namelist()[0]  # only one file inside
        with z.open(csv_name) as f:
            # AEMO files have C/I/D row types — we only want D rows
            df = pd.read_csv(
                f,
                skiprows=1,     # skip the C (header) line
                header=0,       # I line becomes column headers
                low_memory=False
            )

    # Drop the trailing footer row if present, and keep only D rows
    df = df[df.iloc[:, 0] == "D"]

    # Rename columns based on AEMO's known HistDemand structure
    df.columns = [
        "ROWTYPE", "TABLE", "SOURCE", "VERSION",
        "REGIONID", "SETTLEMENTDATE", "PERIODID", "DEMAND"
    ]

    # Filter for SA1 only
    df_sa = df[df["REGIONID"] == REGION_FILTER].copy()

    # Keep only the useful columns
    df_sa = df_sa[["REGIONID", "SETTLEMENTDATE", "PERIODID", "DEMAND"]]

    return df_sa


def main():
    zip_files = get_file_list()

    if not zip_files:
        print("No files found — check the NEMWEB page structure.")
        return

    # Take the most recent N days
    recent_files = zip_files[-DAYS_TO_PULL:]

    all_data = []

    for zip_filename in recent_files:
        try:
            df_sa = download_and_extract(zip_filename)
            all_data.append(df_sa)
            print(f"  -> {len(df_sa)} SA1 rows extracted")
        except Exception as e:
            print(f"  !! Failed on {zip_filename}: {e}")

    if not all_data:
        print("No data extracted. Stopping.")
        return

    # Combine all days into one clean file
    combined = pd.concat(all_data, ignore_index=True)

    output_path = os.path.join(OUTPUT_FOLDER, "sa_demand_combined.csv")
    combined.to_csv(output_path, index=False)

    print(f"\nDone! Saved {len(combined)} total rows to: {output_path}")


if __name__ == "__main__":
    main()