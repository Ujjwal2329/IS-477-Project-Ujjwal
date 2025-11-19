# Project Plan

## 1. Overview
This project analyzes coffee sales and customer behavior across multiple coffee shops to uncover patterns that influence revenue, product mix, and customer preferences.  
The goal is to build an integrated data pipeline that collects, cleans, merges, and analyzes data from two distinct datasets — **Coffee Sales** and **Coffee Shop** — to provide insights into sales trends, product performance, and location-based demand.  

Key outcomes will include:
- Identifying top-selling items and time-of-day trends.
- Understanding which store or city segments contribute most to total sales.
- Demonstrating a complete, reproducible data lifecycle: collection, storage, integration, cleaning, enrichment, analysis, and visualization.

---

## 2. Research Questions
1. Which coffee products generate the highest sales volume and profit margins across locations?  
2. How do customer preferences (drink type, size, add-ons) vary by time and location?  
3. Can integrated sales and shop-level data reveal which operational factors (location, staff count, store size) drive higher daily sales?

---

## 3. Team
**Solo Project — Ujjwal Agarwal**  
- **Role:** Project Lead / Data Engineer / Analyst  
- **Responsibilities:**  
  - Acquire and document both datasets.  
  - Design data-storage structure.  
  - Perform data cleaning and integration using Python (Pandas).  
  - Conduct exploratory data analysis and create visual summaries.  
  - Automate workflow for reproducibility.  
  - Prepare all Markdown deliverables and GitHub releases.

---

## 4. Datasets

### Dataset 1 – Coffee Sales  
**Source:** [Kaggle – Coffee Sales Dataset](https://www.kaggle.com/datasets/ahmedabbas757/coffee-sales)  
**Description:** Transaction-level data of coffee orders, including product type, quantity, price, order date/time, and total sales.  
**Format:** CSV  
**Purpose:** Provides granular sales details per transaction to analyze demand, seasonality, and pricing trends.  

### Dataset 2 – Coffee Shop Dataset  
**Source:** [Kaggle – Coffee Shop Dataset](https://www.kaggle.com/datasets/jawad3664/coffee-shop)  
**Description:** Shop-level and product-level information such as store ID, city, menu items, unit costs, and possibly staffing or rating data.  
**Format:** CSV  
**Purpose:** Offers contextual and operational attributes that can be joined with sales records to compare performance across shops.  

**Integration Plan:**  
Both datasets share product and store identifiers (e.g., “Store ID” or “Product Name”).  
They will be integrated in Python using Pandas `merge()` to create a unified table that links transaction data with store and product attributes.

---

## 5. Timeline

| Phase | Task | Deliverable | Responsible | Target Date |
|-------|------|--------------|--------------|--------------|
| Week 1–2 | Data acquisition, license/terms verification | Downloaded & documented raw data | Ujjwal | Oct 1 – Oct 7 |
| Week 3–4 | Data profiling, cleaning, schema design | Cleaned CSVs & Jupyter notebook | Ujjwal | Oct 14 |
| Week 5–6 | Data integration, feature creation | Integrated dataset | Ujjwal | Oct 28 |
| Week 7–8 | Exploratory analysis, visualization | EDA notebook & charts | Ujjwal | Nov 10 |
| Week 9–10 | Workflow automation & documentation | Python script + Makefile | Ujjwal | Nov 25 |
| Week 11–12 | Final polish & GitHub release | Final repo + README + report | Ujjwal | Dec 10 |

---

## 6. Constraints
- Kaggle datasets are public but must respect their **licenses** and **terms of use**.  
- Both datasets are static CSVs — no live API, limiting real-time updating.  
- Storage limited to local CSV files in GitHub due to repository size caps (≤ 100 MB).  
- Computations and plots will be executed in Jupyter; large intermediate files excluded from version control.

---

## 7. Gaps / Future Input Needed
- Confirm exact matching keys between the two datasets once inspected.  
- Define a consistent currency/price unit if differences exist.  
- Decide on final analytical KPIs (e.g., revenue per store per day, product margin ratio).  
- Identify whether additional open datasets (weather, location demographics) could enhance analysis.  

---

## 8. Relation to Course Modules
- **Data Lifecycle:** Demonstrates the full cycle from acquisition to reporting.  
- **Ethical Handling:** All data publicly available under Kaggle license, anonymized, and used for educational analysis only.  
- **Data Integration:** Combines heterogeneous CSVs with different schemas.  
- **Data Quality & Cleaning:** Missing-value checks, normalization, outlier handling.  
- **Workflow Automation:** Implemented using Python scripts and documented notebooks.  
- **Reproducibility & Provenance:** Versioned code and data through GitHub commits and tags.

---

## 9. References
- Kaggle (2024). “Coffee Sales Dataset.” https://www.kaggle.com/datasets/ahmedabbas757/coffee-sales  
- Kaggle (2024). “Coffee Shop Dataset.” https://www.kaggle.com/datasets/jawad3664/coffee-shop  
