import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("data/processed")

HEALTH_FILE = PROCESSED_DIR / "health_outcomes_quarterly.csv"
SCS_FILE = PROCESSED_DIR / "scs_quarterly.csv"
SITES_FILE = PROCESSED_DIR / "site_counts_quarterly.csv"
NALOXONE_FILE = PROCESSED_DIR / "naloxone_quarterly.csv"
OUTPUT_FILE = PROCESSED_DIR / "master_modeling_dataset.csv"

# Load datasets
health = pd.read_csv(HEALTH_FILE)
scs = pd.read_csv(SCS_FILE)
sites = pd.read_csv(SITES_FILE)
naloxone = pd.read_csv(NALOXONE_FILE)

print("\nRows in each dataset:")
print("Health outcomes:", len(health))
print("SCS:", len(scs))
print("Site counts:", len(sites))
print("Naloxone:", len(naloxone))

# Standardize Year and Quarter data types

for df in [health, scs, sites, naloxone]:
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Quarter"] = (
        df["Quarter"]
        .astype(str)
        .str.extract(r"(\d+)")[0]
    )
    df["Quarter"] = pd.to_numeric(
        df["Quarter"],
        errors="coerce"
    )

# Convert to integers after cleaning
for df in [health, scs, sites, naloxone]:
    df["Year"] = df["Year"].astype(int)
    df["Quarter"] = df["Quarter"].astype(int)

# Merge datasets

master = health.merge(
    scs,
    on=["Year", "Quarter"],
    how="inner"
)

master = master.merge(
    sites,
    on=["Year", "Quarter"],
    how="inner"
)

master = master.merge(
    naloxone,
    on=["Year", "Quarter"],
    how="inner"
)

# Sort chronologically

master = master.sort_values(
    ["Year", "Quarter"]
).reset_index(drop=True)

# Add a flag for the partial SCS quarter
master["SCS_Partial_Quarter"] = (
    (master["Year"] == 2020) &
    (master["Quarter"] == 1)
).astype(int)

# Check results
print("\n" + "=" * 60)
print("MASTER DATASET CHECK")
print("=" * 60)

print("\nRows:", len(master))
print("Columns:", len(master.columns))

print("\nColumn names:")
print(master.columns.tolist())

print("\nMissing values:")
print(master.isna().sum())

print("\nFirst 5 rows:")
print(master.head().to_string(index=False))

print("\nLast 5 rows:")
print(master.tail().to_string(index=False))

print("\nDate range:")
print(
    f"{master.iloc[0]['Year']} Q{master.iloc[0]['Quarter']} "
    f"to "
    f"{master.iloc[-1]['Year']} Q{master.iloc[-1]['Quarter']}"
)

# Save

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

master.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 60)
print("MASTER MODELING DATASET CREATED")
print("=" * 60)

print(f"\nSaved to: {OUTPUT_FILE}")