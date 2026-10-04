"""Part 2.1 - build pharmeasy.db from Part 1 output."""
import os, sqlite3
import pandas as pd
from clean_data import clean

def build(db="pharmeasy.db"):
    df, _ = clean(verbose=False)
    if os.path.exists(db):
        os.remove(db)
    con = sqlite3.connect(db)
    pd.read_csv("regions_master.csv").to_sql("regions_master", con, index=False)
    df.to_sql("orders_clean", con, index=False)
    for t in ("regions_master", "orders_clean"):
        print(t, con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0], "rows")
    con.close()

if __name__ == "__main__":
    build()
