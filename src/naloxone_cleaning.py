import pandas as pd
from pathlib import Path


# ------------------------------------------------------------
# FILE PATHS
# ------------------------------------------------------------

RAW_FILE = Path("data/raw/naloxone.csv")
OUTPUT_FILE = Path("data/processed/naloxone_quarterly.csv")


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

print("=" * 60)
print("CREATING CLEAN NALOXONE QUARTERLY DATASET")
print("=" * 60)

naloxone = pd.read_csv(RAW_FILE)


# ------------------------------------------------------------
# KEEP MODELING PERIOD
# ------------------------------------------------------------

naloxone = naloxone[
    (naloxone["Year"] >= 2020) &
    (naloxone["Year"] <= 2024)
].copy()


# ------------------------------------------------------------
# KEEP NALOXONE IMPLEMENTATION MEASURE
# ------------------------------------------------------------

kits = naloxone[
    naloxone["Category"] == "Kits distributed per 100,000 population"
].copy()


# ------------------------------------------------------------
# RENAME VARIABLES
# ------------------------------------------------------------

kits = kits.rename(columns={
    "Value": "Naloxone_Kits_Per_100k"
})


# ------------------------------------------------------------
# KEEP REQUIRED COLUMNS
# ------------------------------------------------------------

kits = kits[
    [
        "Year",
        "Quarter",
        "Naloxone_Kits_Per_100k"
    ]
]


# ------------------------------------------------------------
# SORT
# ------------------------------------------------------------

kits = kits.sort_values(
    ["Year", "Quarter"]
).reset_index(drop=True)


# ------------------------------------------------------------
# CHECK DATA
# ------------------------------------------------------------

print("\nNumber of quarters:", len(kits))

print("\nMissing values:")
print(kits.isna().sum())

print("\nFirst 5 rows:")
print(kits.head().to_string(index=False))

print("\nLast 5 rows:")
print(kits.tail().to_string(index=False))


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

kits.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\n" + "=" * 60)
print("NALOXONE QUARTERLY DATASET CREATED")
print("=" * 60)

print(f"\nSaved to: {OUTPUT_FILE}")