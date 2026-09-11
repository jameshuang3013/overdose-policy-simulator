import pandas as pd
from pathlib import Path


RAW_FILE = Path("data/raw/site_counts.csv")
OUTPUT_FILE = Path("data/processed/site_counts_quarterly.csv")


sites = pd.read_csv(RAW_FILE)


# CREATE QUARTER

sites["Month_Number"] = pd.to_datetime(
    sites["Month"],
    format="%b"
).dt.month

sites["Quarter"] = "Q" + (
    ((sites["Month_Number"] - 1) // 3) + 1
).astype(str)


# KEEP MODELING PERIOD

sites = sites[
    (sites["Year"] >= 2020) &
    (sites["Year"] <= 2024)
].copy()


# CONVERT TO QUARTERLY DATA

quarterly = sites.pivot_table(
    index=["Year", "Quarter"],
    columns="Category",
    values="Number of sites",
    aggfunc="mean"
).reset_index()


# RENAME COLUMNS

quarterly = quarterly.rename(columns={
    "Total sites": "Total_Sites",
    "SCS sites": "SCS_Sites",
    "OPS sites": "OPS_Sites"
})


# SORT


quarterly = quarterly.sort_values(
    ["Year", "Quarter"]
).reset_index(drop=True)


# CHECK DATA

print("\nNumber of quarters:", len(quarterly))

print("\nMissing values:")
print(quarterly.isna().sum())

print("\nFirst 5 rows:")
print(quarterly.head().to_string(index=False))

print("\nLast 5 rows:")
print(quarterly.tail().to_string(index=False))


# SAVE

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

quarterly.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\n" + "=" * 60)
print("SITE COUNT DATASET CREATED")
print("=" * 60)

print(f"\nSaved to: {OUTPUT_FILE}")