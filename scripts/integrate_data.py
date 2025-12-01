#!/usr/bin/env python

"""
Integrate cleaned coffee sales and coffee shop datasets.

Usage (from the repository root):

    python scripts/integrate_data.py

This script:
- Loads cleaned CSVs from data/processed/
- Aggregates the coffee_shop data by hour_of_day to create a time-of-day profile
- Derives hour_of_day from transaction_time in the sales data
- Merges the two on hour_of_day
- Saves data/processed/coffee_integrated.csv
"""

from pathlib import Path
import sys

import pandas as pd

# Paths to input/output files
PROCESSED_DIR = Path("data/processed")
SALES_CLEAN = PROCESSED_DIR / "coffee_sales_clean.csv"
SHOP_CLEAN = PROCESSED_DIR / "coffee_shop_clean.csv"
INTEGRATED = PROCESSED_DIR / "coffee_integrated.csv"


def integrate():
    # --- Load cleaned datasets ---
    if not SALES_CLEAN.exists():
        print(f"[ERROR] Missing file: {SALES_CLEAN}", file=sys.stderr)
        sys.exit(1)
    if not SHOP_CLEAN.exists():
        print(f"[ERROR] Missing file: {SHOP_CLEAN}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading cleaned sales data from {SALES_CLEAN} ...")
    sales = pd.read_csv(SALES_CLEAN)

    print(f"Loading cleaned shop data from {SHOP_CLEAN} ...")
    shop = pd.read_csv(SHOP_CLEAN)

    print("\nSales columns:", list(sales.columns))
    print("Shop columns: ", list(shop.columns))

    # --- Derive hour_of_day in sales from transaction_time ---
    if "transaction_time" not in sales.columns:
        print(
            "[ERROR] 'transaction_time' column not found in sales data. "
            "Cannot derive hour_of_day.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Parse transaction_time; this will work if it's 'HH:MM:SS' or similar
    sales["transaction_time_parsed"] = pd.to_datetime(
        sales["transaction_time"], errors="coerce"
    )
    sales["hour_of_day"] = sales["transaction_time_parsed"].dt.hour

    # Optional: derive weekday from transaction_date if you want
    if "transaction_date" in sales.columns:
        sales["transaction_date_parsed"] = pd.to_datetime(
            sales["transaction_date"], errors="coerce"
        )
        sales["weekday"] = sales["transaction_date_parsed"].dt.day_name()

    # --- Aggregate shop data by hour_of_day to create a time-of-day profile ---

    if "hour_of_day" not in shop.columns:
        print(
            "[ERROR] 'hour_of_day' column not found in shop data. "
            "Please check coffee_shop_clean.csv.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Example aggregation: average money per hour and most frequent cash_type
    agg_dict = {}
    if "money" in shop.columns:
        agg_dict["money"] = "mean"   # average money per hour

    # Keep some categorical columns by taking the first value per hour
    keep_categorical = []
    for col in ["Time_of_Day", "Weekday", "Month_name"]:
        if col in shop.columns:
            keep_categorical.append(col)

    grouped = shop.groupby("hour_of_day", as_index=False).agg(agg_dict)

    # If we have categorical columns, merge them back by hour_of_day
    if keep_categorical:
        cat_part = (
            shop[["hour_of_day"] + keep_categorical]
            .drop_duplicates(subset=["hour_of_day"])
        )
        shop_hour_profile = grouped.merge(cat_part, on="hour_of_day", how="left")
    else:
        shop_hour_profile = grouped

    print("\nShop hourly profile:")
    print(shop_hour_profile.head())

    # --- Merge sales with shop_hour_profile on hour_of_day ---

    integrated = sales.merge(
        shop_hour_profile,
        on="hour_of_day",
        how="left",
        suffixes=("_sale", "_shop"),
    )

    print(f"\nIntegrated dataset shape: {integrated.shape}")

    # --- Save result ---
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    integrated.to_csv(INTEGRATED, index=False)
    print(f"Saved integrated dataset to {INTEGRATED}")

    # --- Quick sanity check summary ---
    print("\nBasic summary of integrated dataset:")
    print(integrated.head())
    print("\nIntegrated columns:", list(integrated.columns))


if __name__ == "__main__":
    integrate()