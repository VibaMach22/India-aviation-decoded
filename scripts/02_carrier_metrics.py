"""
Airline-level metrics: CAGR and volatility.

CAGR (Compound Annual Growth Rate) tells us how fast an airline's
passenger volume has genuinely grown per year, on average, accounting
for compounding - not just a simple start-to-end percentage change.

Volatility tells us how unstable an airline's month-to-month passenger
numbers have been. The hypothesis we're testing: did Jet Airways and
Go First show rising volatility in the months before they collapsed,
or is that narrative not actually supported by the numbers.
"""

import pandas as pd
import numpy as np

carrier = pd.read_csv('../data/carrier_cleaned.csv')

# ---------------------------------------------------------------
# PART 1: CAGR per airline, using only complete years
# ---------------------------------------------------------------

# First, identify which years are actually complete (12 months reported)
# for each airline. We will not use partial years as CAGR endpoints,
# since that would distort the growth rate.
months_per_year = carrier.groupby(['Airline', 'Year']).size().reset_index(name='months')
complete_years = months_per_year[months_per_year['months'] == 12]

# Build annual passenger totals, but only keep airline-year combinations
# where the year was complete.
annual = carrier.groupby(['Airline', 'Year'])['Passenger Number'].sum().reset_index()
annual = annual.merge(complete_years[['Airline', 'Year']], on=['Airline', 'Year'])

def calculate_cagr(group):
    """
    For a single airline's annual totals, find the earliest and latest
    complete year, then compute CAGR between them.
    Formula: (End Value / Start Value)^(1/num_years) - 1
    """
    group = group.sort_values('Year')
    if len(group) < 2:
        return pd.Series({'start_year': None, 'end_year': None,
                          'start_pax': None, 'end_pax': None, 'cagr_pct': None})

    start_year = group['Year'].iloc[0]
    end_year = group['Year'].iloc[-1]
    start_pax = group['Passenger Number'].iloc[0]
    end_pax = group['Passenger Number'].iloc[-1]
    num_years = end_year - start_year

    if num_years == 0 or start_pax <= 0:
        return pd.Series({'start_year': start_year, 'end_year': end_year,
                          'start_pax': start_pax, 'end_pax': end_pax, 'cagr_pct': None})

    cagr = ((end_pax / start_pax) ** (1 / num_years) - 1) * 100
    return pd.Series({'start_year': start_year, 'end_year': end_year,
                      'start_pax': start_pax, 'end_pax': end_pax, 'cagr_pct': round(cagr, 2)})

cagr_results = annual.groupby('Airline').apply(calculate_cagr).reset_index()
cagr_results = cagr_results.dropna(subset=['cagr_pct']).sort_values('cagr_pct', ascending=False)

print("CAGR by airline (complete years only):")
print(cagr_results.to_string(index=False))

cagr_results.to_csv('../analysis/airline_cagr.csv', index=False)
print("\nSaved: analysis/airline_cagr.csv")

# ---------------------------------------------------------------
# PART 2: Volatility - testing the pre-collapse instability theory
# ---------------------------------------------------------------
# Volatility here is the rolling 6-month standard deviation of
# month-over-month percentage change in passenger numbers, normalized
# so it is comparable across airlines of very different sizes.
#
# A small, stable airline and a huge, stable airline should both show
# LOW volatility despite different absolute passenger counts. That is
# why we use percentage change, not raw passenger numbers, as the
# input to the volatility calculation.

def add_volatility(df):
    df = df.sort_values(['Year', 'Month']).reset_index(drop=True)
    df['pct_change'] = df['Passenger Number'].pct_change() * 100
    # Rolling 6-month standard deviation of that percentage change.
    # A spike in this number means the airline's month-to-month
    # passenger swings have become unusually large and erratic.
    df['volatility_6mo'] = df['pct_change'].rolling(window=6, min_periods=3).std()
    return df

carrier_sorted = carrier.sort_values(['Airline', 'Year', 'Month'])
# include_groups=False would drop Airline, so instead we apply per-group
# manually and reattach the Airline column ourselves to avoid the
# version-dependent groupby behavior that silently drops it.
pieces = []
for airline_name, group in carrier_sorted.groupby('Airline'):
    piece = add_volatility(group)
    piece['Airline'] = airline_name
    pieces.append(piece)
volatility_df = pd.concat(pieces, ignore_index=True)

# Now specifically pull out Jet Airways and Go First in their final
# 12 months of operation, to see whether volatility actually rose
# before each airline's exit - this is the direct test of the
# hypothesis, using real computed numbers, not assumption.

jet_final = volatility_df[
    (volatility_df['Airline'] == 'Jet Airways')
].tail(12)

gofirst_final = volatility_df[
    (volatility_df['Airline'] == 'Go First')
].tail(12)

print("\n" + "="*60)
print("Jet Airways - final 12 months before exit:")
print(jet_final[['Year', 'Month', 'Passenger Number', 'pct_change', 'volatility_6mo']].to_string(index=False))

print("\n" + "="*60)
print("Go First - final 12 months before exit:")
print(gofirst_final[['Year', 'Month', 'Passenger Number', 'pct_change', 'volatility_6mo']].to_string(index=False))

volatility_df.to_csv('../analysis/airline_volatility.csv', index=False)
print("\nSaved: analysis/airline_volatility.csv")
