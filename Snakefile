# Snakefile
#
# Snakemake workflow to automate the end-to-end analysis:
# 1. Download raw data from Kaggle
# 2. Clean raw data -> processed CSVs
# 3. Integrate datasets -> coffee_integrated.csv
# 4. Generate figures -> figures/*.png

import os
from pathlib import Path

PROJECT_ROOT = Path(".").resolve()
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
FIGURES_DIR = PROJECT_ROOT / "figures"

RAW_SALES = RAW_DIR / "coffee_sales.csv"
RAW_SHOP = RAW_DIR / "coffee_shop.csv"

CLEAN_SALES = PROCESSED_DIR / "coffee_sales_clean.csv"
CLEAN_SHOP = PROCESSED_DIR / "coffee_shop_clean.csv"

INTEGRATED = PROCESSED_DIR / "coffee_integrated.csv"

FIG_TOP_PRODUCTS = FIGURES_DIR / "top_products_by_revenue.png"
FIG_REV_BY_HOUR = FIGURES_DIR / "revenue_by_hour_of_day.png"
FIG_REV_BY_TOD  = FIGURES_DIR / "revenue_by_time_of_day.png"
FIG_TOP_STORES  = FIGURES_DIR / "top_stores_by_revenue.png"


rule all:
    """
    Final targets of the workflow.
    Running `snakemake` without args will build all of these.
    """
    input:
        INTEGRATED,
        FIG_TOP_PRODUCTS,
        FIG_REV_BY_HOUR,
        FIG_REV_BY_TOD,
        FIG_TOP_STORES


rule get_data:
    """
    Download raw datasets from Kaggle into data/raw/ using scripts/get_data.py.
    """
    output:
        RAW_SALES,
        RAW_SHOP
    shell:
        """
        python scripts/get_data.py download
        """


rule clean_data:
    """
    Clean raw data -> data/processed/coffee_sales_clean.csv,
    data/processed/coffee_shop_clean.csv.
    """
    input:
        RAW_SALES,
        RAW_SHOP
    output:
        CLEAN_SALES,
        CLEAN_SHOP
    shell:
        """
        python scripts/clean_data.py
        """


rule integrate_data:
    """
    Integrate cleaned sales and shop data into coffee_integrated.csv.
    """
    input:
        CLEAN_SALES,
        CLEAN_SHOP
    output:
        INTEGRATED
    shell:
        """
        python scripts/integrate_data.py
        """


rule make_figures:
    """
    Generate analysis figures from the integrated dataset.
    """
    input:
        INTEGRATED
    output:
        FIG_TOP_PRODUCTS,
        FIG_REV_BY_HOUR,
        FIG_REV_BY_TOD,
        FIG_TOP_STORES
    shell:
        """
        python scripts/make_figures.py
        """