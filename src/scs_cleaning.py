import pandas as pd
from pathlib import Path


RAW_FILE = Path("data/raw/scs-visits-clients-trends.csv")
OUTPUT_FILE = Path("data/processed/scs_quarterly.csv")

scs = pd.read_csv(RAW_FILE)


# CONVERT DATE

scs["date"] = pd.to_datetime(scs["date"])
scs["Year"] = scs["date"].dt.year
scs["Quarter"] = "Q" + scs["date"].dt.quarter.astype(str)


# KEEP MODELING PERIOD

scs = scs[
    (scs["Year"] >= 2020) &
    (scs["Year"] <= 2024)
].copy()


# AGGREGATE MONTHLY DATA TO QUARTERLY DATA

scs_quarterly = (
    scs.groupby(["Year", "Quarter"], as_index=False)
    .agg({
        # Sum monthly event/activity totals
        "trend_total_visits": "sum",
        "trend_nr_clients": "sum",
        "trend_nr_od_nf": "sum",
        "trend_nr_od_naloxone": "sum",

        # Average monthly rates/capacity measures
        "trend_rate_od_nf": "mean",
        "trend_rate_od_naloxone": "mean",
        "trend_avg_visits_per_site": "mean",
        "trend_avg_clients_per_site": "mean",
        "nr_sites_reporting": "mean"
    })
)


# RENAME COLUMNS
scs_quarterly = scs_quarterly.rename(columns={
    "trend_total_visits": "SCS_Total_Visits",
    "trend_nr_clients": "SCS_Clients_Monthly_Sum",
    "trend_nr_od_nf": "SCS_Nonfatal_Overdoses",
    "trend_nr_od_naloxone": "SCS_Naloxone_Administrations",
    "trend_rate_od_nf": "SCS_Nonfatal_OD_Rate",
    "trend_rate_od_naloxone": "SCS_Naloxone_OD_Rate",
    "trend_avg_visits_per_site": "SCS_Avg_Visits_Per_Site",
    "trend_avg_clients_per_site": "SCS_Avg_Clients_Per_Site",
    "nr_sites_reporting": "SCS_Sites_Reporting"
})


# SORT DATA

scs_quarterly = scs_quarterly.sort_values(
    ["Year", "Quarter"]
).reset_index(drop=True)


# VALIDATION

print("\nNumber of quarters:", len(scs_quarterly))

print("\nMissing values:")
print(scs_quarterly.isna().sum())

print("\nFirst 5 rows:")
print(scs_quarterly.head())

print("\nLast 5 rows:")
print(scs_quarterly.tail())


# SAVE

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

scs_quarterly.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 60)
print("CLEAN SCS DATASET CREATED")
print("=" * 60)

print(f"\nSaved to: {OUTPUT_FILE}")