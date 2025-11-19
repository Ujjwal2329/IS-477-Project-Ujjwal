# Status Report – Coffee Sales & Shop Integration Project (Milestone 3)

## 1. Project Overview

This project analyzes coffee sales and customer behavior across multiple coffee shops by integrating a transaction-level **Coffee Sales** dataset with a **Coffee Shop** dataset. The goal is to build a reproducible data pipeline that handles acquisition, cleaning, integration, and analysis, and then use it to answer questions about product performance, time-of-day patterns, and store-level differences in revenue.

The project continues to follow the original plan described in `ProjectPlan.md`.

---

## 2. Status by Task (relative to ProjectPlan.md)

### 2.1 Data acquisition, license/terms verification

- **Planned (ProjectPlan.md):**  
  Download both Kaggle datasets, verify licenses/terms of use, and document sources.

- **Work completed so far:**  
  - Downloaded both coffee datasets from Kaggle.  
  - Converted the original Excel files to CSV.  
  - Stored the raw CSV files under `data/raw/`.  
  - Documented dataset sources and basic license information in `data/README.md`.

- **Artifacts in the repository:**  
  - `data/raw/coffee_sales.csv`  
  - `data/raw/coffee_shop.csv`  
  - `data/README.md`

- **Remaining work / blockers:**  
  - Add more detailed notes about the exact Kaggle licenses/terms in the final report.

---

### 2.2 Data profiling, cleaning, and schema design

- **Planned:**  
  Profile each dataset (data types, missing values, outliers), design a consistent schema, and save cleaned versions.

- **Work completed so far:**  
  - Created an initial profiling notebook that:  
    - Loads both datasets.  
    - Prints shapes, previews (`head()`), and schema information (`info()`).  
    - Computes missing value counts per column with `isna().sum()`.  
  - Saved preliminary “clean” copies of both datasets for further processing in `data/processed/`.

- **Artifacts in the repository:**  
  - `notebooks/01_profiling.ipynb`  
  - `data/processed/coffee_sales_clean.csv`  
  - `data/processed/coffee_shop_clean.csv`

- **Remaining work / blockers:**  
  - Decide on final cleaning steps (e.g., how to handle missing values and potential outliers).  
  - Finalize a documented schema for the integrated dataset (column names, types, keys).

---

### 2.3 Data integration and feature creation

- **Planned:**  
  Join the sales and shop datasets (e.g., by store or product attributes) and create features like daily revenue per store, top products by city, etc.

- **Work completed so far:**  
  - Reviewed the columns in both datasets and identified potential join keys (e.g., product names or time-of-day categories).  
  - Planned to create an integrated dataset that combines transaction-level details with time-of-day and coffee_name information.

- **Artifacts in the repository:**  
  - (Planned) `notebooks/02_integration.ipynb`  
  - (Planned) `scripts/integrate_data.py`  
  - (Planned) `data/processed/coffee_integrated.csv`

- **Remaining work / blockers:**  
  - Implement the actual merge logic in a notebook or script using `pandas.merge`.  
  - Resolve any mismatches between product naming conventions in the two datasets.  
  - Create derived features such as:
    - Daily revenue per store  
    - Top products per city or time-of-day  
    - Average ticket size (revenue per transaction)

_Current status: **Not yet started / planned for next phase**._

---

### 2.4 Exploratory analysis and visualization

- **Planned:**  
  Perform EDA on the integrated dataset and build visualizations (e.g., top-selling products, hourly sales patterns, city comparisons).

- **Work completed so far:**  
  - No full EDA on the integrated dataset yet, since integration is not complete.  
  - Initial profiling notebook provides basic insight into distributions and missing values.

- **Artifacts in the repository:**  
  - (Planned) `notebooks/03_eda.ipynb`  
  - (Planned) `figures/top_products.png`  
  - (Planned) `figures/sales_by_hour.png`

- **Remaining work / blockers:**  
  - After integration, create:
    - Bar charts of top-selling products by store/city.  
    - Time-series plots of sales by hour and day.  
    - Tables summarizing revenue and quantities by product and location.

_Current status: **Not started** (dependent on integration)._

---

### 2.5 Workflow automation and documentation

- **Planned:**  
  Implement an automated workflow (e.g., Snakemake or a Python “run all” script) that runs the full pipeline from raw data to final figures, and document how to execute it.

- **Work completed so far:**  
  - Set up a folder structure that separates raw data, processed data, notebooks, scripts, and figures.  
  - Identified major steps that will need to be automated: data loading, cleaning, integration, and visualization.

- **Artifacts in the repository:**  
  - `data/` (with `raw/` and `processed/`)  
  - `notebooks/`  
  - `scripts/`  
  - `figures/`  

- **Remaining work / blockers:**  
  - Create a `Snakefile` or `run_all.py` script that:
    1. Reads raw data  
    2. Runs cleaning and integration  
    3. Produces final summary tables and plots  
  - Test the workflow from a clean clone of the repository.  
  - Document the steps clearly in the final `README.md`.

_Current status: **Planning phase**._

---

### 2.6 Final report and GitHub organization

- **Planned:**  
  Expand `README.md` into the final project report with sections for Summary, Data profile, Data quality, Findings, Future work, Reproducing, and References.

- **Work completed so far:**  
  - Existing `README.md` provides a basic description of the project.  
  - Created additional folders to keep data, notebooks, scripts, and figures organized for the final submission.

- **Remaining work / blockers:**  
  - Populate each required section in `README.md` once analysis is more complete.  
  - Add a detailed “Reproducing” section describing how to rerun the workflow.  
  - Add references to datasets and any libraries used.

---

## 3. Updated Timeline

| Phase | Task | Original Target Date | Updated Target Date | Status | Notes |
|-------|------|----------------------|---------------------|--------|-------|
| Week 1–2 | Data acquisition, license/terms verification | Oct 1–7 | **Completed** | ✅ Completed | Datasets downloaded, converted to CSV, and stored in `data/raw/`. |
| Week 3–4 | Data profiling, cleaning, schema design | Oct 14 | **In progress** | 🟡 In progress | Initial profiling notebook completed; final cleaning rules and schema still to be finalized. |
| Week 5–6 | Data integration, feature creation | Oct 28 | **Next phase** | 🔴 Not started | Integration will be implemented after finalizing cleaning decisions. |
| Week 7–8 | Exploratory analysis, visualization | Nov 10 | **After integration** | 🔴 Not started | EDA and visualizations depend on integrated dataset. |
| Week 9–10 | Workflow automation & documentation | Nov 25 | **End of project period** | 🔴 Not started | Will be addressed once core analysis is stable. |
| Week 11–12 | Final polish & GitHub release | Dec 10 | **Dec 7–10** | 🔴 Not started | Final documentation, cleanup, and tagging for the final project. |

---

## 4. Changes to the Project Plan

- **Changes due to progress and timing:**  
  - Data acquisition and initial profiling have been completed as planned.  
  - Integration and EDA will be shifted slightly later than the original dates but still before the final project deadline.  
  - The core datasets and research questions remain the same.

- **Changes based on feedback from Milestone 2:**  
  - There was no Formal feedback on Milestone 2 that could be incorporated in this report; any required adjustments will be reflected in the final report.

---

## 5. Individual Contribution Summary

Since this is a solo project, all work for this milestone was completed by me **Ujjwal Agarwal**:

- Set up the initial repository structure (data, notebooks, scripts, figures).  
- Downloaded and converted the Kaggle coffee datasets and added them to `data/raw/`.  
- Created `data/README.md` documenting the datasets and their sources.  
- Authored the initial profiling notebook `notebooks/01_profiling.ipynb` and generated preliminary cleaned data files in `data/processed/`.  
- Wrote this `StatusReport.md` and updated the project timeline.