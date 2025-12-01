# IS-477-Project
Course project for IS 477
# Data directory

This folder contains all data used in the project.

- `raw/` – **raw input data** downloaded from Kaggle using `scripts/get_data.py`
- `processed/` – **cleaned / integrated data** produced by notebooks or scripts
- `checksums.sha256` – SHA-256 hashes for the raw input files

Raw data files are **not** stored in the Git repo; they are recreated
programmatically.

---

## Datasets

This project uses two public Kaggle datasets:

1. **Coffee Sales dataset**  
   Kaggle ID: `ahmedabbas757/coffee-sales`  
   Saved locally as: `data/raw/coffee_sales.csv`

2. **Coffee Shop dataset**  
   Kaggle ID: `jawad3664/coffee-shop`  
   Saved locally as: `data/raw/coffee_shop.csv`

The script `scripts/get_data.py` downloads both and unzips them into
`data/raw/`.

---

## Prerequisites: Kaggle API setup

1. Create a Kaggle account and go to **Account → Settings → API**.
2. Either:

   - **Recommended (API v1.8+)**: create a new API token and set it as
     an environment variable in your shell:

     ```bash
     export KAGGLE_API_TOKEN='KGAT_...your_token_here...'
     ```

     (You can add that line to `~/.zshrc` or `~/.bashrc` to make it
     permanent.)

   - **Legacy method**: click **“Create New Token”** under *Legacy API
     Credentials*. This downloads `kaggle.json`. Move it to:

     - macOS/Linux: `~/.kaggle/kaggle.json`
     - Windows: `C:\Users\<USER>\.kaggle\kaggle.json`

     On macOS/Linux you may need:

     ```bash
     chmod 600 ~/.kaggle/kaggle.json
     ```

3. From the **repository root**, create and activate a virtual
   environment (optional but recommended) and install the Kaggle client:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows
   pip install kaggle
