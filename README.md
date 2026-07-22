India Aviation Decoded: 10 Years, 30 Airlines, 2,100 Routes

A data pipeline and analysis of India's domestic aviation sector using a decade of DGCA data (2015-2026). Built to surface patterns in airline market structure, operational risk, and route network concentration that are not visible in aggregate industry summaries.

---

## Key findings

Market concentration: IndiGo's domestic market share rose from 36.8% in 2015 to 64.0% in 2025 — a climb that accelerated directly following Jet Airways' collapse in 2019 and Go First's in 2023.

Volatility as an early warning: A 6-month rolling volatility metric computed from monthly passenger data flagged Jet Airways months before its April 2019 grounding — volatility climbed from a stable range of 3-7 to above 40 in the final months. The same metric did not flag Go First, whose collapse was externally triggered and showed no extended prior instability.

Route concentration: 100 routes — 6% of the meaningful network — carry 73.3% of all domestic passenger traffic. The top 10 routes alone account for 22.5% of total traffic, and every one of them connects Delhi, Mumbai, or Bengaluru.

Regional growth corridors: The fastest-growing routes over a verified 6+ year window are not metro-to-metro. Chennai-Ranchi (94.7% CAGR), Hyderabad-Udaipur (54.5%), and Bagdogra-Hyderabad (52.3%) lead a list dominated by tier-2 city connections.

---

Data source

Raw data from the Directorate General of Civil Aviation (DGCA) and Ministry of Civil Aviation, aggregated by [Vonter/india-aviation-traffic](https://github.com/Vonter/india-aviation-traffic).

Two files used:
- `domestic_carrier.csv` — monthly passenger volumes per airline (2015-2026)
- `domestic_city.csv` — monthly passenger volumes per city pair (2015-2026)

Place both in the `/data` folder before running the pipeline.

---

How to run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the pipeline in order
python scripts/01_clean_data.py
python scripts/02_carrier_metrics.py
python scripts/03_route_metrics.py
python scripts/04_generate_charts.py
```

Each script reads from the previous step's outputs. Running them out of order will fail. The full pipeline takes under 30 seconds on any modern machine.

---

Repository structure

```
data/
  domestic_carrier.csv       # Raw DGCA carrier data (download separately)
  domestic_city.csv          # Raw DGCA route data (download separately)
  carrier_cleaned.csv        # Output of 01_clean_data.py
  routes_cleaned.csv         # Output of 01_clean_data.py

scripts/
  01_clean_data.py           # Filters, type-converts, fixes route direction bug
  02_carrier_metrics.py      # CAGR and volatility per airline
  03_route_metrics.py        # Pareto concentration and CAGR per route
  04_generate_charts.py      # Generates all five output charts

analysis/
  airline_cagr.csv           # CAGR per airline, complete years only
  airline_volatility.csv     # Monthly volatility scores per airline
  market_share_by_year.csv   # Annual market share per airline
  route_pareto.csv           # Ranked routes with cumulative traffic share
  route_cagr.csv             # CAGR per route, 6+ year span only

visuals/
  market_share_evolution.png
  volatility_comparison.png
  airline_cagr_comparison.png
  route_pareto_curve.png
  top_growing_routes.png

reports/
  METHODOLOGY.md             # Analytical decisions, assumptions, known limitations
  india_aviation_decoded_report.md  # Full findings report
```

---

Methodology notes

CAGR is computed only between complete calendar years (12 months reported). Partial years are excluded as endpoints since they systematically distort the computed rate in the direction of the trend.

Route CAGR requires a minimum 6-year span between first and last qualifying year. An early version of this calculation produced Mumbai-Port Blair at 185% CAGR based on two adjacent complete years inside a decade of otherwise patchy data. The span filter removes these distortions.

Volatility is the 6-month rolling standard deviation of month-over-month percentage change. Percentage change is used rather than absolute passenger numbers so that airlines of different sizes are comparable on the same scale.

Full methodology, including data quality issues found and how they were handled, is in `reports/METHODOLOGY.md`.

---

## About

Built by Viba Mahesh — International Business student at IESEG School of Management (France), interning in Supply Chain & Operations at Grundfos Pumps India.

[LinkedIn](https://linkedin.com/in/your-link-here) | [GitHub](https://github.com/VibaMach22)

