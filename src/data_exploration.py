import pandas as pd

print("=" * 60)
print("DATASET 1 - OVERLAP ANALYSIS")
print("=" * 60)

file_path = "data/raw/SubstanceHarmsData.csv"

harms = pd.read_csv(file_path)

# Keep only usable overall-number observations
overall = harms[
    (harms["Specific_Measure"] == "Overall numbers") &
    (harms["Unit"] == "Number")
].copy()

# Canada only
canada = overall[
    overall["Region"] == "Canada"
].copy()

print("\nTotal Canada observations:", len(canada))

# ------------------------------------------------------------
# QUARTERLY DATA
# ------------------------------------------------------------

quarterly = canada[
    canada["Time_Period"] == "By quarter"
].copy()

print("\n" + "=" * 60)
print("CANADA - QUARTERLY DATA")
print("=" * 60)

print("\nSources:")
print(quarterly["Source"].unique())

print("\nQuarterly observations by source:")
print(
    quarterly.groupby("Source")["Year_Quarter"]
    .agg(["min", "max", "count"])
)

# ------------------------------------------------------------
# ANNUAL DATA
# ------------------------------------------------------------

annual = canada[
    canada["Time_Period"] == "By year"
].copy()

print("\n" + "=" * 60)
print("CANADA - ANNUAL DATA")
print("=" * 60)

print("\nAnnual observations by source:")
print(
    annual.groupby("Source")["Year_Quarter"]
    .agg(["min", "max", "count"])
)

# ------------------------------------------------------------
# QUARTERLY OVERLAP
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("QUARTERLY OVERLAP")
print("=" * 60)

pivot = quarterly.pivot_table(
    index="Year_Quarter",
    columns="Source",
    values="Value",
    aggfunc="first"
)

print("\nNumber of available outcomes per quarter:")
print(pivot.notna().sum(axis=1).value_counts().sort_index())

print("\nQuarters where ALL FOUR outcomes are available:")

all_four = pivot.dropna()

print(all_four)

print("\nNumber of quarters with all four outcomes:", len(all_four))

# ------------------------------------------------------------
# MISSING OUTCOMES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("MISSING OUTCOME CHECK")
print("=" * 60)

print(
    pivot.isna().sum()
)

# ------------------------------------------------------------
# DATE RANGE
# ------------------------------------------------------------

if len(all_four) > 0:
    print("\nEarliest quarter with all four outcomes:")
    print(all_four.index.min())

    print("\nLatest quarter with all four outcomes:")
    print(all_four.index.max())