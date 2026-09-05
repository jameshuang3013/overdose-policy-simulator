import pandas as pd
from pathlib import Path

print("=" * 60)
print("CREATING 2024 BASELINE DATASET")
print("=" * 60)

# --------------------------------------------------
# File paths
# --------------------------------------------------

INPUT_FILE = Path("data/processed/master_modeling_dataset.csv")
OUTPUT_FILE = Path("data/processed/baseline_2024.csv")

# --------------------------------------------------
# Load master dataset
# --------------------------------------------------

master = pd.read_csv(INPUT_FILE)

# --------------------------------------------------
# Select 2024 data
# --------------------------------------------------

baseline_data = master[
    master["Year"] == 2024
].copy()

print("\n2024 quarters found:", len(baseline_data))

# --------------------------------------------------
# Variables used for the baseline
# --------------------------------------------------

baseline_variables = [
    "SCS_Total_Visits",
    "SCS_Clients_Monthly_Sum",
    "SCS_Nonfatal_Overdoses",
    "SCS_Naloxone_Administrations",
    "SCS_Sites",
    "OPS_Sites",
    "Total_Sites",
    "Naloxone_Kits_Per_100k",
    "Opioid_Deaths",
    "Hospitalizations",
    "ED_Visits",
    "EMS_Responses"
]

# --------------------------------------------------
# Calculate 2024 annual averages
# --------------------------------------------------

baseline = baseline_data[baseline_variables].mean().to_frame().T

# Add baseline year
baseline.insert(0, "Baseline_Year", 2024)

# --------------------------------------------------
# Check results
# --------------------------------------------------

print("\n" + "=" * 60)
print("2024 BASELINE")
print("=" * 60)

print("\nBaseline values:")

for column in baseline.columns:
    if column != "Baseline_Year":
        print(f"{column}: {baseline[column].iloc[0]:,.2f}")

print("\nMissing values:")
print(baseline.isna().sum())

# --------------------------------------------------
# Save
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

baseline.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 60)
print("2024 BASELINE DATASET CREATED")
print("=" * 60)

print(f"\nSaved to: {OUTPUT_FILE}")