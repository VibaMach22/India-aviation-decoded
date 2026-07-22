"""
Data cleaning pipeline for India Aviation Decoded project.
Loads raw DGCA carrier and route data, cleans it, and outputs
analysis-ready CSVs for the metrics scripts to use.
"""

import pandas as pd
import numpy as np

# ---------------------------------------------------------------
# STEP 1: Load carrier-level data
# ---------------------------------------------------------------
print("Loading carrier data...")
carrier = pd.read_csv('../data/domestic_carrier.csv')

# Keep only ScheduledDomestic - these are real commercial flights.
# NonScheduled = charters/cargo, not relevant to passenger market share.
# We also drop 'Total Domestic' and 'Total International' rows since
# those are pre-aggregated totals, not individual airlines - including
# them would double-count if we ever sum across the Airline column.
carrier = carrier[carrier['Type'] == 'ScheduledDomestic']
carrier = carrier[~carrier['Airline'].isin(['Total Domestic', 'Total International'])]

# Convert Year and Month to proper numeric types, then build a single
# sortable date-like column. Month is currently a zero-padded string
# like '01', '02' - this turns it into something we can sort and group on.
carrier['Year'] = carrier['Year'].astype(int)
carrier['Month'] = carrier['Month'].astype(int)
carrier['Passenger Number'] = pd.to_numeric(carrier['Passenger Number'], errors='coerce')

print(f"Carrier data after filtering: {len(carrier)} rows")
print(f"Airlines remaining: {carrier['Airline'].nunique()}")
print(carrier[['Airline', 'Year', 'Month', 'Passenger Number']].head())

# ---------------------------------------------------------------
# STEP 2: Load and clean route (city-pair) data
# ---------------------------------------------------------------
print("\n" + "="*60)
print("Loading route data...")
routes = pd.read_csv('../data/domestic_city.csv')

routes['Year'] = routes['Year'].astype(int)
routes['Month'] = routes['Month'].astype(int)
routes['PaxToCity2'] = pd.to_numeric(routes['PaxToCity2'], errors='coerce').fillna(0)
routes['PaxFromCity2'] = pd.to_numeric(routes['PaxFromCity2'], errors='coerce').fillna(0)

# THE DIRECTION PROBLEM:
# The raw data sometimes logs "DELHI -> MUMBAI" and "MUMBAI -> DELHI"
# as two separate rows in the same month, with inconsistent completeness
# (we saw this directly: one row had ~300k passengers, the paired
# reverse-direction row had ~3.6k - almost certainly a reporting
# artifact, not real traffic).
#
# Fix: treat each route as direction-agnostic. We build a 'RoutePair'
# key by alphabetically sorting the two city names, so DELHI-MUMBAI
# and MUMBAI-DELHI become the same key. Then we sum total passenger
# movement (both directions, both columns) per RoutePair per month.
# This trades direction-level detail for route-level reliability,
# which is the right tradeoff given the data quality issue we found.

routes['RoutePair'] = routes.apply(
    lambda r: ' - '.join(sorted([str(r['City1']), str(r['City2'])])),
    axis=1
)
routes['TotalPax'] = routes['PaxToCity2'] + routes['PaxFromCity2']

# Now group by the unified RoutePair + Year + Month, summing TotalPax.
# This merges any duplicate-direction rows into one true total per route per month.
routes_clean = routes.groupby(['RoutePair', 'Year', 'Month'], as_index=False)['TotalPax'].sum()

print(f"Route data after cleaning: {len(routes_clean)} rows")
print(f"Unique routes (direction-merged): {routes_clean['RoutePair'].nunique()}")
print(routes_clean.head())

# ---------------------------------------------------------------
# STEP 3: Save cleaned outputs
# ---------------------------------------------------------------
# These cleaned files are what every subsequent script will load.
# Nobody downstream touches the raw CSVs again - this is the single
# source of truth from here forward.

carrier.to_csv('../data/carrier_cleaned.csv', index=False)
routes_clean.to_csv('../data/routes_cleaned.csv', index=False)

print("\n" + "="*60)
print("Saved: data/carrier_cleaned.csv")
print("Saved: data/routes_cleaned.csv")
