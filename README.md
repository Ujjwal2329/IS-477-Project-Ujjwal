# IS-477-Project
Course project for IS 477
# Coffee Sales & Shop Integration Project

---

## Summary

This project investigates coffee sales and customer behavior across multiple coffee shops by integrating a transaction-level **Coffee Sales** dataset with a time-of-day–level **Coffee Shop** dataset. The primary goal is to build a **fully reproducible data pipeline** that spans data acquisition, storage and organization, cleaning, integration, analysis, and documentation.

The work is motivated by practical questions that coffee shop operators and analysts might ask, such as: *Which products generate the most revenue? How do sales vary by time of day and location? Are there recognizable patterns in customer behavior that could inform staffing, inventory, or promotions?* To address these questions, the project is structured around three core research questions:

1. **Which coffee products generate the highest sales volume and/or revenue across locations?**
2. **How do customer preferences (e.g., drink type, size, add-ons or product category) vary by time of day and store/location?**
3. **Can integrated sales and shop-level data reveal which operational factors (e.g., location, product mix, time-of-day patterns) are associated with higher daily or hourly sales?**

Methodologically, the project follows the data lifecycle discussed in class:

- **Acquisition**: Raw data are programmatically downloaded from Kaggle using the Kaggle API and a dedicated Python script (`scripts/get_data.py`), rather than being stored directly in the repository.
- **Storage & organization**: Data are managed in a clearly documented filesystem-based layout under `data/`, with a distinction between `data/raw/` and `data/processed/` and consistent naming conventions.
- **Profiling & cleaning**: Initial profiling is performed in a Jupyter notebook (`notebooks/01_profiling.ipynb`), and cleaning logic is captured in scripts/notebooks that create cleaned versions of the datasets and normalize important fields (dates, times, numeric columns).
- **Integration & enrichment**: The cleaned datasets are integrated using a time-of-day–based model: transaction-level sales data are enriched with an hourly profile derived from the coffee shop dataset, implemented in `scripts/integrate_data.py`.
- **Analysis & visualization**: Exploratory data analysis (EDA) notebooks and scripts use the integrated dataset to compute descriptive statistics and generate visualizations (e.g., top-selling products, sales by hour of day and store location).
- **Reproducibility & documentation**: All key steps are automated or documented through scripts, notebooks, a structured repository layout, and this Markdown report.

Overall, the project demonstrates how two heterogeneous but related datasets can be combined into an integrated analytical view. The final integrated dataset supports answering the research questions by providing a unified table with transaction-level detail, location information, and time-of-day contextual features. While the main focus is descriptive and exploratory rather than predictive modeling, the resulting pipeline could readily be extended to forecasting or segmentation in future work.

---

## Data profile

This project uses two public Kaggle datasets, both distributed in tabular form. They are accessed programmatically and stored locally as CSV files.

### Coffee Sales dataset

- **Source**: Kaggle – “Coffee Sales Dataset” (`ahmedabbas757/coffee-sales`)
- **Local file**: `data/raw/coffee_sales.csv` (downloaded via `scripts/get_data.py`)
- **Granularity**: Each row represents a **single transaction**.
- **Key fields** (from the cleaned version `coffee_sales_clean.csv`):
  - `transaction_id`: Unique identifier for each transaction.
  - `transaction_date`: Date of the transaction (string in the raw data, converted to datetime in cleaning).
  - `transaction_time`: Time of the transaction (string in the raw data, converted to a time/datetime object).
  - `transaction_qty`: Quantity of units sold in the transaction.
  - `store_id`: Identifier for the store where the transaction occurred.
  - `store_location`: Human-readable store location (e.g., city or neighborhood).
  - `product_id`: Product identifier.
  - `product_category`: High-level product category (e.g., coffee, food, other).
  - `product_type`: More specific product type or submenu category.
  - `product_detail`: Additional descriptive information about the product.
  - `unit_price`: Unit price of the item at the time of the transaction.

**Intended use in the project**

This dataset provides the **core transactional view** needed to compute:

- Sales volume and revenue by product, category, store, and time.
- Customer preference patterns by store/location and time of day.
- Derived features at various aggregation levels (e.g., daily revenue per store, hourly transactions, popular product categories by location).

**Ethical and legal constraints**

- The dataset is publicly available on Kaggle and is used under its specified license for **educational and non-commercial** purposes.
- It does not contain direct personal identifiers; analysis focuses on aggregated patterns of purchases.
- The project does not attempt to deanonymize or link the data to external person-level sources.
- Raw Kaggle files are **not redistributed** in the Git repository; instead, they are downloaded on demand using the Kaggle API, respecting terms of use.

---

### Coffee Shop dataset

- **Source**: Kaggle – “Coffee Shop Dataset” (`jawad3664/coffee-shop`)
- **Local file**: `data/raw/coffee_shop.csv`
- **Granularity**: Each row represents a **time-of-day/operational record**, often associated with hour-of-day, weekday, and other shop-level context.
- **Key fields** (from the cleaned version `coffee_shop_clean.csv`):
  - `hour_of_day`: Integer hour (0–23) representing the time of day.
  - `cash_type`: Payment method category (e.g., card, cash) or similar.
  - `money`: Monetary amount associated with that hour or record (e.g., revenue).
  - `coffee_name`: Name of a specific coffee product (where applicable).
  - `Time_of_Day`: Categorical label (e.g., Morning, Afternoon, Evening).
  - `Weekday`: Day of the week (e.g., Mon, Tue).
  - `Month_name`: Month name associated with the record.
  - `Weekdaysort`, `Monthsort`: Numeric ordering fields for plotting or grouping.
  - `Date`, `Time`: Additional temporal fields that may be used for profiling or extended modeling.

**Intended use in the project**

This dataset provides **contextual and temporal information** about coffee-shop operations:

- Hourly patterns of revenue (`money`) and potentially product-specific behavior.
- Day-of-week and month-level context for sales.
- Time-of-day categorizations that can be used to group or label transactions (Morning vs Afternoon vs Evening).

Because the Coffee Sales dataset does not carry detailed time-of-day context beyond raw `transaction_time`, the Coffee Shop dataset is used to **build an hourly profile** that can be joined to transaction-level data. This enriches each transaction with additional time-of-day attributes (average hourly money, typical Time_of_Day label, etc.).

**Ethical and legal constraints**

- As with the Coffee Sales dataset, the Coffee Shop dataset is public, used for educational purposes, and contains no personal identifiers.
- The data are not redistributed directly; they are accessed via Kaggle and reproduced locally via script.
- Licenses and terms of use are respected by pointing users to Kaggle for original downloads and by avoiding inclusion of raw Kaggle files in version control.

---

## Data quality

Data quality was assessed and addressed in multiple steps using both notebooks and scripts.

### Initial profiling

The notebook `notebooks/01_profiling.ipynb` performs initial data profiling on both datasets:

- **Schema inspection**:
  - Uses `DataFrame.info()` to check column names, data types, and non-null counts.
- **Missing values**:
  - Computes `isna().sum()` per column to identify missing or incomplete fields.
- **Basic distributions**:
  - For categorical variables (e.g., `store_location`, `product_category`), value counts are inspected.
  - For numeric variables (e.g., `transaction_qty`, `unit_price`, `money`), summary statistics are examined (`describe()`).

The notebook saves preliminary cleaned copies of the datasets to:

- `data/processed/coffee_sales_clean.csv`
- `data/processed/coffee_shop_clean.csv`

These form the starting point for integration and subsequent EDA.

### Cleaning steps (conceptual)

While the raw cleaning logic can be implemented either in notebooks or in a dedicated `scripts/clean_data.py` script, the key **cleaning actions** are:

- **Type conversion**:
  - Parse `transaction_date` and `transaction_time` into datetime-compatible formats.
  - Ensure `transaction_qty`, `unit_price`, and `money` are numeric.
- **Handling missing values**:
  - For critical identifiers (e.g., `transaction_id`), rows with missing IDs would be candidates for removal.
  - For non-critical descriptive fields (e.g., `product_detail`), missing values may be left as-is or filled with a placeholder.
  - For numeric fields like `money`, rows with invalid or missing values can be dropped or imputed, depending on frequency and impact.
- **Duplicate checking**:
  - Check for duplicate `transaction_id` rows and remove exact duplicates if they appear.
- **Standardizing categorical values**:
  - Normalize text case and categories for fields like `store_location`, `product_category`, or `Time_of_Day` (e.g., ensuring “Morning” is consistently spelled).

The goal of cleaning is not to transform the datasets extensively but to ensure that:

- Joins are reliable (no unexpected type mismatches).
- Time-based fields are usable for integration and grouping.
- Numeric analyses (sums, averages) do not suffer from type or missing-value issues.

### Quality findings (high level)

From the profiling:

- The Coffee Sales dataset is generally well-structured with consistent transaction identifiers and a reasonable amount of missing data, mostly in non-critical descriptive fields.
- The Coffee Shop dataset contains some redundancy across time-of-day and date fields, which is managed by aggregating and deduplicating by `hour_of_day` for integration.
- There are some minor parsing warnings for dates/times (due to varied string formats), but these are handled gracefully by `pandas.to_datetime` with `errors="coerce"`, and resulting `NaT` values can be monitored.

---

## Data collection and acquisition

To ensure reproducible data acquisition and integrity, the project uses a dedicated script and checksum files.

### Programmatic acquisition

- **Script**: `scripts/get_data.py`
- **Purpose**:
  - Download the Coffee Sales and Coffee Shop datasets from Kaggle using the Kaggle API.
  - Store the files under `data/raw/`.
  - Optionally compute and verify SHA-256 checksums for integrity.

**Key behaviors**:

1. Uses the Kaggle CLI (`kaggle datasets download ...`) to fetch:
   - `ahmedabbas757/coffee-sales`
   - `jawad3664/coffee-shop`
2. Unzips the downloaded archives into `data/raw/`, producing:
   - `data/raw/coffee_sales.csv`
   - `data/raw/coffee_shop.csv`
3. Ensures that raw CSVs are **not committed** to Git; instead, they are recreated on demand.

### Integrity checking with SHA-256

- **Checksum file**: `data/checksums.sha256`
- **Commands**:
  - `python scripts/get_data.py write-checks`
    - Computes SHA-256 hashes of `coffee_sales.csv` and `coffee_shop.csv` and writes them to `data/checksums.sha256`.
  - `python scripts/get_data.py verify`
    - Recomputes hashes and compares them against `data/checksums.sha256`, printing `[OK]` for matches and `[FAIL]` for mismatches or missing files.

This ensures that:

- Users who clone the repository can verify they are using the **exact same raw inputs** as the original analysis.
- Any accidental corruption or modification of the raw CSVs can be detected.

### Documentation of acquisition steps

The file `data/README.md` documents:

- How to set up Kaggle API credentials (either via `KAGGLE_API_TOKEN` or `kaggle.json`).
- How to create and activate a Python virtual environment.
- The exact commands to:
  - Download the data: `python scripts/get_data.py download`
  - Compute checksums: `python scripts/get_data.py write-checks`
  - Verify integrity: `python scripts/get_data.py verify`

This documentation ensures that another student, TA, or instructor can reproduce the data acquisition step independently.

---

## Storage and organization

The project uses a **filesystem-based, tabular storage strategy** instead of a relational database. All data are stored as CSV files in a structured folder layout inside the Git repository.

### Directory layout

```text
.
├── data/
│   ├── raw/          # Raw input data downloaded from Kaggle (CSV, zip, xlsx)
│   ├── processed/    # Cleaned, integrated, and derived CSV files
│   └── README.md     # Instructions for data acquisition and integrity checks
├── figures/          # Output plots and visualizations used in the report
├── notebooks/        # Jupyter notebooks for profiling, integration, and EDA
├── scripts/          # Python scripts for acquisition, cleaning, integration, etc.
├── ProjectPlan.md    # Milestone 2 project plan
├── StatusReport.md   # Milestone 3 status report
└── README.md         # Final project report (this file)