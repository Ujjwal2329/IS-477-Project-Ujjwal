#!/usr/bin/env python

"""
Download coffee datasets from Kaggle and check SHA-256 checksums.

Run these from the repository root, e.g.:

  python scripts/get_data.py download
  python scripts/get_data.py write-checks
  python scripts/get_data.py verify
"""

import argparse
import hashlib
from pathlib import Path
import subprocess
import sys
import zipfile

# Folders / files
RAW_DIR = Path("data/raw")
CHECKSUM_FILE = Path("data/checksums.sha256")

# Datasets from Kaggle
DATASETS = {
    "coffee_sales": {
        "kaggle_id": "ahmedabbas757/coffee-sales",
        "zip_name": "coffee-sales.zip",
        "expected_files": ["coffee_sales.csv"],
    },
    "coffee_shop": {
        "kaggle_id": "jawad3664/coffee-shop",
        "zip_name": "coffee-shop.zip",
        "expected_files": ["coffee_shop.csv"],
    },
}


def download_dataset(name: str, meta: dict) -> None:
    """Download one Kaggle dataset and unzip it into data/raw/."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    kaggle_id = meta["kaggle_id"]
    zip_name = meta["zip_name"]
    zip_path = RAW_DIR / zip_name

    cmd = [
        "kaggle",
        "datasets",
        "download",
        "-d",
        kaggle_id,
        "-p",
        str(RAW_DIR),
        "--force",
    ]
    print(f"Downloading {kaggle_id} into {RAW_DIR} ...")
    subprocess.run(cmd, check=True)

    # If the zip file name is different, rename the only .zip we see
    if not zip_path.exists():
        zips = list(RAW_DIR.glob("*.zip"))
        if len(zips) == 1:
            zips[0].rename(zip_path)

    print(f"Unzipping {zip_path.name} ...")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(RAW_DIR)


def download_all() -> None:
    for ds_name, meta in DATASETS.items():
        print(f"\n=== Downloading {ds_name} ===")
        download_dataset(ds_name, meta)


def sha256sum(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def write_checksums() -> None:
    """
    Create data/checksums.sha256 with SHA-256 hashes
    for each expected raw CSV file.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with CHECKSUM_FILE.open("w") as f:
        for _, meta in DATASETS.items():
            for fname in meta["expected_files"]:
                file_path = RAW_DIR / fname
                if not file_path.exists():
                    print(f"[WARN] Missing file: {file_path}", file=sys.stderr)
                    continue
                digest = sha256sum(file_path)
                rel_path = file_path.as_posix()
                line = f"{digest}  {rel_path}\n"
                f.write(line)
                print(line, end="")  # also print to console


def verify_checksums() -> None:
    """
    Compare current files under data/raw/ to stored hashes.
    """
    if not CHECKSUM_FILE.exists():
        print("Checksum file not found. Run 'write-checks' first.", file=sys.stderr)
        sys.exit(1)

    print(f"Verifying checksums from {CHECKSUM_FILE} ...")
    all_ok = True

    with CHECKSUM_FILE.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(maxsplit=1)
            if len(parts) != 2:
                continue

            expected_hash, rel_path = parts
            file_path = Path(rel_path)

            if not file_path.exists():
                print(f"[FAIL] Missing file: {file_path}", file=sys.stderr)
                all_ok = False
                continue

            actual_hash = sha256sum(file_path)

            if actual_hash == expected_hash:
                print(f"[OK]   {file_path}")
            else:
                print(
                    f"[FAIL] {file_path} hash mismatch.\n"
                    f"       expected: {expected_hash}\n"
                    f"       actual:   {actual_hash}",
                    file=sys.stderr,
                )
                all_ok = False

    if not all_ok:
        sys.exit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download coffee datasets and check integrity."
    )
    parser.add_argument(
        "command",
        choices=["download", "write-checks", "verify"],
        help="download: get data from Kaggle; "
             "write-checks: create checksum file; "
             "verify: compare files to stored checksums.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.command == "download":
        download_all()
    elif args.command == "write-checks":
        write_checksums()
    elif args.command == "verify":
        verify_checksums()


if __name__ == "__main__":
    main()