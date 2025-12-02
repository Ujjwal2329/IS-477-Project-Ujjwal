"""
scripts/clean_data.py

Clean the raw coffee sales and coffee shop datasets and write
cleaned versions to data/processed/.

Usage (from project root):

    python scripts/clean_data.py

This script is part of the Data Quality & Cleaning stage:
- Converts key columns to proper types
- Drops obvious bad rows (missing/invalid qty/price/hour)
- Removes duplicates
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def clean_sales():
    """Clean the coffee_sales.csv file and write coffee_sales_clean.csv."""
    raw_path = RAW_DIR / "coffee_sales.csv"
    out_path = PROCESSED_DIR / "coffee_sales_clean.csv"

    print(f"Loading raw sales data from {raw_path} ...")
    sales = pd.read_csv(raw_path)

    print("Initial sales shape:", sales.shape)

    # --- Strip whitespace in string columns ---
    for col in sales.select_dtypes(include="object").columns:
        sales[col] = sales[col].astype(str).str.strip()

    # --- Remove duplicate transactions (by transaction_id) ---
    if "transaction_id" in sales.columns:
        before = len(sales)
        sales = sales.drop_duplicates(subset=["transaction_id"])
        after = len(sales)
        print(f"Dropped {before - after} duplicate rows based on transaction_id")

    # --- Convert numeric columns ---
    # transaction_qty and unit_price are critical for analysis
    if "transaction_qty" in sales.columns:
        sales["transaction_qty"] = pd.to_numeric(
            sales["transaction_qty"], errors="coerce"
        )
    if "unit_price" in sales.columns:
        sales["unit_price"] = pd.to_numeric(
            sales["unit_price"], errors="coerce"
        )

    # --- Drop rows with missing or invalid qty/price ---
    critical_cols = [col for col in ["transaction_qty", "unit_price"] if col in sales.columns]
    if critical_cols:
        before = len(sales)
        # Drop rows with NaN or non-positive qty/price
        mask_valid = (sales[critical_cols] > 0).all(axis=1)
        mask_notna = sales[critical_cols].notna().all(axis=1)
        sales = sales[mask_valid & mask_notna]
        after = len(sales)
        print(f"Dropped {before - after} rows with missing/invalid qty/price")

    print("Cleaned sales shape:", sales.shape)
    print(f"Writing cleaned sales data to {out_path} ...")
    sales.to_csv(out_path, index=False)


def clean_shop():
    """Clean the coffee_shop.csv file and write coffee_shop_clean.csv."""
    raw_path = RAW_DIR / "coffee_shop.csv"
    out_path = PROCESSED_DIR / "coffee_shop_clean.csv"

    print(f"Loading raw shop data from {raw_path} ...")
    shop = pd.read_csv(raw_path)

    print("Initial shop shape:", shop.shape)

    # --- Strip whitespace in string columns ---
    for col in shop.select_dtypes(include="object").columns:
        shop[col] = shop[col].astype(str).str.strip()

    # --- Convert hour_of_day and money to numeric where present ---
    if "hour_of_day" in shop.columns:
        shop["hour_of_day"] = pd.to_numeric(
            shop["hour_of_day"], errors="coerce"
        )
    if "money" in shop.columns:
        shop["money"] = pd.to_numeric(
            shop["money"], errors="coerce"
        )

    # --- Drop rows with missing/invalid hour_of_day ---
    if "hour_of_day" in shop.columns:
        before = len(shop)
        shop = shop.dropna(subset=["hour_of_day"])
        shop = shop[(shop["hour_of_day"] >= 0) & (shop["hour_of_day"] <= 23)]
        shop["hour_of_day"] = shop["hour_of_day"].astype(int)
        after = len(shop)
        print(f"Dropped {before - after} rows with invalid hour_of_day")

    # --- Drop rows with missing money if you want to use money as a metric ---
    if "money" in shop.columns:
        before = len(shop)
        shop = shop.dropna(subset=["money"])
        after = len(shop)
        print(f"Dropped {before - after} rows with missing money")

    print("Cleaned shop shape:", shop.shape)
    print(f"Writing cleaned shop data to {out_path} ...")
    shop.to_csv(out_path, index=False)


def main():
    clean_sales()
    print("-" * 60)
    clean_shop()


if __name__ == "__main__":
    main()