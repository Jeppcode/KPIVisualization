# Waves of Change: KPI Ripple Effect for Retail

Interactive Streamlit app that demonstrates how small changes in key store KPIs can create large effects over a full year. Adjust a few sliders and see instant changes in purchases, revenue, products sold, and profit.

## Features
- Two column layout for minimal scrolling: inputs on the left, results on the right  
- Base KPI settings: yearly visitors, hitrate, average purchase value (SEK), products per customer, profit margin  
- Scenario adjustments: additive change in hitrate (percentage points), average purchase (SEK), and products per customer  
- Live KPI cards and a compact results table  
- Altair bar chart with fixed Y scale and conditional colors  
  - Green for positive change  
  - Red for negative change  
- One click reset of scenario adjustments

## How it calculates
- **Purchases** = visitors × hitrate  
- **Revenue** = purchases × average purchase value  
- **Products sold** = purchases × products per customer  
- **Profit** = revenue × profit margin

## Public URL
https://kpiimpact.streamlit.app/

## Quick start
```bash
pip install streamlit pandas altair
streamlit run Project.py
```

## Usage
1. Set base KPI values in the left column.  
2. Adjust the scenario sliders to test what if changes.  
3. Read the KPI cards and the results table on the right.  
4. Review the bar chart to see direction and magnitude.  
5. Click **Reset to base scenario** to clear all adjustments.


## Requirements
- Python 3.9 or newer  
- Packages: `streamlit`, `pandas`, `altair`



