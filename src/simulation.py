from pathlib import Path
import pandas as pd


# ============================================================
# OVERDOSE POLICY SIMULATOR
# Simulation Engine
# Canada - 2024 baseline
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"


# ============================================================
# 1. MODEL PARAMETERS
# ============================================================

# ------------------------------------------------------------
# SCS
# ------------------------------------------------------------

SCS_COST_PER_VISIT = 52.00

# 2024 Safeworks:
# 1,035 adverse events
# 9 EMS call-outs
SCS_ONSITE_MANAGEMENT_RATE = 1 - (9 / 1035)

# EMS + ED + physician assessment
SCS_AVOIDED_EMERGENCY_COST = 1622.00


# ------------------------------------------------------------
# Virtual Overdose Monitoring (NORS)
# ------------------------------------------------------------

NORS_PROGRAM_COST_2_YEARS = 1_592_000.00

NORS_PROGRAM_COST_PER_QUARTER = (
    NORS_PROGRAM_COST_2_YEARS / 8
)

NORS_SAVINGS_PER_RESPONSE = 4_470.82

# Sensitivity/threshold value only
NORS_CALL_COST_THRESHOLD = 450.00

NORS_BENEFIT_COST_RATIO = 8.59


# ------------------------------------------------------------
# Naloxone
# ------------------------------------------------------------

NALOXONE_COST_PER_KIT = 50.00


# ============================================================
# 2. LOAD 2024 BASELINE
# ============================================================

baseline_path = DATA_DIR / "baseline_2024.csv"

baseline = pd.read_csv(baseline_path).iloc[0]


# ============================================================
# 3. BASELINE VALUES
# ============================================================

BASELINE_SCS_VISITS = float(
    baseline["SCS_Total_Visits"]
)

BASELINE_SCS_EVENTS = float(
    baseline["SCS_Nonfatal_Overdoses"]
)

SCS_EVENT_RATE = (
    BASELINE_SCS_EVENTS /
    BASELINE_SCS_VISITS
)


BASELINE_NALOXONE_RATE = float(
    baseline["Naloxone_Kits_Per_100k"]
)


# ============================================================
# 4. NORS ACTIVITY BENCHMARK
# ============================================================

NORS_OBSERVED_RESPONSES = 11
NORS_OBSERVATION_QUARTERS = 7

NORS_RESPONSE_BENCHMARK = (
    NORS_OBSERVED_RESPONSES /
    NORS_OBSERVATION_QUARTERS
)


# ============================================================
# 5. VALIDATE USER INPUT
# ============================================================

def validate_implementation_rate(implementation_rate):
    """
    Convert an implementation rate to a value between 0 and 1.

    Examples:
        0.50 -> 0.50
        50   -> 0.50
    """

    implementation_rate = float(
        implementation_rate
    )

    if implementation_rate > 1:
        implementation_rate /= 100

    if implementation_rate < 0:
        raise ValueError(
            "Implementation rate cannot be below 0%."
        )

    if implementation_rate > 1:
        raise ValueError(
            "Implementation rate cannot exceed 100%."
        )

    return implementation_rate


# ============================================================
# 6. SCS CALCULATION
# ============================================================

def simulate_scs(implementation_rate):

    rate = validate_implementation_rate(
        implementation_rate
    )

    incremental_visits = (
        BASELINE_SCS_VISITS * rate
    )

    projected_visits = (
        BASELINE_SCS_VISITS +
        incremental_visits
    )

    additional_events = (
        incremental_visits *
        SCS_EVENT_RATE
    )

    onsite_events = (
        additional_events *
        SCS_ONSITE_MANAGEMENT_RATE
    )

    avoided_emergency_cost = (
        onsite_events *
        SCS_AVOIDED_EMERGENCY_COST
    )

    operating_cost = (
        incremental_visits *
        SCS_COST_PER_VISIT
    )

    net_fiscal_impact = (
        avoided_emergency_cost -
        operating_cost
    )

    return {
        "implementation_rate": rate,
        "projected_visits": projected_visits,
        "incremental_visits": incremental_visits,
        "additional_events": additional_events,
        "onsite_events": onsite_events,
        "avoided_emergency_cost": avoided_emergency_cost,
        "operating_cost": operating_cost,
        "net_fiscal_impact": net_fiscal_impact,
    }


# ============================================================
# 7. VIRTUAL OVERDOSE MONITORING CALCULATION
# ============================================================

def simulate_nors(implementation_rate):

    rate = validate_implementation_rate(
        implementation_rate
    )

    projected_responses = (
        NORS_RESPONSE_BENCHMARK * rate
    )

    healthcare_savings = (
        projected_responses *
        NORS_SAVINGS_PER_RESPONSE
    )

    operating_cost = (
        NORS_PROGRAM_COST_PER_QUARTER *
        rate
    )

    healthcare_net_impact = (
        healthcare_savings -
        operating_cost
    )

    broader_benefits = (
        operating_cost *
        NORS_BENEFIT_COST_RATIO
    )

    broader_net_benefit = (
        broader_benefits -
        operating_cost
    )

    return {
        "implementation_rate": rate,
        "projected_responses": projected_responses,
        "healthcare_savings": healthcare_savings,
        "operating_cost": operating_cost,
        "healthcare_net_impact": healthcare_net_impact,
        "published_broader_benefits": broader_benefits,
        "published_broader_net_benefit": broader_net_benefit,
    }


# ============================================================
# 8. NALOXONE CALCULATION
# ============================================================

def simulate_naloxone(implementation_rate):

    rate = validate_implementation_rate(
        implementation_rate
    )

    incremental_kits_rate = (
        BASELINE_NALOXONE_RATE * rate
    )

    projected_kits_rate = (
        BASELINE_NALOXONE_RATE +
        incremental_kits_rate
    )

    incremental_cost = (
        incremental_kits_rate *
        NALOXONE_COST_PER_KIT
    )

    return {
        "implementation_rate": rate,
        "projected_kits_per_100k": projected_kits_rate,
        "incremental_kits_per_100k": incremental_kits_rate,
        "incremental_cost_per_100k": incremental_cost,
    }


# ============================================================
# 9. COMPLETE SIMULATION
# ============================================================

def run_simulation(
    scs_rate,
    nors_rate,
    naloxone_rate
):
    """
    Run the simulator using independent implementation
    rates for each intervention.

    Example:

        run_simulation(
            0.50,
            0.30,
            0.70
        )

    means:

        SCS = 50%
        Virtual monitoring = 30%
        Naloxone = 70%
    """

    scs_rate = validate_implementation_rate(
        scs_rate
    )

    nors_rate = validate_implementation_rate(
        nors_rate
    )

    naloxone_rate = validate_implementation_rate(
        naloxone_rate
    )

    scs = simulate_scs(scs_rate)

    nors = simulate_nors(nors_rate)

    naloxone = simulate_naloxone(
        naloxone_rate
    )

    return {
        "scs": scs,
        "nors": nors,
        "naloxone": naloxone,
    }


# ============================================================
# 10. TEST
# ============================================================

if __name__ == "__main__":

    results = run_simulation(
        0.50,
        0.30,
        0.70
    )

    print()
    print("=" * 70)
    print("OVERDOSE POLICY SIMULATOR - TEST")
    print("=" * 70)

    print("\nIMPLEMENTATION RATES")

    print(
        f"SCS: "
        f"{results['scs']['implementation_rate']:.0%}"
    )

    print(
        f"Virtual monitoring: "
        f"{results['nors']['implementation_rate']:.0%}"
    )

    print(
        f"Naloxone: "
        f"{results['naloxone']['implementation_rate']:.0%}"
    )

    print("\nSCS")
    print("-" * 70)

    print(
        f"Projected visits/quarter: "
        f"{results['scs']['projected_visits']:,.2f}"
    )

    print(
        f"Incremental visits: "
        f"{results['scs']['incremental_visits']:,.2f}"
    )

    print(
        f"Avoided emergency cost: "
        f"${results['scs']['avoided_emergency_cost']:,.2f}"
    )

    print(
        f"Operating cost: "
        f"${results['scs']['operating_cost']:,.2f}"
    )

    print(
        f"Net fiscal impact: "
        f"${results['scs']['net_fiscal_impact']:,.2f}"
    )

    print("\nVIRTUAL OVERDOSE MONITORING")
    print("-" * 70)

    print(
        f"Projected responses/quarter: "
        f"{results['nors']['projected_responses']:,.2f}"
    )

    print(
        f"Healthcare savings: "
        f"${results['nors']['healthcare_savings']:,.2f}"
    )

    print(
        f"Operating cost: "
        f"${results['nors']['operating_cost']:,.2f}"
    )

    print(
        f"Healthcare-only net impact: "
        f"${results['nors']['healthcare_net_impact']:,.2f}"
    )

    print("\nNALOXONE")
    print("-" * 70)

    print(
        f"Projected kits/100k/quarter: "
        f"{results['naloxone']['projected_kits_per_100k']:,.2f}"
    )

    print(
        f"Incremental kits/100k: "
        f"{results['naloxone']['incremental_kits_per_100k']:,.2f}"
    )

    print(
        f"Incremental cost/100k: "
        f"${results['naloxone']['incremental_cost_per_100k']:,.2f}"
    )

    print()
    print("=" * 70)