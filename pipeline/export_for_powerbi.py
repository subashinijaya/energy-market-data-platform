"""
export_for_powerbi.py
-----------------------
Phase 5 (prep step): Exports the star schema tables built by dbt
(dim_date, dim_region, fact_demand) from the SQLite warehouse into
clean CSV files that Power BI can load directly.

Author: Anne Subashini Sritharan
Project: energy-market-data-platform
"""

import sqlite3
import pandas as pd
import os

DB_FILE = "data/warehouse.db"
OUTPUT_FOLDER = "powerbi/data"

TABLES = ["dim_date", "dim_region", "fact_demand"]


def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    conn = sqlite3.connect(DB_FILE)

    for table in TABLES:
        print(f"Exporting: {table}")
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)

        output_path = os.path.join(OUTPUT_FOLDER, f"{table}.csv")
        df.to_csv(output_path, index=False)

        print(f"  -> {len(df)} rows saved to {output_path}")

    conn.close()
    print("\nDone! All tables exported for Power BI.")


if __name__ == "__main__":
    main()