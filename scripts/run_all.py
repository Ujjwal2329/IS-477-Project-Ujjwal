"""
scripts/run_all.py

Simple "Run All" script to execute the full pipeline in order:

1. Download raw data from Kaggle  -> data/raw/
2. Clean raw data                 -> data/processed/coffee_sales_clean.csv,
                                     data/processed/coffee_shop_clean.csv
3. Integrate cleaned data         -> data/processed/coffee_integrated.csv
4. Generate analysis figures      -> figures/*.png

Usage (from project root):

    python scripts/run_all.py
"""

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_step(cmd, step_name):
    print(f"\n=== {step_name} ===")
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print(f"Step '{step_name}' failed with exit code {result.returncode}.", file=sys.stderr)
        sys.exit(result.returncode)
    else:
        print(f"Step '{step_name}' completed successfully.")


def main():
    steps = [
        (["python", "scripts/get_data.py", "download"], "Download raw data"),
        (["python", "scripts/clean_data.py"], "Clean data"),
        (["python", "scripts/integrate_data.py"], "Integrate data"),
        (["python", "scripts/make_figures.py"], "Generate figures"),
    ]

    for cmd, name in steps:
        run_step(cmd, name)

    print("\nAll steps completed successfully. Raw, cleaned, integrated data and figures are up to date.")


if __name__ == "__main__":
    main()