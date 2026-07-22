"""
Route-level metrics: Pareto concentration and route CAGR.

Pareto concentration answers a real structural question about Indian
aviation: is demand spread fairly evenly across hundreds of routes, or
does a small number of corridors carry most of the traffic. This has
direct relevance to how airlines allocate aircraft and how airports
plan capacity.

Route CAGR identifies which specific corridors have grown fastest over
the decade, restricted to routes with enough history for the number to
be meaningful rather than noise from a route that only existed for two
years.
"""

import pandas as pd
import numpy as np

routes = pd.read_csv('../data/routes_cleaned.csv')

# ---------------------------------------------------------------
# PART 1: Pareto concentration
# ---------------------------------------------------------------
# Exclude routes with negligible total traffic across the full decade.
# These are routes that were registered (often under regional
# connectivity schemes) but never carried meaningful passenger volume.
# Including them would understate real concentration, since they pad
# the denominator (total route count) without representing genuine
# demand.

route_totals = routes.groupby('RoutePair')['TotalPax'].sum().reset_index()
route_totals = route_totals[route_totals['TotalPax'] >= 100]
route_totals = route_totals.sort_values('TotalPax', ascending=False).reset_index(drop=True)

total_traffic = route_totals['TotalPax'].sum()
route_totals['cumulative_pax'] = route_totals['TotalPax'].cumsum()
route_totals['cumulative_pct'] = (route_totals['cumulative_pax'] / total_traffic) * 100
route_totals['route_rank'] = route_totals.index + 1

n_routes = len(route_totals)
print(f"Routes with meaningful traffic (100+ passengers over the decade): {n_routes}")
print(f"Total decade passenger movements across these routes: {total_traffic:,.0f}")

# Find what share of total traffic specific top-N route counts represent
for n in [10, 20, 50, 100, 200]:
    pct = route_totals.iloc[n-1]['cumulative_pct']
    print(f"Top {n} routes ({n/n_routes*100:.1f}% of all routes) carry {pct:.1f}% of total traffic")

route_totals.to_csv('../analysis/route_pareto.csv', index=False)
print("\nSaved: analysis/route_pareto.csv")

# ---------------------------------------------------------------
# PART 2: Route-level CAGR, restricted to routes with real history
# ---------------------------------------------------------------
# A route that only existed for two years cannot produce a meaningful
# CAGR - a young route can show enormous percentage growth simply
# because it started from almost nothing. We restrict this calculation
# to routes with at least 8 distinct years of data, matching the
# threshold we identified during initial data exploration.

route_years = routes.groupby('RoutePair')['Year'].nunique().reset_index(name='years_active')
long_routes = route_years[route_years['years_active'] >= 8]['RoutePair'].tolist()

routes_long = routes[routes['RoutePair'].isin(long_routes)]
annual_route = routes_long.groupby(['RoutePair', 'Year'])['TotalPax'].sum().reset_index()

# Also require the year be reasonably complete - at least 10 of 12
# months reported, to avoid a partial year distorting the start or
# end point of the CAGR calculation, same logic as the airline CAGR.
months_per_route_year = routes_long.groupby(['RoutePair', 'Year']).size().reset_index(name='months')
complete_route_years = months_per_route_year[months_per_route_year['months'] >= 10]
annual_route = annual_route.merge(complete_route_years[['RoutePair', 'Year']], on=['RoutePair', 'Year'])

def calculate_route_cagr(group):
    group = group.sort_values('Year')
    # Require a real multi-year span, not just two scattered complete
    # years from a route with mostly sparse reporting. We check that
    # the gap between the actual first and last complete year is at
    # least 6 years, ensuring this reflects genuine long-term history
    # rather than two incidentally-complete years years apart in time
    # from each other but close together within a sparse decade.
    if len(group) < 2:
        return pd.Series({'start_year': None, 'end_year': None, 'cagr_pct': None, 'span_years': None})

    start_year = group['Year'].iloc[0]
    end_year = group['Year'].iloc[-1]
    span = end_year - start_year

    if span < 6:
        return pd.Series({'start_year': start_year, 'end_year': end_year, 'cagr_pct': None, 'span_years': span})

    start_pax = group['TotalPax'].iloc[0]
    end_pax = group['TotalPax'].iloc[-1]
    if start_pax <= 0:
        return pd.Series({'start_year': start_year, 'end_year': end_year, 'cagr_pct': None, 'span_years': span})

    cagr = ((end_pax / start_pax) ** (1 / span) - 1) * 100
    return pd.Series({'start_year': start_year, 'end_year': end_year, 'cagr_pct': round(cagr, 2), 'span_years': span})

route_cagr = annual_route.groupby('RoutePair').apply(calculate_route_cagr).reset_index()
route_cagr = route_cagr.dropna(subset=['cagr_pct'])

print(f"\nRoutes with valid long-term CAGR calculated (6+ year genuine span): {len(route_cagr)}")
print("\nTop 15 fastest-growing routes:")
print(route_cagr.sort_values('cagr_pct', ascending=False).head(15).to_string(index=False))

print("\nBottom 10 declining routes:")
print(route_cagr.sort_values('cagr_pct').head(10).to_string(index=False))

route_cagr.to_csv('../analysis/route_cagr.csv', index=False)
print("\nSaved: analysis/route_cagr.csv")
