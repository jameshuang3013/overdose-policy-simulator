from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"


# Provisional operating cost
SCS_COST_PER_VISIT = 52.00

# 2024 Safeworks:
# 1,035 adverse events
# 9 EMS call-outs
#
# Used to estimate the proportion of events potentially managed
# onsite without EMS.
SCS_ONSITE_MANAGEMENT_RATE = 1 - (9 / 1035)

# EMS + emergency department + physician assessment
SCS_AVOIDED_EMERGENCY_COST = 1622.00


# Virtual Overdose Monitoring (NORS)

# Program-level cost assumption
NORS_PROGRAM_COST_2_YEARS = 1_592_000.00

# Two years = 8 quarters
NORS_PROGRAM_COST_PER_QUARTER = (
    NORS_PROGRAM_COST_2_YEARS / 8
)

# Published healthcare-system savings per response.
# Reference value only.
NORS_SAVINGS_PER_RESPONSE = 4_470.82

# Published sensitivity/threshold value.
# Reference value only.
NORS_CALL_COST_THRESHOLD = 450.00

# Published benefit-cost ratio.
# Reference value only.
NORS_BENEFIT_COST_RATIO = 8.59


# Naloxone

# Provisional cost assumption
NALOXONE_COST_PER_KIT = 50.00



baseline_path = DATA_DIR / "baseline_2024.csv"
baseline = pd.read_csv(baseline_path).iloc[0]


# SCS
BASELINE_SCS_VISITS = float(
    baseline["SCS_Total_Visits"]
)

BASELINE_SCS_EVENTS = float(
    baseline["SCS_Nonfatal_Overdoses"]
)

# Observed 2024 SCS non-fatal overdose event rate
SCS_EVENT_RATE = (
    BASELINE_SCS_EVENTS /
    BASELINE_SCS_VISITS
)


# Naloxone
BASELINE_NALOXONE_RATE = float(
    baseline["Naloxone_Kits_Per_100k"]
)


# 5. INPUT VALIDATION

def validate_implementation_rate(implementation_rate):
    """
    Convert an implementation rate into a decimal between 0 and 1.

    Examples:
        0.50 -> 0.50
        50   -> 0.50
        100  -> 1.00
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


# 6. SCS FISCAL CALCULATION

def simulate_scs(implementation_rate):
    """
    Calculate the fiscal impact of increasing SCS activity.

    The implementation percentage represents an increase relative
    to the 2024 quarterly baseline.

    Example:
        50% implementation means 50% more SCS visits than the
        2024 baseline.
    """

    rate = validate_implementation_rate(
        implementation_rate
    )

    # Additional activity

    incremental_visits = (
        BASELINE_SCS_VISITS * rate
    )

    projected_visits = (
        BASELINE_SCS_VISITS +
        incremental_visits
    )

    # Estimate additional non-fatal overdose events

    additional_events = (
        incremental_visits *
        SCS_EVENT_RATE
    )

    # Estimate events potentially managed onsite

    onsite_events = (
        additional_events *
        SCS_ONSITE_MANAGEMENT_RATE
    )

    # Potential emergency-service savings

    avoided_emergency_cost = (
        onsite_events *
        SCS_AVOIDED_EMERGENCY_COST
    )

    # Additional SCS operating cost

    operating_cost = (
        incremental_visits *
        SCS_COST_PER_VISIT
    )

    # Net fiscal impact

    net_fiscal_impact = (
        avoided_emergency_cost -
        operating_cost
    )

    return {
        "implementation_rate": rate,
        "baseline_visits": BASELINE_SCS_VISITS,
        "projected_visits": projected_visits,
        "incremental_visits": incremental_visits,
        "additional_events": additional_events,
        "onsite_events": onsite_events,
        "avoided_emergency_cost": avoided_emergency_cost,
        "operating_cost": operating_cost,
        "net_fiscal_impact": net_fiscal_impact,
    }


# 7. VIRTUAL OVERDOSE MONITORING FISCAL CALCULATION

def simulate_nors(implementation_rate):
    """
    Calculate the program-level cost of virtual overdose monitoring.

    The implementation percentage scales the quarterly program-cost
    assumption.

    The model does NOT project:
        - response volume
        - healthcare savings
        - healthcare net impact

    because a sufficiently reliable national response-volume baseline
    is not available.
    """

    rate = validate_implementation_rate(
        implementation_rate
    )

    # Program-level quarterly cost
    operating_cost = (
        NORS_PROGRAM_COST_PER_QUARTER *
        rate
    )

    return {
        "implementation_rate": rate,
        "operating_cost": operating_cost,

        # Not projected in the base model
        "healthcare_savings": None,
        "healthcare_net_impact": None,

        # Evidence-only reference values
        "published_savings_per_response":
            NORS_SAVINGS_PER_RESPONSE,

        "published_benefit_cost_ratio":
            NORS_BENEFIT_COST_RATIO,

        "call_cost_threshold":
            NORS_CALL_COST_THRESHOLD,
    }


# 8. NALOXONE FISCAL CALCULATION

def simulate_naloxone(implementation_rate):
    """
    Calculate the additional cost associated with increasing
    naloxone distribution relative to the 2024 baseline.

    The result is expressed per 100,000 population per quarter.
    """

    rate = validate_implementation_rate(
        implementation_rate
    )

    # Additional distribution

    incremental_kits_rate = (
        BASELINE_NALOXONE_RATE *
        rate
    )

    projected_kits_rate = (
        BASELINE_NALOXONE_RATE +
        incremental_kits_rate
    )

    # Additional distribution cost

    incremental_cost = (
        incremental_kits_rate *
        NALOXONE_COST_PER_KIT
    )

    return {
        "implementation_rate": rate,
        "baseline_kits_per_100k":
            BASELINE_NALOXONE_RATE,

        "projected_kits_per_100k":
            projected_kits_rate,

        "incremental_kits_per_100k":
            incremental_kits_rate,

        "incremental_cost_per_100k":
            incremental_cost,
    }


# COMPLETE SIMULATION

def run_simulation(
    scs_rate,
    nors_rate,
    naloxone_rate
):
    """
    Run the complete fiscal simulation.

    Each implementation rate is independent.

    Implementation rates represent increases relative to the
    2024 baseline.
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

    scs = simulate_scs(
        scs_rate
    )

    nors = simulate_nors(
        nors_rate
    )

    naloxone = simulate_naloxone(
        naloxone_rate
    )

    return {
        "scs": scs,
        "nors": nors,
        "naloxone": naloxone,
    }


# FISCAL SUMMARY

def calculate_fiscal_summary(results):
    """
    Create a summary of the directly modeled fiscal outcomes.

    Important:
    SCS, NORS, and naloxone outputs do not all share the same
    geographic/unit basis. Therefore, this function does NOT
    combine all three costs into one misleading national total.

    The summary focuses on comparable intervention-specific
    fiscal outputs.
    """

    scs = results["scs"]
    nors = results["nors"]
    naloxone = results["naloxone"]

    return {
        # SCS
        "scs_operating_cost":
            scs["operating_cost"],

        "scs_potential_savings":
            scs["avoided_emergency_cost"],

        "scs_net_fiscal_impact":
            scs["net_fiscal_impact"],

        # NORS
        "nors_program_cost":
            nors["operating_cost"],

        # Naloxone
        "naloxone_additional_cost_per_100k":
            naloxone["incremental_cost_per_100k"],
    }


# TEST
"""
"if __name__ == "__main__":

    results = run_simulation(
        0.50,
        0.30,
        0.70
    )

    fiscal = calculate_fiscal_summary(
        results
    )

    print()
    print("=" * 70)
    print("OVERDOSE POLICY SIMULATOR - FISCAL MODEL TEST")
    print("=" * 70)

    print("\nIMPLEMENTATION RATES")
    print("-" * 70)

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

    print("\nSCS FISCAL OUTCOMES")
    print("-" * 70)

    print(
        f"Baseline visits/quarter: "
        f"{results['scs']['baseline_visits']:,.2f}"
    )

    print(
        f"Projected visits/quarter: "
        f"{results['scs']['projected_visits']:,.2f}"
    )

    print(
        f"Additional visits: "
        f"{results['scs']['incremental_visits']:,.2f}"
    )

    print(
        f"Additional non-fatal overdose events: "
        f"{results['scs']['additional_events']:,.2f}"
    )

    print(
        f"Potentially managed onsite: "
        f"{results['scs']['onsite_events']:,.2f}"
    )

    print(
        f"Potential emergency-service savings: "
        f"${results['scs']['avoided_emergency_cost']:,.2f}"
    )

    print(
        f"SCS operating cost: "
        f"${results['scs']['operating_cost']:,.2f}"
    )

    print(
        f"Net fiscal impact: "
        f"${results['scs']['net_fiscal_impact']:,.2f}"
    )

    print("\nVIRTUAL OVERDOSE MONITORING")
    print("-" * 70)

    print(
        f"Program cost/quarter: "
        f"${results['nors']['operating_cost']:,.2f}"
    )

    print(
        "Projected healthcare savings: "
        "Not calculated."
    )

    print(
        f"Published savings/response: "
        f"${results['nors']['published_savings_per_response']:,.2f}"
    )

    print(
        f"Published BCR: "
        f"{results['nors']['published_benefit_cost_ratio']:.2f}"
    )

    print("\nNALOXONE FISCAL OUTCOMES")
    print("-" * 70)

    print(
        f"Baseline distribution rate: "
        f"{results['naloxone']['baseline_kits_per_100k']:,.2f} "
        f"kits/100k/quarter"
    )

    print(
        f"Projected distribution rate: "
        f"{results['naloxone']['projected_kits_per_100k']:,.2f} "
        f"kits/100k/quarter"
    )

    print(
        f"Additional distribution: "
        f"{results['naloxone']['incremental_kits_per_100k']:,.2f} "
        f"kits/100k/quarter"
    )

    print(
        f"Additional distribution cost: "
        f"${results['naloxone']['incremental_cost_per_100k']:,.2f} "
        f"per 100k/quarter"
    )

    print("\nFISCAL SUMMARY")
    print("-" * 70)

    print(
        f"SCS cost: "
        f"${fiscal['scs_operating_cost']:,.2f}"
    )

    print(
        f"SCS potential savings: "
        f"${fiscal['scs_potential_savings']:,.2f}"
    )

    print(
        f"SCS net fiscal impact: "
        f"${fiscal['scs_net_fiscal_impact']:,.2f}"
    )

    print(
        f"NORS program cost: "
        f"${fiscal['nors_program_cost']:,.2f}"
    )

    print(
        f"Naloxone additional cost/100k: "
        f"${fiscal['naloxone_additional_cost_per_100k']:,.2f}"
    )

    print()
    print("=" * 70)
    """