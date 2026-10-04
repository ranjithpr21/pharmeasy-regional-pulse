"""Part 1 - cleaning pipeline + validate_schema. Run: python3 clean_data.py"""
import pandas as pd

REQUIRED = ["order_id", "order_date", "region", "category", "product",
            "quantity", "sales_inr", "profit_inr"]


def validate_schema(df, required_columns):
    missing = [c for c in required_columns if c not in df.columns]
    return {"status": "blocked_schema" if missing else "validated",
            "row_count": len(df), "missing_columns": missing}


def clean(raw_path="pharmeasy_orders_raw.csv", master_path="regions_master.csv", verbose=True):
    log = {}
    # dtype=str + keep_default_na=False: read blanks as "" (not NaN) so that exact-duplicate
    # comparison is reliable, then convert blanks to NA explicitly afterwards.
    df = pd.read_csv(raw_path, dtype=str, keep_default_na=False)
    log["raw_rows"] = len(df)
    log["raw_region_variants"] = df["region"].nunique()

    # 1. exact duplicates (all 8 columns) - done BEFORE normalisation, per spec order
    n = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    log["duplicates_removed"] = n - len(df)
    log["rows_after_dedup"] = len(df)

    # types (blank -> NaN)
    df = df.replace("", pd.NA)
    df["quantity"] = df["quantity"].astype(int)
    df["sales_inr"] = df["sales_inr"].astype(float)
    df["profit_inr"] = pd.to_numeric(df["profit_inr"])
    log["missing_profit_before"] = int(df["profit_inr"].isna().sum())
    log["missing_category_before"] = int(df["category"].isna().sum())

    # 2. region normalisation
    df["region"] = df["region"].str.strip().str.title()
    master = pd.read_csv(master_path)
    active = set(master["region"]) & set(df["region"])
    log["canonical_regions"] = df["region"].nunique()
    unknown = set(df["region"]) - set(master["region"])
    assert not unknown, f"regions not in master after normalisation: {unknown}"

    # 3. category imputation via product->category lookup (must be 1:1)
    known = df.dropna(subset=["category"])
    fan = known.groupby("product")["category"].nunique()
    assert (fan == 1).all(), "product maps to >1 category - lookup not exact"
    lookup = known.drop_duplicates("product").set_index("product")["category"].to_dict()
    df["category"] = df["category"].fillna(df["product"].map(lookup))

    # 4. profit imputation: category mean margin (from non-missing rows) x sales
    ok = df.dropna(subset=["profit_inr"])
    margin = (ok["profit_inr"] / ok["sales_inr"]).groupby(ok["category"]).mean()
    miss = df["profit_inr"].isna()
    df.loc[miss, "profit_inr"] = (df.loc[miss, "sales_inr"] * df.loc[miss, "category"].map(margin)).round(2)
    log["category_mean_margin"] = margin.round(4).to_dict()
    log["missing_after"] = {"profit_inr": int(df["profit_inr"].isna().sum()),
                            "category": int(df["category"].isna().sum())}
    df["order_date"] = pd.to_datetime(df["order_date"]).dt.strftime("%Y-%m-%d")
    df = df.sort_values("order_id").reset_index(drop=True)
    df.to_csv("orders_clean.csv", index=False)

    if verbose:
        for k, v in log.items():
            print(f"{k}: {v}")
        print("validate (clean):", validate_schema(df, REQUIRED))
        print("validate (broken):", validate_schema(df.drop(columns=["profit_inr"]), REQUIRED))
    return df, log


if __name__ == "__main__":
    clean()
