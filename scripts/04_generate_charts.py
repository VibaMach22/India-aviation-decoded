"""
Generates the market share evolution chart as a standalone image,
replicating what was built in Power BI before the canvas issue.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

market_share = pd.read_csv('../analysis/market_share_by_year.csv')

# Same airline selection used in the Power BI filter
focus_airlines = ['IndiGo', 'Jet Airways', 'Go First', 'SpiceJet', 'Air India', 'Vistara', 'Akasa Air']
data = market_share[market_share['Airline'].isin(focus_airlines)]

# Colors chosen to be distinct and readable, IndiGo gets the standout teal
colors = {
    'IndiGo': '#1ABC9C',
    'Jet Airways': '#27AE60',
    'Go First': '#D4AC0D',
    'SpiceJet': '#9B59B6',
    'Air India': '#E91E8C',
    'Vistara': '#8B6914',
    'Akasa Air': '#3498DB'
}

fig, ax = plt.subplots(figsize=(12, 7))

for airline in focus_airlines:
    airline_data = data[data['Airline'] == airline].sort_values('Year')
    ax.plot(airline_data['Year'], airline_data['MarketSharePct'],
            label=airline, color=colors[airline], linewidth=2.5, marker='o', markersize=4)

ax.set_title("India's Aviation Power Shift: Market Share (2015-2026)",
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Market Share (%)', fontsize=12)
ax.legend(loc='upper left', ncol=4, frameon=False, fontsize=10)
ax.grid(True, linestyle='--', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.yaxis.set_major_formatter(mticker.PercentFormatter())

plt.tight_layout()
plt.savefig('../visuals/market_share_evolution.png', dpi=200, bbox_inches='tight')
print("Saved: visuals/market_share_evolution.png")

# ---------------------------------------------------------------
# CHART 2: Jet Airways vs Go First volatility comparison
# ---------------------------------------------------------------

volatility = pd.read_csv('../analysis/airline_volatility.csv')

# Build a proper time axis using Year + Month, since the volatility
# data is monthly, not annual like market share
volatility['date'] = pd.to_datetime(volatility['Year'].astype(str) + '-' +
                                      volatility['Month'].astype(str).str.zfill(2) + '-01')

jet = volatility[volatility['Airline'] == 'Jet Airways'].sort_values('date')
gofirst = volatility[volatility['Airline'] == 'Go First'].sort_values('date')

fig, ax = plt.subplots(figsize=(12, 7))

ax.plot(jet['date'], jet['volatility_6mo'], label='Jet Airways',
        color='#27AE60', linewidth=2.5)
ax.plot(gofirst['date'], gofirst['volatility_6mo'], label='Go First',
        color='#3498DB', linewidth=2.5)

# Mark the actual exit points with vertical lines, since this is the
# whole point of the chart - showing what happened right before each
ax.axvline(pd.Timestamp('2019-04-01'), color='#27AE60', linestyle=':', alpha=0.6, linewidth=1.5)
ax.text(pd.Timestamp('2019-05-01'), ax.get_ylim()[1]*0.92, 'Jet Airways\ngrounded',
        fontsize=9, color='#27AE60')

ax.axvline(pd.Timestamp('2023-05-01'), color='#3498DB', linestyle=':', alpha=0.6, linewidth=1.5)
ax.text(pd.Timestamp('2023-06-01'), ax.get_ylim()[1]*0.92, 'Go First\nfiles for bankruptcy',
        fontsize=9, color='#3498DB')

ax.set_title("Did Instability Predict Collapse? Jet Airways vs Go First",
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('')
ax.set_ylabel('6-Month Rolling Volatility (% points)', fontsize=12)
ax.legend(loc='upper left', frameon=False, fontsize=11)
ax.grid(True, linestyle='--', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('../visuals/volatility_comparison.png', dpi=200, bbox_inches='tight')
print("Saved: visuals/volatility_comparison.png")

# ---------------------------------------------------------------
# CHART 3: Airline CAGR comparison — horizontal bar chart
# ---------------------------------------------------------------
import matplotlib.patches as mpatches

cagr = pd.read_csv('../analysis/airline_cagr.csv')

# Exclude tiny/cargo operators that distort scale, keep commercially relevant ones
exclude = ['Blue Dart Aviation', 'QuikJet Cargo', 'India One Air',
           'Air Heritage', 'Air Taxi', 'Pawan Hans', 'Zoom Air',
           'Air Odisha', 'Air Pegasus', 'Air Carnival', 'Air Deccan']
cagr = cagr[~cagr['Airline'].isin(exclude)].sort_values('cagr_pct')

colors = ['#E74C3C' if x < 0 else '#2ECC71' if x > 20 else '#3498DB'
          for x in cagr['cagr_pct']]

fig, ax = plt.subplots(figsize=(11, 7))
bars = ax.barh(cagr['Airline'], cagr['cagr_pct'], color=colors, height=0.6)

# Add value labels on each bar
for bar, val in zip(bars, cagr['cagr_pct']):
    ax.text(val + 0.5, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}%', va='center', fontsize=9)

ax.axvline(0, color='black', linewidth=0.8)
ax.set_title('Airline Passenger CAGR — Full Operating Period',
             fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('CAGR (%)', fontsize=11)
ax.grid(axis='x', linestyle='--', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

legend_elements = [
    mpatches.Patch(color='#2ECC71', label='High growth (>20%)'),
    mpatches.Patch(color='#3498DB', label='Moderate growth'),
    mpatches.Patch(color='#E74C3C', label='Decline')
]
ax.legend(handles=legend_elements, loc='lower right', frameon=False, fontsize=9)

plt.tight_layout()
plt.savefig('../visuals/airline_cagr_comparison.png', dpi=200, bbox_inches='tight')
print("Saved: visuals/airline_cagr_comparison.png")

# ---------------------------------------------------------------
# CHART 4: Route Pareto concentration curve
# ---------------------------------------------------------------
pareto = pd.read_csv('../analysis/route_pareto.csv')
total_routes = len(pareto)
pareto['route_pct'] = (pareto['route_rank'] / total_routes) * 100

fig, ax = plt.subplots(figsize=(11, 7))

ax.plot(pareto['route_pct'], pareto['cumulative_pct'],
        color='#2C3E50', linewidth=2.5)
ax.fill_between(pareto['route_pct'], pareto['cumulative_pct'],
                alpha=0.1, color='#2C3E50')

# Mark key thresholds
for route_n, label in [(10, 'Top 10'), (50, 'Top 50'), (100, 'Top 100')]:
    row = pareto[pareto['route_rank'] == route_n].iloc[0]
    x = row['route_pct']
    y = row['cumulative_pct']
    ax.plot(x, y, 'o', color='#E74C3C', markersize=7, zorder=5)
    ax.annotate(f'{label} routes\n{y:.1f}% of traffic',
                xy=(x, y), xytext=(x + 3, y - 8),
                fontsize=9, color='#E74C3C',
                arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1))

ax.set_title("Route Concentration: How Few Routes Carry How Much Traffic",
             fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Share of All Routes (%)', fontsize=11)
ax.set_ylabel('Cumulative Share of Total Passenger Traffic (%)', fontsize=11)
ax.grid(linestyle='--', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('../visuals/route_pareto_curve.png', dpi=200, bbox_inches='tight')
print("Saved: visuals/route_pareto_curve.png")

# ---------------------------------------------------------------
# CHART 5: Top 15 fastest-growing routes
# ---------------------------------------------------------------
route_cagr = pd.read_csv('../analysis/route_cagr.csv')
top15 = route_cagr.sort_values('cagr_pct', ascending=False).head(15)
top15 = top15.sort_values('cagr_pct')

# Clean up route names for readability
top15['RoutePair'] = top15['RoutePair'].str.title()

fig, ax = plt.subplots(figsize=(11, 8))
bars = ax.barh(top15['RoutePair'], top15['cagr_pct'],
               color='#1ABC9C', height=0.65)

for bar, val in zip(bars, top15['cagr_pct']):
    ax.text(val + 0.5, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}%', va='center', fontsize=9)

ax.set_title("Top 15 Fastest-Growing Domestic Routes (6+ Year Span)",
             fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Annual Growth Rate / CAGR (%)', fontsize=11)
ax.grid(axis='x', linestyle='--', alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('../visuals/top_growing_routes.png', dpi=200, bbox_inches='tight')
print("Saved: visuals/top_growing_routes.png")
