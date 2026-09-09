# Overdose Policy Fiscal Simulator

## Project Overview

The Overdose Policy Fiscal Simulator is an analytical tool designed to help policymakers evaluate the potential cost and financial impacts of overdose prevention and harm reduction interventions in Canada.

The simulator allows users to independently adjust implementation levels for three interventions:

- Supervised Consumption Services (SCS)
- Virtual Overdose Monitoring
- Naloxone Distribution

The model uses Canadian historical data and evidence-based cost estimates to calculate projected intervention costs, healthcare savings, and net financial impacts.

To run the simulator:

1. Clone the repository

Open a terminal and run:

git clone https://github.com/jameshuang3013/overdose-policy-simulator.git

Then move into the project folder:

cd overdose-policy-simulator
2. Install the required packages

Run:

python -m pip install pandas matplotlib streamlit
3. Run the simulator

Start the Streamlit application with:

python -m streamlit run src/app.py

The application will open in your web browser.
