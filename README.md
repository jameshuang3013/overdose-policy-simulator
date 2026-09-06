# Overdose Policy Simulator

## Project Overview

The Overdose Policy Simulator is an AI-augmented analytical tool designed to help policymakers evaluate the potential cost and financial impacts of overdose prevention and harm reduction interventions in Canada.

The simulator allows users to independently adjust implementation levels for three interventions:

- Supervised Consumption Services (SCS)
- Virtual Overdose Monitoring
- Naloxone Distribution

The model uses Canadian historical data and evidence-based cost estimates to calculate projected intervention costs, healthcare savings, and net financial impacts.

## Data

The project uses Canadian data covering approximately 2020–2024, including:

- Opioid-related deaths
- Hospitalizations
- Emergency department visits
- Emergency medical service responses
- Supervised consumption service visits and activities
- SCS and OPS site counts
- Naloxone kits distributed per 100,000 population

The raw datasets are stored in `data/raw/`, while cleaned and integrated datasets are stored in `data/processed/`.

## Simulation Model

The simulator uses the 2024 quarterly average as the baseline.

Users can independently select an implementation rate from 0% to 100% for each intervention.

The model estimates:

- Projected SCS activity and operating costs
- Avoided emergency-service costs associated with SCS
- Projected virtual monitoring responses and healthcare savings
- Projected naloxone distribution and associated costs
- Net financial impacts

The model does not assume a universal reduction in mortality or hospitalizations where a sufficiently direct intervention-specific estimate was not available.
