"""
load_to_db.py
---------------
Phase 2: ETL
Reads the combined SA1 demand CSV from Phase 1, cleans it,
and loads it into a SQLite database (data/warehouse.db).

This becomes the foundation that dbt (Phase 3) will build on.

Author: Anne Subashini Sritharan
Project: energy-market-data-platform
"""

import pandas as pd
import sqlite3
import os

# ---------- SETTINGS ----------
INPUT_FILE = "data/raw/sa_demand_combined.csv"
DB_FILE = "data/warehouse.db"
TABLE_NAME = "raw_demand"


def load_and_clean():
    """
    Read the raw CSV, clean it up, and return a tidy DataFrame.
    """
    print(f"Reading: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)

    # ---- Clean step 1: correct data types ----
    df["SETTLEMENTDATE"] = pd.to_datetime(df["SETTLEMENTDATE"])
    df["PERIODID"] = df["PERIODID"].astype(int)
    df["DEMAND"] = df["DEMAND"].astype(float)

    # ---- Clean step 2: remove duplicates ----
    before = len(df)
    df = df.drop_duplicates(subset=["REGIONID", "SETTLEMENTDATE", "PERIODID"])
    after = len(df)
    if before != after:
        print(f"  Removed {before - after} duplicate rows")

    # ---- Clean step 3: check for missing/negative demand ----
    bad_rows = df[df["DEMAND"].isna() | (df["DEMAND"] < 0)]
    if len(bad_rows) > 0:
        print(f"  WARNING: {len(bad_rows)} rows have missing/negative demand")
        df = df[~df.index.isin(bad_rows.index)]

    # ---- Clean step 4: sort nicely ----
    df = df.sort_values(["SETTLEMENTDATE", "PERIODID"]).reset_index(drop=True)

    print(f"Clean rows ready: {len(df)}")
    return df


def load_to_sqlite(df):
    """
    Write the cleaned DataFrame into a SQLite database table.
    """
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
    conn.close()

    print(f"Loaded {len(df)} rows into {DB_FILE} -> table '{TABLE_NAME}'")


def main():
    df = load_and_clean()
    load_to_sqlite(df)
    print("\nPhase 2 ETL complete!")


if __name__ == "__main__":
    main()