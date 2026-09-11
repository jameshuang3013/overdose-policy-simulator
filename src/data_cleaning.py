import pandas as pd
from pathlib import Path


RAW_FILE = Path("data/raw/SubstanceHarmsData.csv")
OUTPUT_FILE = Path("data/processed/health_outcomes_quarterly.csv")


harms = pd.read_csv(RAW_FILE)


# FILTER USABLE OBSERVATIONS

clean = harms[
    (harms["Region"] == "Canada") &
    (harms["Specific_Measure"] == "Overall numbers") &
    (harms["Unit"] == "Number") &
    (harms["Time_Period"] == "By quarter")
].copy()


# KEEP MODELING PERIOD
valid_periods = []

for year in range(2017, 2025):
    for quarter in range(1, 5):
        valid_periods.append(f"{year} Q{quarter}")

clean = clean[
    clean["Year_Quarter"].isin(valid_periods)
].copy()


# CONVERT FROM LONG FORMAT TO WIDE FORMAT
wide = clean.pivot_table(
    index="Year_Quarter",
    columns="Source",
    values="Value",
    aggfunc="first"
).reset_index()


# RENAME COLUMNS
wide = wide.rename(columns={
    "Year_Quarter": "Year_Quarter",
    "Deaths": "Opioid_Deaths",
    "Hospitalizations": "Hospitalizations",
    "Emergency Department (ED) Visits": "ED_Visits",
    "Emergency Medical Services (EMS)": "EMS_Responses"
})


# SPLIT YEAR AND QUARTER
wide["Year"] = wide["Year_Quarter"].str[:4].astype(int)
wide["Quarter"] = wide["Year_Quarter"].str[-2:]


# REORDER COLUMNS
wide = wide[
    [
        "Year",
        "Quarter",
        "Opioid_Deaths",
        "Hospitalizations",
        "ED_Visits",
        "EMS_Responses"
    ]
]


# SORT
wide = wide.sort_values(
    ["Year", "Quarter"]
).reset_index(drop=True)


# CHECK FOR MISSING VALUES
print("\nMissing values:")
print(wide.isna().sum())


# CHECK NUMBER OF ROWS
print("\nNumber of quarters:", len(wide))


# SHOW DATA
print("\nFirst 5 rows:")
print(wide.head())

print("\nLast 5 rows:")
print(wide.tail())


# SAVE
OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

wide.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 60)
print("CLEAN DATASET CREATED")
print("=" * 60)

print(f"\nSaved to: {OUTPUT_FILE}")