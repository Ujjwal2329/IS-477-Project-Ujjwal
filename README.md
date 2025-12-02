# Coffee Shop Sales & Behavior Analysis

## Contributors

- Ujjwal Agarwal (solo project)

---

## Summary

This project analyzes coffee sales and customer behavior across multiple coffee shop locations using two publicly available datasets from Kaggle. The goal is to build a **reproducible, end-to-end data pipeline** that starts from raw data acquisition and proceeds through cleaning, integration, analysis, and visualization. The final outputs include both numeric summaries and figures that answer concrete business questions about product performance, time-of-day patterns, and store-level differences in revenue.

The first dataset, *Coffee Sales*, contains transaction-level data from three coffee shops over several months. Each row corresponds to a single transaction and records the date and time, quantity sold, store information, unit price, and product description fields. This dataset supports detailed analysis of demand patterns, including which products are most popular, which times of day are busiest, and how pricing interacts with volume.

The second dataset, *Coffee Shop*, provides a complementary view of the business at an hourly level. It includes columns such as `hour_of_day`, `Time_of_Day` (e.g., Morning, Afternoon, Evening), `Weekday`, `Month_name`, and `money`, which represent typical or average monetary activity per hour. While the first dataset is strictly transactional, this second dataset captures a higher-level time-of-day profile of the coffee shop environment.

The project is guided by three research questions:

1. **Which coffee products generate the highest sales volume and/or revenue across locations?**  
2. **How do customer preferences (e.g., drink type, size, add-ons) vary by time of day and store/location?**  
3. **Can integrated sales and shop-level data reveal which operational factors (e.g., location, product mix) are associated with higher daily sales?**

To address these questions, I implemented a complete data lifecycle:

- **Data collection and acquisition:** Raw data are downloaded programmatically from Kaggle using the `kaggle` CLI via the script `scripts/get_data.py`. Integrity is checked using SHA-256 checksums recorded in `data/checksums.sha256`.
- **Storage and organization:** The project uses a filesystem-based, tabular storage strategy with a clear separation between `data/raw/` and `data/processed/`, plus dedicated folders for notebooks, scripts, and figures.
- **Extraction, cleaning, and integration:** Cleaning logic (type conversions, duplicate removal, handling of invalid values) is implemented in `scripts/clean_data.py` and documented in `notebooks/03_profiling.ipynb`. The integrated dataset is created by `scripts/integrate_data.py` and documented in `notebooks/02_integration.ipynb`.
- **Analysis and visualization:** Key analysis and visualizations are implemented in `notebooks/04_analysis_and_visualization.ipynb` and automated via `scripts/make_figures.py`.
- **Workflow automation and provenance:** A `Snakefile` defines a Snakemake workflow that automates the entire pipeline from data download through figure generation, and `scripts/run_all.py` provides a simple “run everything” entry point.
- **Reproducibility and transparency:** All steps are scripted, version-controlled in Git, and documented in Markdown. The repository is structured so that a new user can start from raw data and reproduce all processed outputs and figures.
- **Metadata and documentation:** The `data/README.md` file documents the datasets, licenses/terms of use, and acquisition steps. An example OpenRefine JSON recipe is provided for demonstration of external data cleaning.

Overall, the project demonstrates how a relatively small but rich business dataset can be turned into actionable insights using modern data engineering and data science practices. It emphasizes not only the analysis itself, but also ethical data use, transparent documentation, and repeatable workflows.

---

## Data profile

### Datasets and sources

This project uses two datasets from Kaggle:

1. **Coffee Sales dataset**  
   - Kaggle ID: `ahmedabbas757/coffee-sales`  
   - Local path (raw): `data/raw/coffee_sales.csv`  
   - Description: Transaction-level coffee shop sales from three locations over several months of 2023.  
   - Key columns (examples):  
     - `transaction_id`: Unique ID for each transaction  
     - `transaction_date`: Date of the transaction (MM/DD/YY)  
     - `transaction_time`: Time of the transaction (HH:MM:SS)  
     - `transaction_qty`: Quantity of items sold  
     - `store_id`, `store_location`: Shop identifier and city/neighborhood  
     - `product_id`: Product identifier  
     - `unit_price`: Price per unit sold  
     - `product_category`, `product_type`, `product_detail`: Product descriptors  

2. **Coffee Shop dataset**  
   - Kaggle ID: `jawad3664/coffee-shop`  
   - Local path (raw): `data/raw/coffee_shop.csv`  
   - Description: Hourly-level coffee shop data with time-of-day and temporal metadata.  
   - Key columns (examples):  
     - `hour_of_day`: Hour index (0–23)  
     - `cash_type`: Payment type or category  
     - `money`: Monetary measure per hour (e.g., typical revenue or cash flow)  
     - `coffee_name`: Name of a coffee drink (depending on row type)  
     - `Time_of_Day`: Categorical label such as Morning, Afternoon, Evening, Night  
     - `Weekday`, `Month_name`: Temporal descriptors  

Both datasets are **publicly available** on Kaggle and used here strictly for **educational, non-commercial** purposes. All usage complies with Kaggle’s terms of service and any dataset-specific license or attribution guidelines; the original authors retain any rights associated with the data.

### Data access and formats

Data are downloaded using the `kaggle` CLI via the script:

- `scripts/get_data.py`

This script downloads the corresponding `.zip` archives into `data/raw/` and extracts them into CSV files. The raw CSV files are **not** committed to the Git repository. Instead, a checksum file:

- `data/checksums.sha256`

provides SHA-256 hashes for each raw input file so that users (and graders) can verify the integrity of downloads.

All processing steps operate on **CSV** files (tabular, comma-separated). There is no live API; all data acquisition is batch-oriented. The integrated dataset:

- `data/processed/coffee_integrated.csv`

combines transactional details with time-of-day context derived from the shop dataset.

### Ethical, legal, and policy considerations

Although the datasets do not contain personally identifiable information, basic ethical and legal issues were still considered:

- **Consent and privacy:** Data are synthetic or anonymized training datasets intended for public use. No attempt is made to deanonymize or link them to real individuals or organizations.
- **Licensing and terms of use:** Before using each dataset, the Kaggle dataset page was reviewed for licensing terms, usage restrictions, and required attribution. This project respects those constraints and cites the dataset authors in the References section.
- **Redistribution:** To avoid any ambiguity about redistribution of original raw files, this repository **does not** include the raw Kaggle CSVs. Instead, instructions and scripts are provided so others can obtain them directly from Kaggle and verify them using checksums.
- **Educational use only:** Analyses and recommendations are treated as illustrative; they are not deployed in production or used to make real business decisions.

### Metadata and internal documentation

Metadata and data documentation are organized as follows:

- `data/README.md`  
  Describes each dataset, its Kaggle ID, acquisition steps using `kaggle`, and how to verify checksums.
- `openrefine/coffee_sales_refine.json`  
  Example OpenRefine operation history (JSON “recipe”) demonstrating how a column such as `store_location` could be cleaned (whitespace trimming) using an external tool.
- Source code and notebooks include descriptive comments and Markdown cells explaining the transformations applied at each step of the workflow.

Combined, these materials support the **understandability, discovery, and reuse** of the curated data within this project.

---

## Data quality

Data quality was assessed in several stages using both scripts and notebooks:

- **Scripts:**
  - `scripts/clean_data.py` – main cleaning logic for raw CSVs.
- **Notebooks:**
  - `notebooks/03_profiling.ipynb` – data quality profiling and documentation.

### Quality dimensions and checks

The following data quality dimensions were evaluated:

1. **Completeness**  
   - Missing values were inspected using `isna().sum()` for both datasets.
   - For the sales data, particular attention was given to `transaction_qty` and `unit_price` because they are required for computing revenue.
   - For the shop data, `hour_of_day` and `money` were treated as critical fields.

2. **Uniqueness**  
   - The sales dataset uses `transaction_id` as a primary identifier. Duplicate checks were performed using `.duplicated(subset=["transaction_id"])`.
   - For the shop dataset, the grain is hourly rather than transactional. Depending on the interpretation of the data, uniqueness by `hour_of_day` or by composite keys (e.g., `hour_of_day`, `Weekday`) can be inspected.

3. **Validity and range checks**  
   - Numeric fields (e.g., `transaction_qty`, `unit_price`, `hour_of_day`, `money`) were converted to numeric types using `pd.to_numeric(..., errors="coerce")`.
   - For `hour_of_day`, valid values are restricted to the range 0–23. Any rows outside this range were removed.
   - Non-positive or missing values for `transaction_qty` or `unit_price` were considered invalid for the purpose of revenue analysis.

4. **Consistency**  
   - Categorical values such as `product_category`, `store_location`, and `Time_of_Day` were inspected using `value_counts()`.  
   - Basic checks confirmed that locations and time-of-day labels are consistent across rows (e.g., no obviously mistyped categories).

5. **Integrity across transformations**  
   - After each stage (cleaning, integration), dataset shapes and key column summaries were printed and examined (e.g., number of rows, number of columns, unique values in key fields).
   - The integrated dataset was validated to ensure that key derived fields (like `revenue` and `hour_of_day`) behaved as expected.

### Cleaning methods and decisions

The main cleaning logic is implemented in `scripts/clean_data.py` and documented in `notebooks/03_profiling.ipynb`. Key decisions include:

#### Sales data (`coffee_sales_clean.csv`)

- **Whitespace trimming:**  
  All string columns are stripped of leading and trailing whitespace to avoid artificially distinct categories (e.g., `"Hell's Kitchen"` vs `"Hell's Kitchen "`).
- **Duplicate removal:**  
  Duplicate rows based on `transaction_id` are dropped, ensuring that each transaction is counted once in aggregations.
- **Type conversion:**  
  - `transaction_qty` and `unit_price` are converted to numeric types.
- **Invalid and missing values:**  
  Rows with missing or non-positive `transaction_qty` or `unit_price` are removed. These records would otherwise lead to nonsensical or misleading revenue calculations.
- **Result:**  
  A cleaned sales table where each row represents a valid transaction with reliable quantity and price information, suitable for computing revenue and aggregated metrics.

#### Shop data (`coffee_shop_clean.csv`)

- **Whitespace trimming:**  
  String fields (such as `Time_of_Day` and `Weekday`) are stripped of whitespace.
- **Type conversion and range checks:**  
  - `hour_of_day` is converted to numeric and restricted to 0–23; out-of-range rows are dropped.
  - `money` is converted to numeric; rows with missing `money` are removed so that hourly averages and totals are meaningful.
- **Result:**  
  A cleaned hourly profile of the shop, with consistent time-of-day labeling and valid `hour_of_day` and `money` fields that can be combined with transactional data.

### Documentation of quality results

The notebook `notebooks/03_profiling.ipynb` records:

- Schema (`info()` outputs) for both datasets.
- Missing value counts before and after cleaning.
- Summary statistics (`describe()`) for key numeric fields.
- Simple outlier checks for non-positive quantities/prices and invalid hours.
- Short textual summaries of the chosen cleaning decisions.

These results are summarized and interpreted in this README under **Data quality** and referenced in the **Findings** section where relevant.

---

## Findings

The main findings are derived from analysis in:

- `notebooks/04_analysis_and_visualization.ipynb`
- Figures generated by `scripts/make_figures.py` and saved in `figures/`

### 1. Top products by revenue

Using the integrated dataset, total quantity and total revenue were aggregated by product descriptor (e.g., `product_type` or `product_category`). The plot:

- `figures/top_products_by_revenue.png`

shows the top 10 product types by total revenue across all stores. In general:

- Coffee drinks and tea products account for a large share of total revenue.
- Bakery and chocolate items also contribute meaningfully, but typically rank below core beverage categories.
- There is a clear long-tail effect: a small number of product types produce a large fraction of revenue.

These results directly address the first research question by highlighting which product categories are most valuable to the business.

### 2. Time-of-day patterns

The integrated dataset includes a derived `revenue` column as well as `hour_of_day` and `Time_of_Day` labels merged from the shop dataset. Two key figures:

- `figures/revenue_by_hour_of_day.png`
- `figures/revenue_by_time_of_day.png`

show that:

- Revenue is strongly concentrated in **morning hours**, with a pronounced peak during typical commuting/breakfast times (roughly 7–10 AM).
- Afternoon hours maintain moderate activity, while very early and very late hours generate comparatively little revenue.
- When grouped by `Time_of_Day` categories, “Morning” clearly dominates total revenue, followed by “Afternoon”, with “Evening” and “Night” contributing less.

This supports the second research question by demonstrating how customer behavior (and demand for coffee products) varies with time of day.

### 3. Store-level performance

Aggregating total revenue by `store_location` produces:

- `figures/top_stores_by_revenue.png`

The three primary locations in the dataset are:

- Astoria  
- Hell’s Kitchen  
- Lower Manhattan  

The analysis shows that:

- All three stores generate substantial revenue, with relatively similar magnitudes.
- One location (often Hell’s Kitchen in prior analyses of this dataset) tends to edge out the others in total revenue, suggesting slightly higher foot traffic or larger average order values.
- These differences, combined with product mix and time-of-day patterns, can inform staffing decisions, local marketing campaigns, or promotions tailored to specific neighborhoods.

### 4. High-level implications

Taken together, the results suggest that:

- **Product strategy:** Coffee and tea products should remain the focus of the offering, with bakery and chocolate items positioned as complementary upsell options.
- **Time-based promotions:** Morning hours are crucial; any operational issues at this time (e.g., staffing bottlenecks) could significantly impact revenue. Promotions aimed at afternoon or early evening could help smooth overall demand.
- **Location strategy:** Revenue differences across locations indicate potential for targeted interventions—such as local advertising or menu tweaks—while recognizing that the three shops share broadly similar patterns.

These findings are illustrative of how even simple aggregated metrics can drive meaningful decisions in a coffee shop business.

---

## Future work

Several extensions and enhancements could deepen the analysis and improve the robustness of the pipeline:

1. **Richer feature engineering**  
   - Add derived temporal features such as:
     - `month`, `week_of_year`, `is_weekend`, or holiday flags.
     - Rolling or moving averages of daily revenue to identify trends and seasonality.
   - Incorporate weather or local event data to see how external conditions affect coffee demand.

2. **More sophisticated integration**  
   - Currently, the integration focuses on aligning transactions with hourly profiles via `hour_of_day` and related time-of-day fields.
   - A more advanced schema could separate fact and dimension tables (e.g., a star schema with `FactTransactions`, `DimProduct`, `DimStore`, `DimTime`) and use SQL/SQLite as the main analytical backend.
   - Additional data sources (e.g., demographics or neighborhood income data) could be joined on store location to better explain store-level differences.

3. **Predictive modeling**  
   - Build models to predict hourly or daily revenue based on:
     - Product mix
     - Time of day and day of week
     - Store location
   - Techniques could include linear regression, tree-based models, or time-series forecasting.
   - This would move the project beyond descriptive analytics into predictive and prescriptive analytics.

4. **Interactive dashboards**  
   - Create an interactive dashboard (e.g., in Streamlit, Dash, or a BI tool) to explore:
     - Product performance by location
     - Time-of-day patterns for each store
     - Sensitivity to pricing changes
   - This would make the insights more accessible to non-technical stakeholders.

5. **Stronger FAIR and archival practices**  
   - Deposit a fixed snapshot of the repository (code, notebooks, and non-Kaggle-restricted artifacts) into an archival repository such as Zenodo or OSF.
   - Mint a DOI and include machine-readable metadata (e.g., DataCite or schema.org) for the project.
   - Provide a more formal data dictionary describing each variable, its type, and domain.

6. **Expanded data quality tooling**  
   - Integrate a data quality library such as Great Expectations or Pandera to automatically validate assumptions (e.g., ranges, uniqueness) as part of the pipeline.
   - Extend the OpenRefine JSON recipes to cover more cleaning operations and document these as an alternative GUI-based approach for less technical users.

Together, these enhancements would make the project more realistic as a data product, more informative for decision-makers, and more aligned with long-term research data management best practices.

---

## Workflow automation and provenance

The project offers two primary ways to run the **end-to-end workflow** from raw data acquisition through figure generation:

1. A **Snakemake workflow** defined in the `Snakefile`.
2. A simple **Run All script**: `scripts/run_all.py`.

### Snakemake workflow

The `Snakefile` at the project root defines the following rules:

1. **`get_data`**  
   - Calls `python scripts/get_data.py download`  
   - Downloads Kaggle datasets into `data/raw/`:
     - `data/raw/coffee_sales.csv`
     - `data/raw/coffee_shop.csv`

2. **`clean_data`**  
   - Calls `python scripts/clean_data.py`  
   - Produces cleaned files:
     - `data/processed/coffee_sales_clean.csv`
     - `data/processed/coffee_shop_clean.csv`

3. **`integrate_data`**  
   - Calls `python scripts/integrate_data.py`  
   - Produces:
     - `data/processed/coffee_integrated.csv`

4. **`make_figures`**  
   - Calls `python scripts/make_figures.py`  
   - Produces figures in `figures/`:
     - `top_products_by_revenue.png`
     - `revenue_by_hour_of_day.png`
     - `revenue_by_time_of_day.png`
     - `top_stores_by_revenue.png`

Running:

```bash
snakemake -j1

## Reproducing, Reproducibility & Metadata

This section provides a complete, step-by-step description of how someone else can reproduce the workflow and analysis, and how the data and metadata are organized to support discovery, understandability, and reuse.

### 1. Prerequisites

1. **Clone the repository**

   ```bash
   git clone <YOUR_REPO_URL>.git
   cd IS-477-Project-Ujjwal
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install software dependencies**

   Dependencies are specified in `requirements.txt`. Install them with:

   ```bash
   pip install -r requirements.txt
   ```

   If needed, you can regenerate a full environment snapshot (for example, into `env/requirements-freeze.txt`) using:

   ```bash
   pip freeze > env/requirements-freeze.txt
   ```

   This provides a precise record of packages and versions used for the analysis.

4. **Configure the Kaggle API**

   To obtain the raw datasets programmatically, configure the Kaggle CLI as described in `data/README.md`:

   - Obtain an API token from Kaggle (Account → Settings → API).
   - Either:
     - Set the environment variable:

       ```bash
       export KAGGLE_API_TOKEN='KGAT_...your_token_here...'
       ```

       **or**

     - Use the legacy `kaggle.json` method, placing the file in:
       - macOS/Linux: `~/.kaggle/kaggle.json`
       - Windows: `C:\Users\<USER>\.kaggle\kaggle.json`

   - You can test your setup with:

     ```bash
     kaggle -v
     ```

   The script `scripts/get_data.py` uses the Kaggle CLI under the hood; if `kaggle` is not configured, data acquisition will fail.

### 2. Sequence of steps to reproduce the workflow

You can reproduce the entire workflow from raw data to figures in two ways: with **Snakemake** (full provenance) or with a simpler **Run All script**.

#### Option A – Snakemake workflow (full provenance)

The `Snakefile` at the project root defines the following pipeline:

1. **Data acquisition**

   ```bash
   python scripts/get_data.py download
   ```

   This downloads the two Kaggle datasets:

   - `ahmedabbas757/coffee-sales`
   - `jawad3664/coffee-shop`

   and writes the raw CSVs into `data/raw/`:

   - `data/raw/coffee_sales.csv`
   - `data/raw/coffee_shop.csv`

   SHA-256 checksums for the raw files are stored in `data/checksums.sha256`. These can be verified manually using standard tools (e.g., `shasum -a 256`) to ensure the downloaded files match the expected content.

2. **Data cleaning**

   ```bash
   python scripts/clean_data.py
   ```

   This script:

   - Trims whitespace from string columns.
   - Converts key numeric columns (e.g., `transaction_qty`, `unit_price`, `hour_of_day`, `money`) to numeric types.
   - Drops rows with invalid or missing values in critical fields (e.g., non-positive quantities or prices; invalid `hour_of_day`).
   - Removes duplicate transactions based on `transaction_id`.

   Outputs:

   - `data/processed/coffee_sales_clean.csv`
   - `data/processed/coffee_shop_clean.csv`

3. **Data integration**

   ```bash
   python scripts/integrate_data.py
   ```

   This script:

   - Loads the cleaned datasets from `data/processed/`.
   - Parses transaction date/time and extracts `hour_of_day`.
   - Merges the hourly profile from the coffee shop dataset into the sales data based on `hour_of_day`, attaching `Time_of_Day`, `Weekday`, and `Month_name`.
   - Adds a `revenue` column (`transaction_qty * unit_price`), if not already present.

   Output:

   - `data/processed/coffee_integrated.csv`

4. **Analysis and visualization**

   ```bash
   python scripts/make_figures.py
   ```

   This script:

   - Loads `data/processed/coffee_integrated.csv`.
   - Computes product-, time-, and store-level aggregations.
   - Generates and saves figures in `figures/`:
     - `figures/top_products_by_revenue.png`
     - `figures/revenue_by_hour_of_day.png`
     - `figures/revenue_by_time_of_day.png`
     - `figures/top_stores_by_revenue.png`

To run the full Snakemake workflow in one command:

```bash
snakemake -j1
```

Snakemake automatically determines which steps need to be re-run based on timestamps and rule definitions, providing a clear provenance chain from raw data to final outputs.

#### Option B – Run All script (simple entry point)

Alternatively, you can reproduce the entire workflow with a single command:

```bash
python scripts/run_all.py
```

This script sequentially calls the same four scripts listed above:

1. `scripts/get_data.py download`
2. `scripts/clean_data.py`
3. `scripts/integrate_data.py`
4. `scripts/make_figures.py`

This is a simpler entry point for users who do not wish to install Snakemake, while still providing a fully automated pipeline.

### 3. Inspecting the analysis and results

Once the workflow has completed:

- Cleaned data are in `data/processed/`:
  - `coffee_sales_clean.csv`
  - `coffee_shop_clean.csv`
  - `coffee_integrated.csv`
- Figures are in `figures/`:
  - `top_products_by_revenue.png`
  - `revenue_by_hour_of_day.png`
  - `revenue_by_time_of_day.png`
  - `top_stores_by_revenue.png`

Notebooks documenting the steps:

- **Data acquisition & context:**
  - `notebooks/00_data_acquisition.ipynb`
- **Storage & organization overview:**
  - `notebooks/01_storage_and_organization.ipynb`
- **Integration logic and sanity checks:**
  - `notebooks/02_integration.ipynb`
- **Data quality assessment & cleaning:**
  - `notebooks/03_profiling.ipynb`
- **Analysis & visualization:**
  - `notebooks/04_analysis_and_visualization.ipynb`

You can open these notebooks in Jupyter, VS Code, or any compatible environment to inspect intermediate tables, additional plots, and narrative descriptions of each step.

### 4. Box archive and Git ignore rules

Per the course requirements, a copy of the **output data** (and optionally the input data if not retrieved programmatically) must be uploaded to Box.

- A shareable Box folder link should be added here before submission:

  > **Box folder URL:** https://uofi.box.com/s/hdb1q131221vztvsr9w7i4edfmobqp4f 

After downloading the Box archive:

- Place the CSV files from `data/processed/` into the local `data/processed/` folder in this repository.
- Place the PNG files from `figures/` into the local `figures/` folder.

The directory structure should look like:

data/processed/coffee_integrated.csv  
figures/top_products_by_revenue.png  
... etc.

After downloading the Box archive, place the contents into the appropriate directories in the project structure, for example:

- `data/processed/`  ← downloaded processed CSVs  
- `figures/`         ← downloaded figure PNGs  

If you choose to keep the exact Box download structure (e.g., `data/box_archive/`), ensure that directory is added to `.gitignore`, e.g.:

```gitignore
# Box archive copy
data/box_archive/
```

This prevents large or redundant Box-based data copies from being committed to Git while still making them available locally.

### 5. Metadata and data documentation

To support discovery, understandability, and reuse, the project includes:

- **Dataset documentation**

  - `data/README.md`  
    Describes each dataset, its Kaggle ID, how to acquire it via the Kaggle API and `scripts/get_data.py`, and how to verify file integrity using `data/checksums.sha256`.

- **Data dictionary / codebook**

  - A data dictionary file (e.g., `data/data_dictionary.md`) can be used to summarize:
    - Column names
    - Data types
    - Allowed values or typical ranges
    - Brief descriptions of each variable

  This helps readers quickly understand the meaning and structure of the curated data.

- **OpenRefine operation history**

  - `openrefine/coffee_sales_refine.json`  
    Provides an example JSON “recipe” that documents how a tool like OpenRefine could be used to perform additional cleaning (e.g., trimming whitespace in `store_location`). This demonstrates how GUI-driven transformations can also be captured in a machine-readable, reproducible form.

- **Workflow metadata**

  - The `Snakefile` encodes the dependency structure between raw inputs, intermediate files, and final outputs.
  - `scripts/run_all.py` encapsulates the canonical execution order, serving as a minimal but explicit description of the pipeline.

- **Project-level descriptive metadata**

  The main `README.md` (this file) acts as project-level descriptive metadata, similar in spirit to standards like DataCite or schema.org by providing:

  - A human-readable title and summary
  - Description of datasets, methods, and workflows
  - Information on how to obtain and reuse the data and code
  - References and licensing notes

### 6. Licenses and reuse

- **Data licenses**

  The raw data are obtained from Kaggle:

  - `ahmedabbas757/coffee-sales`
  - `jawad3664/coffee-shop`

  These datasets are subject to the licenses and terms of use specified on their respective Kaggle pages. This project does **not** redistribute the original raw CSVs; instead, it provides scripts and instructions for others to obtain them directly from Kaggle.

- **Code license**

  The analysis scripts, notebooks, and workflow definitions in this repository (excluding external libraries and Kaggle data) can be licensed under a permissive open-source license (e.g., MIT), allowing others to reuse and adapt the code while respecting attribution requirements as specified in the chosen license.

By following the steps above and using the provided scripts, notebooks, and documentation, another user can recreate the entire analysis—from raw data acquisition through integration, cleaning, and visualization—thereby satisfying the course goals for **reproducibility**, **transparency**, and **metadata-rich documentation**.