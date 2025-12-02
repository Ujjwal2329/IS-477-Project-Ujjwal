"""
scripts/make_figures.py

Generate key analysis figures from the integrated dataset and save them
to the figures/ directory.

Usage (from project root):

    python scripts/make_figures.py

This script is part of the "Data analysis and visualization" stage:
- Loads data/processed/coffee_integrated.csv
- Ensures a 'revenue' column exists
- Creates:
  - top_products_by_revenue.png
  - revenue_by_hour_of_day.png
  - revenue_by_time_of_day.png
  - top_stores_by_revenue.png
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
FIGURES_DIR = PROJECT_ROOT / "figures"

INTEGRATED_PATH = PROCESSED_DIR / "coffee_integrated.csv"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def load_integrated() -> pd.DataFrame:
    df = pd.read_csv(INTEGRATED_PATH)
    if "revenue" not in df.columns and {"transaction_qty", "unit_price"}.issubset(df.columns):
        df["revenue"] = df["transaction_qty"] * df["unit_price"]
    return df


def plot_top_products_by_revenue(df: pd.DataFrame):
    product_col = None
    for candidate in ["product_type", "product_category", "product_detail", "product_id"]:
        if candidate in df.columns:
            product_col = candidate
            break

    if product_col is None:
        print("No suitable product column found; skipping top products plot.")
        return

    product_summary = (
        df
        .groupby(product_col, as_index=False)
        .agg(
            total_qty=("transaction_qty", "sum"),
            total_revenue=("revenue", "sum")
        )
        .sort_values("total_revenue", ascending=False)
    )

    top_products = product_summary.head(10)
    top_products_sorted = top_products.sort_values("total_revenue", ascending=True)

    plt.figure(figsize=(10, 5))
    plt.barh(top_products_sorted[product_col], top_products_sorted["total_revenue"])
    plt.xlabel("Total revenue")
    plt.ylabel(product_col)
    plt.title(f"Top 10 {product_col} by revenue")
    plt.tight_layout()

    fig_path = FIGURES_DIR / "top_products_by_revenue.png"
    plt.savefig(fig_path, dpi=150)
    plt.close()
    print(f"Saved {fig_path}")


def plot_revenue_by_hour(df: pd.DataFrame):
    if "hour_of_day" not in df.columns:
        print("hour_of_day not found; skipping revenue_by_hour_of_day plot.")
        return

    rev_by_hour = (
        df
        .groupby("hour_of_day", as_index=False)
        .agg(total_revenue=("revenue", "sum"))
        .sort_values("hour_of_day")
    )

    plt.figure(figsize=(8, 4))
    plt.plot(rev_by_hour["hour_of_day"], rev_by_hour["total_revenue"])
    plt.xlabel("Hour of day")
    plt.ylabel("Total revenue")
    plt.title("Total revenue by hour of day")
    plt.xticks(range(0, 24, 2))
    plt.tight_layout()

    fig_path = FIGURES_DIR / "revenue_by_hour_of_day.png"
    plt.savefig(fig_path, dpi=150)
    plt.close()
    print(f"Saved {fig_path}")


def plot_revenue_by_time_of_day(df: pd.DataFrame):
    if "Time_of_Day" not in df.columns:
        print("Time_of_Day not found; skipping revenue_by_time_of_day plot.")
        return

    rev_by_tod = (
        df
        .groupby("Time_of_Day", as_index=False)
        .agg(total_revenue=("revenue", "sum"))
        .sort_values("total_revenue", ascending=False)
    )

    plt.figure(figsize=(6, 4))
    plt.bar(rev_by_tod["Time_of_Day"], rev_by_tod["total_revenue"])
    plt.xlabel("Time of Day")
    plt.ylabel("Total revenue")
    plt.title("Total revenue by Time_of_Day")
    plt.tight_layout()

    fig_path = FIGURES_DIR / "revenue_by_time_of_day.png"
    plt.savefig(fig_path, dpi=150)
    plt.close()
    print(f"Saved {fig_path}")


def plot_top_stores_by_revenue(df: pd.DataFrame):
    if "store_location" not in df.columns:
        print("store_location not found; skipping top_stores_by_revenue plot.")
        return

    rev_by_store = (
        df
        .groupby("store_location", as_index=False)
        .agg(total_revenue=("revenue", "sum"))
        .sort_values("total_revenue", ascending=False)
    )

    top_stores = rev_by_store.head(10)
    top_stores_sorted = top_stores.sort_values("total_revenue", ascending=True)

    plt.figure(figsize=(8, 5))
    plt.barh(top_stores_sorted["store_location"], top_stores_sorted["total_revenue"])
    plt.xlabel("Total revenue")
    plt.ylabel("Store location")
    plt.title("Top 10 store locations by revenue")
    plt.tight_layout()

    fig_path = FIGURES_DIR / "top_stores_by_revenue.png"
    plt.savefig(fig_path, dpi=150)
    plt.close()
    print(f"Saved {fig_path}")


def main():
    df = load_integrated()
    print(f"Loaded integrated data: {df.shape}")

    plot_top_products_by_revenue(df)
    plot_revenue_by_hour(df)
    plot_revenue_by_time_of_day(df)
    plot_top_stores_by_revenue(df)


if __name__ == "__main__":
    main()