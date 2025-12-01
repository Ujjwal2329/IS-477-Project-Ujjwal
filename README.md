# IS-477-Project
Course project for IS 477
# Coffee Sales & Shop Integration Project

## Contributors

- Ujjwal Agarwal

---

## Summary

This project analyzes coffee sales and customer behavior across multiple coffee shops by integrating a transaction-level **Coffee Sales** dataset with a shop-level **Coffee Shop** dataset. The main goal is to build a **reproducible end-to-end data pipeline** that covers acquisition, storage, cleaning, integration, analysis, and visualization.

The analysis focuses on understanding which products sell best, how sales vary by time of day and location, and how shop-level characteristics relate to revenue. The project follows the data lifecycle discussed in class: data are acquired programmatically from Kaggle, stored in a structured filesystem layout, cleaned and integrated using Python, analyzed via notebooks and scripts, and documented in this report.

All work is done as an individual project. The code, data workflow, and documentation are designed so that another person can reproduce the results from scratch, starting from the public Kaggle datasets.

---

## Research questions

The project is guided by the following research questions:

1. **Which coffee products generate the highest sales volume and/or revenue across locations?**
2. **How do customer preferences (e.g., drink type, size, add-ons) vary by time of day and store/location?**
3. **Can integrated sales and shop-level data reveal which operational factors (e.g., location, product mix) are associated with higher daily sales?**

---

## Project structure and storage strategy

This project uses a **filesystem-based, tabular storage strategy** instead of a
relational database. All data are stored as CSV files in a structured folder
layout inside the Git repository.

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