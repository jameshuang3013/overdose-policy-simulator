import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from simulation import (
    run_simulation,
    calculate_fiscal_summary,
    BASELINE_NALOXONE_RATE,
)


# PAGE CONFIGURATION
st.set_page_config(
    page_title="Overdose Policy Fiscal Simulator",
    page_icon="🏥",
    layout="wide",
)


# PROJECT PATHS
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"


# LOAD HISTORICAL DATA
@st.cache_data
def load_historical_data():

    file_path = (
        DATA_DIR /
        "master_modeling_dataset.csv"
    )

    df = pd.read_csv(file_path)

    df["Quarter_Label"] = (
        df["Year"].astype(str)
        + " Q"
        + df["Quarter"].astype(str)
    )

    return df


historical_data = load_historical_data()


# TITLE
st.title("Overdose Policy Fiscal Simulator")

st.markdown(
    """
This interactive simulator allows users to explore the potential
**fiscal impact** of different implementation levels for selected
overdose prevention and harm reduction interventions in Canada.

The model uses Canadian historical data and published cost estimates
to produce scenario-based estimates of intervention costs and
directly supported potential fiscal savings.

Results are intended for **decision support and scenario analysis**,
not as predictions of future health outcomes.
"""
)


# SIDEBAR — POLICY INPUTS
st.sidebar.header("Policy Implementation")

st.sidebar.markdown(
    """
Choose the implementation level for each intervention.

The percentages represent an **increase in intervention activity
relative to the 2024 baseline**.

They do **not** represent the percentage of the population receiving
the intervention.
"""
)


# SCS
scs_percent = st.sidebar.slider(
    "Supervised Consumption Services (SCS)",
    min_value=0,
    max_value=100,
    value=0,
    step=1,
)


# Virtual Overdose Monitoring
nors_percent = st.sidebar.slider(
    "Virtual Overdose Monitoring",
    min_value=0,
    max_value=100,
    value=0,
    step=1,
)


# Naloxone
naloxone_percent = st.sidebar.slider(
    "Naloxone Distribution",
    min_value=0,
    max_value=100,
    value=0,
    step=1,
)


# Convert percentages to decimal rates
scs_rate = scs_percent / 100
nors_rate = nors_percent / 100
naloxone_rate = naloxone_percent / 100


# RUN SIMULATION
results = run_simulation(
    scs_rate=scs_rate,
    nors_rate=nors_rate,
    naloxone_rate=naloxone_rate,
)

fiscal = calculate_fiscal_summary(
    results
)


# INTERPRETATION GUIDE
st.info(
    """
### How to interpret the implementation percentages

The percentages represent a **change relative to the 2024 baseline**,
not the percentage of the Canadian population receiving an intervention.

**SCS:** The implementation percentage increases SCS activity relative
to the 2024 quarterly baseline. The model then estimates additional
operating cost and potential emergency-service savings.

**Virtual Overdose Monitoring:** The implementation percentage scales
the program-level quarterly cost assumption. The model does not
project response volume or national healthcare savings because a
sufficiently reliable national activity baseline is unavailable.

**Naloxone:** The implementation percentage increases the modeled
distribution rate relative to the 2024 Canadian baseline. The model
estimates the associated additional distribution cost.

The model does not automatically assume reductions in mortality,
hospitalizations, or emergency-department visits.
"""
)


# FISCAL SUMMARY CARDS
st.header("Fiscal Outcomes")


# SCS FISCAL RESULTS
st.header("Supervised Consumption Services")

scs = results["scs"]


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Implementation",
        f"{scs_percent}%",
    )


with col2:

    st.metric(
        "Additional Visits / Quarter",
        f"{scs['incremental_visits']:,.0f}",
    )


with col3:

    st.metric(
        "Projected Visits / Quarter",
        f"{scs['projected_visits']:,.0f}",
    )


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Potential Emergency-Service Savings",
        f"${scs['avoided_emergency_cost']:,.0f}",
    )


with col2:

    st.metric(
        "SCS Operating Cost",
        f"${scs['operating_cost']:,.0f}",
    )


with col3:

    st.metric(
        "Net Fiscal Impact",
        f"${scs['net_fiscal_impact']:,.0f}",
    )


st.markdown(
    """
### SCS cost calculation

The model estimates additional SCS visits from the selected
implementation increase. The observed 2024 SCS non-fatal
overdose-event rate is then applied to those additional visits.

The resulting events are adjusted using the 2024 Safeworks
onsite-management rate.

Potential emergency-service savings are based on the published
combined cost of EMS, emergency-department care, and physician
assessment.

The SCS fiscal calculation is:

**Potential Emergency-Service Savings − SCS Operating Cost**
"""
)


# SCS COST VS SAVINGS CHART

st.subheader("SCS Cost vs Potential Savings")

scs_chart_data = pd.DataFrame(
    {
        "Category": [
            "Operating Cost",
            "Potential Savings",
        ],
        "Amount": [
            scs["operating_cost"],
            scs["avoided_emergency_cost"],
        ],
    }
)


fig, ax = plt.subplots(
    figsize=(8, 4.5)
)

ax.bar(
    scs_chart_data["Category"],
    scs_chart_data["Amount"],
)

ax.set_ylabel("CAD / Quarter")

ax.set_title(
    "SCS Modeled Cost and Potential Savings"
)

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)


# VIRTUAL OVERDOSE MONITORING
st.header("Virtual Overdose Monitoring")

nors = results["nors"]


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Implementation",
        f"{nors_percent}%",
    )


with col2:

    st.metric(
        "Program Cost / Quarter",
        f"${nors['operating_cost']:,.0f}",
    )


st.subheader("Published Evidence References")


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Published Savings / Response",
        f"${nors['published_savings_per_response']:,.2f}",
    )


with col2:

    st.metric(
        "Published Benefit-Cost Ratio",
        f"{nors['published_benefit_cost_ratio']:.2f}",
    )


# NALOXONE
st.header("Naloxone Distribution")

naloxone = results["naloxone"]


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Implementation",
        f"{naloxone_percent}%",
    )


with col2:

    st.metric(
        "Baseline Distribution Rate",
        f"{BASELINE_NALOXONE_RATE:,.0f}",
        help="Kits distributed per 100,000 population per quarter.",
    )


with col3:

    st.metric(
        "Projected Distribution Rate",
        f"{naloxone['projected_kits_per_100k']:,.0f}",
    )


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Additional Distribution",
        f"{naloxone['incremental_kits_per_100k']:,.0f}",
    )


with col2:

    st.metric(
        "Additional Cost / 100k / Quarter",
        f"${naloxone['incremental_cost_per_100k']:,.0f}",
    )


# MODELED INTERVENTION COSTS
st.subheader("Modeled Intervention Costs")

cost_data = pd.DataFrame({
    "Intervention": [
        "Supervised Consumption\nServices",
        "Virtual Overdose\nMonitoring",
        "Naloxone Distribution"
    ],
    "Cost": [
        scs["operating_cost"],
        nors["operating_cost"],
        naloxone["incremental_cost_per_100k"]
    ]
})

fig, ax = plt.subplots(figsize=(8, 3.8))

bars = ax.barh(cost_data["Intervention"], cost_data["Cost"])

# Add value labels
for bar in bars:
    width = bar.get_width()
    ax.text(
        width,
        bar.get_y() + bar.get_height()/2,
        f" ${width:,.0f}",
        va="center",
        ha="left",
        fontsize=10
    )

ax.set_xlabel("Modeled Cost (CAD)")
ax.set_title("Modeled Intervention Costs")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)


# INTERVENTION COST TABLE
st.header("Fiscal Cost Summary")

summary_table = pd.DataFrame(
    {
        "Intervention": [
            "Supervised Consumption Services",
            "Virtual Overdose Monitoring",
            "Naloxone Distribution",
        ],
        "Implementation": [
            f"{scs_percent}%",
            f"{nors_percent}%",
            f"{naloxone_percent}%",
        ],
        "Modeled Cost": [
            f"${scs['operating_cost']:,.0f} / quarter",
            f"${nors['operating_cost']:,.0f} / quarter",
            f"${naloxone['incremental_cost_per_100k']:,.0f} / 100k / quarter",
        ],
        "Potential Direct Savings": [
            f"${scs['avoided_emergency_cost']:,.0f}",
            "Not projected",
            "Not projected",
        ],
        "Net Fiscal Impact": [
            f"${scs['net_fiscal_impact']:,.0f}",
            "Not projected",
            "Not projected",
        ],
    }
)

st.dataframe(
    summary_table,
    use_container_width=True,
    hide_index=True,
)
