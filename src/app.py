import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from simulation import run_simulation


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Overdose Policy Simulator",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"


# ============================================================
# LOAD HISTORICAL DATA
# ============================================================

@st.cache_data
def load_historical_data():

    data_path = (
        DATA_DIR /
        "master_modeling_dataset.csv"
    )

    return pd.read_csv(data_path)


historical_data = load_historical_data()


# ============================================================
# TITLE
# ============================================================

st.title("Overdose Policy Simulator")

st.write(
    """
    Explore how different implementation levels of overdose
    prevention interventions affect projected activity,
    costs, and selected economic outcomes.
    """
)


st.divider()


# ============================================================
# POLICY INPUTS
# ============================================================

st.header("Policy Implementation")

st.write(
    "Select an implementation level for each intervention."
)


col1, col2, col3 = st.columns(3)


with col1:

    st.subheader("SCS")

    scs_percentage = st.slider(
        "SCS implementation",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        format="%d%%"
    )


with col2:

    st.subheader("Virtual Monitoring")

    nors_percentage = st.slider(
        "Virtual monitoring implementation",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        format="%d%%"
    )


with col3:

    st.subheader("Naloxone")

    naloxone_percentage = st.slider(
        "Naloxone implementation",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        format="%d%%"
    )


# Convert percentages to 0-1

scs_rate = scs_percentage / 100

nors_rate = nors_percentage / 100

naloxone_rate = naloxone_percentage / 100


# ============================================================
# RUN SIMULATION
# ============================================================

results = run_simulation(
    scs_rate,
    nors_rate,
    naloxone_rate
)

scs = results["scs"]

nors = results["nors"]

naloxone = results["naloxone"]


st.divider()

st.header("Projected Impact")


# ============================================================
# SCS RESULTS
# ============================================================

st.subheader(
    f"Supervised Consumption Services — {scs_percentage}%"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Projected Visits / Quarter",
        f"{scs['projected_visits']:,.0f}"
    )

with col2:

    st.metric(
        "Additional Visits",
        f"{scs['incremental_visits']:,.0f}"
    )

with col3:

    st.metric(
        "Additional Events",
        f"{scs['additional_events']:,.0f}"
    )


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Avoided Emergency Cost",
        f"${scs['avoided_emergency_cost']:,.0f}"
    )

with col2:

    st.metric(
        "Operating Cost",
        f"${scs['operating_cost']:,.0f}"
    )

with col3:

    st.metric(
        "Net Fiscal Impact",
        f"${scs['net_fiscal_impact']:,.0f}"
    )


# ============================================================
# NORS RESULTS
# ============================================================

st.divider()

st.subheader(
    f"Virtual Overdose Monitoring — {nors_percentage}%"
)

st.info(
    """
    This component uses published National Overdose Response
    Service (NORS) program activity as a benchmark. It is not a
    national population baseline.
    """
)


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Projected Responses / Quarter",
        f"{nors['projected_responses']:,.2f}"
    )

with col2:

    st.metric(
        "Healthcare Savings",
        f"${nors['healthcare_savings']:,.0f}"
    )

with col3:

    st.metric(
        "Program Cost",
        f"${nors['operating_cost']:,.0f}"
    )


col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Healthcare-Only Net Impact",
        f"${nors['healthcare_net_impact']:,.0f}"
    )

with col2:

    st.metric(
        "Published Benefit-Cost Ratio",
        "8.59"
    )


# ============================================================
# NALOXONE RESULTS
# ============================================================

st.divider()

st.subheader(
    f"Naloxone Distribution — {naloxone_percentage}%"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Baseline Kits / 100k / Quarter",
        f"{1731.56:,.0f}"
    )

with col2:

    st.metric(
        "Projected Kits / 100k / Quarter",
        f"{naloxone['projected_kits_per_100k']:,.0f}"
    )

with col3:

    st.metric(
        "Additional Kits / 100k",
        f"{naloxone['incremental_kits_per_100k']:,.0f}"
    )


st.metric(
    "Additional Cost / 100k",
    f"${naloxone['incremental_cost_per_100k']:,.0f}"
)


st.caption(
    "The base model does not apply an unsupported mortality-"
    "reduction estimate to additional naloxone distribution."
)


# ============================================================
# COST COMPARISON
# ============================================================

st.divider()

st.header("Intervention Cost Comparison")

cost_data = pd.DataFrame(
    {
        "Intervention": [
            "SCS",
            "Virtual Monitoring",
            "Naloxone"
        ],
        "Cost": [
            scs["operating_cost"],
            nors["operating_cost"],
            naloxone["incremental_cost_per_100k"]
        ]
    }
)


fig, ax = plt.subplots()

ax.bar(
    cost_data["Intervention"],
    cost_data["Cost"]
)

ax.set_ylabel("CAD")
ax.set_title("Projected Incremental Cost")

st.pyplot(fig)


# ============================================================
# HISTORICAL CONTEXT
# ============================================================

st.divider()

st.header("Historical Context")

st.write(
    """
    Historical Canadian health-outcome data are shown for
    context. These trends are not interpreted as causal estimates
    of intervention effectiveness.
    """
)


historical_plot = historical_data.copy()

historical_plot["Date"] = pd.PeriodIndex(
    historical_plot["Year"].astype(str)
    + "Q"
    + historical_plot["Quarter"].astype(str),
    freq="Q"
).to_timestamp()


fig, ax = plt.subplots()

ax.plot(
    historical_plot["Date"],
    historical_plot["Opioid_Deaths"],
    label="Opioid Deaths"
)

ax.plot(
    historical_plot["Date"],
    historical_plot["Hospitalizations"],
    label="Hospitalizations"
)

ax.plot(
    historical_plot["Date"],
    historical_plot["ED_Visits"],
    label="ED Visits"
)

ax.set_xlabel("Year")
ax.set_ylabel("Number")
ax.set_title(
    "Canadian Opioid-Related Health Outcomes"
)

ax.legend()

st.pyplot(fig)


# ============================================================
# METHODOLOGY
# ============================================================

st.divider()

with st.expander("How the Simulator Works"):

    st.markdown(
        """
        ### 1. User inputs

        The user independently selects an implementation rate for
        SCS, virtual overdose monitoring, and naloxone.

        The three rates do not have to be the same.

        ### 2. SCS

        Additional SCS visits are calculated from the 2024
        quarterly baseline.

        The observed 2024 SCS nonfatal-overdose event rate is
        applied to the additional visits.

        Estimated emergency costs avoided are based on the
        published SCS cost analysis.

        SCS operating costs use a provisional $52 CAD per visit
        estimate from a Calgary SCS cost study.

        ### 3. Virtual overdose monitoring

        The model uses published NORS program activity as a
        benchmark.

        Published healthcare savings of $4,470.82 per community
        overdose response are used.

        The published 8.59 benefit-cost ratio is displayed
        separately.

        ### 4. Naloxone

        The model uses the observed Canadian naloxone distribution
        rate per 100,000 population.

        A $50 CAD per-kit cost assumption is applied.

        No unsupported mortality-effectiveness estimate is used.

        ### Important limitation

        These are scenario projections based on published
        parameters and observed baseline activity.

        The simulator does not claim that changing an
        implementation percentage will directly cause a specific
        change in national mortality or hospitalization.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Overdose Policy Simulator | AI-Augmented Policy Analysis Pilot"
)