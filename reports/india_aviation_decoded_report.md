# India Aviation Decoded: A Decade of Domestic Air Travel (2015-2026)

**Data source:** Directorate General of Civil Aviation (DGCA), Ministry of Civil Aviation, India  
**Compiled via:** Vonter/india-aviation-traffic (GitHub)  
**Analysis period:** 2015 to 2026 (partial year)  
**Analyst:** Viba Mahesh, IESEG School of Management

---

## What this project is

This project takes a decade of raw government data on India's domestic aviation sector and runs a structured analytical pipeline across it to surface patterns that are difficult to see by looking at the numbers manually.

The raw data comes as two separate files. One records monthly passenger volumes per airline from 2015 onwards. The other records monthly passenger volumes per route across all city pairs. Together, they cover 30 airlines, 1,910 unique domestic corridors, and over 1.35 billion passenger movements.

The analysis is built in Python across four scripts that run sequentially: cleaning the raw data, computing airline-level metrics (CAGR and volatility), computing route-level metrics (concentration and growth), and generating the output charts. Every number in this report is computed directly from the DGCA source files. No figures are manually estimated or sourced from secondary summaries.

---

## How the data was cleaned

The raw carrier file mixes four categories of flights together: scheduled domestic, scheduled international, non-scheduled domestic, and non-scheduled international. Non-scheduled covers charters and cargo. These were removed, leaving only commercial passenger flights on domestic routes. The file also includes pre-aggregated rows where DGCA has added its own industry totals. These were removed before any calculation, since leaving them in would cause every passenger to be counted twice when summing across airlines.

The route file had a structural problem where some corridors were logged in both directions in the same month, with inconsistent passenger numbers between the two entries. The fix was to treat every route as direction-agnostic: city names are sorted alphabetically to create one consistent label per corridor (so both DELHI-MUMBAI and MUMBAI-DELHI become DELHI-MUMBAI), and all passenger figures for that label within a given month are summed together. This reduced 2,122 directional entries to 1,910 unified corridors.

---

## Finding 1: IndiGo's decade-long consolidation of the market

IndiGo held 36.8% of the domestic scheduled market in 2015. By 2025 that figure had risen to 64.0%. No other airline in the dataset comes close to this trajectory.

The metric used to measure this is CAGR, or Compound Annual Growth Rate. Rather than simply comparing start and end passenger numbers, CAGR expresses total growth as an equivalent annual rate, which makes airlines of different ages and sizes directly comparable. IndiGo's CAGR over the 2015-2025 period works out to 13.7% per year.

What makes IndiGo's number meaningful is the context around it. Two airlines — Jet Airways and Go First — collapsed during this period. Their combined market share did not disappear; it was absorbed largely by IndiGo. The market share chart shows IndiGo's line accelerating its climb precisely around 2018-2019, when Jet Airways grounded, and again sustaining its dominance through the COVID recovery period.

SpiceJet, by contrast, shows a CAGR of -6.8% over the same decade, making it the only major scheduled carrier with negative long-term growth in passenger volume. This is consistent with SpiceJet's widely reported financial difficulties across the same period.

A methodological note: CAGR calculations in this project only use years where all 12 months of data are reported. Partial years are excluded as endpoints because using them would distort the rate — a partial year captures lower cumulative passengers than a full year would, which compresses the computed growth rate relative to the true one, or overstates decline.

---

## Finding 2: Volatility as an early warning signal — but only for Jet Airways

The hypothesis going into this analysis was that airlines in financial distress would show rising instability in their monthly passenger numbers before they collapsed. The idea is that operational problems — groundings, route cuts, capacity uncertainty — would show up as erratic month-to-month swings before the final exit.

To test this, a volatility metric was computed for every airline: the 6-month rolling standard deviation of month-over-month percentage change in passenger numbers. Percentage change was used rather than raw numbers so that airlines of different sizes are comparable. A 100,000 passenger swing means something very different for IndiGo versus Star Air.

The results split cleanly into two cases.

For Jet Airways, the hypothesis holds. Volatility remained low and stable — typically between 3 and 7 — from 2015 through early 2018. Starting in February 2019 it began rising sharply, climbing through 10, then 21, then 34, then 42 in the final months before the airline grounded its fleet in April 2019. This is a genuine, computable early warning signal, visible several months before the exit.

For Go First, the hypothesis does not hold. The biggest volatility spikes in Go First's data occur in 2020 and 2021, nearly two years before its bankruptcy filing in May 2023. These spikes reflect the COVID-19 disruption, which affected every airline simultaneously, not Go First specifically. In the 12 months immediately before the bankruptcy, Go First's volatility was actually declining, sitting at relatively low levels right up to the filing. A single spike appears in May 2023 — but that is the collapse itself being recorded, not a precursor to it.

Go First's exit was driven by externally reported factors including grounded aircraft and an engine supplier dispute, which is consistent with a sudden event rather than a gradual operational deterioration. The data reflects this: there was no extended period of increasing instability to detect beforehand.

The honest conclusion is that volatility-based monitoring would have flagged Jet Airways with enough lead time to act, but would not have provided meaningful advance warning for Go First. Both cases are presented separately rather than combined into a single claim, because the data only supports the hypothesis for one of them.

---

## Finding 3: India's aviation network is more concentrated than the 80/20 rule suggests

After removing 233 dormant or near-dormant routes (those with fewer than 100 total passengers across the entire decade), the analysis covers 1,677 routes representing genuine commercial demand.

The concentration finding:

- The top 10 routes (0.6% of the network) carry 22.5% of all domestic passenger traffic
- The top 50 routes (3.0% of the network) carry 55.2%
- The top 100 routes (6.0% of the network) carry 73.3%
- The top 200 routes (11.9% of the network) carry 87.9%

The classic Pareto principle predicts 20% of inputs causing 80% of outputs. Indian aviation runs significantly tighter than that. 6% of routes carry 73% of traffic, which is closer to a 94/6 split than an 80/20 split.

Every one of the top 10 routes connects at least one of three cities: Delhi, Mumbai, or Bengaluru. Delhi-Mumbai alone, at 61.5 million passengers across the decade, accounts for 4.6% of all domestic traffic by itself.

The implication is structural: India's aviation network is heavily spine-dependent. A disruption to even a small number of metro-to-metro corridors would affect a disproportionate share of total national air travel. Regional connectivity schemes have added many routes to the network over this period, but most of them sit in the long tail — 500 routes are required to reach 97.6% of total traffic, meaning the last 1,177 routes collectively account for only 2.4%.

This metric is computed using a cumulative sum: routes are ranked by total decade passengers, a running total is computed as each successive route is added, and that running total is expressed as a percentage of the grand total. This is standard concentration analysis methodology, sometimes called a Lorenz curve approach.

---

## Finding 4: The fastest-growing corridors are not the ones you'd expect

Route-level CAGR was computed for routes meeting two conditions: at least 8 distinct years in the dataset, and a minimum span of 6 years between the first and last qualifying year. The second condition was added after an initial version of the calculation produced Mumbai-Port Blair at 185% annual growth — which on inspection turned out to be based on only 2022 and 2023, two complete years sitting inside a decade of otherwise patchy reporting for that route. Accepting it would have made a 1-year growth rate appear to be a long-term trend.

After applying the corrected methodology, 339 routes have a valid long-term CAGR.

The fastest-growing route in the dataset is Chennai-Ranchi at 94.7% annual growth over 2018-2025. This is followed by Hyderabad-Udaipur at 54.5%, Bagdogra-Hyderabad at 52.3%, and Bengaluru-Dehra Dun at 50.7%.

The pattern across the top 15 fastest-growing routes is consistent: these are connections between tier-2 cities and major southern or northern hubs, not connections between already-saturated metro pairs. Routes like Delhi-Mumbai are the backbone of the network but their growth is moderate — the demand is already there and well-served. The high growth routes are corridors that barely existed five years ago and are now growing rapidly as regional connectivity improves and middle-income air travel expands into non-metro markets.

This is directly relevant to airport capacity planning and airline network strategy: the routes with the most growth headroom are not the ones that already dominate the traffic tables.

---

## Who this analysis is useful for

An aviation market researcher or policy analyst at AAI, DGCA, or a think tank would find the route concentration finding directly relevant to discussions about connectivity equity — specifically, how much of India's aviation growth actually reaches tier-2 and tier-3 markets versus remaining concentrated in metro corridors.

An airline strategy team would find the fastest-growing routes analysis relevant for network planning, since these are corridors with demonstrated demand growth over a sustained period from government-sourced data.

A risk or operations researcher would find the volatility finding relevant as a starting point for thinking about operational health monitoring — with the important caveat that the methodology flagged one airline correctly and missed another, which tells you something about the limits of passenger-data-based monitoring for supply-side collapse events.

Anyone working in Indian aviation would find the COVID impact numbers grounding: domestic traffic fell 56.4% from 2019 to 2020, dropping from 143.7 million passengers to 62.7 million. Recovery to pre-COVID levels happened by 2023, and 2025 set a new record at 167.1 million domestic passengers.

---

## Limitations

The carrier file and route file cannot be joined at the airline-route level. There is no way, from this data, to determine which airline operated which specific route. The two layers of analysis — airline performance and route network structure — are parallel views of the same period, not a merged dataset.

All CAGR figures are computed from the first to the last complete year of data for each entity. Partial years are excluded. This means some airlines or routes with strong recent growth may show lower CAGRs than their most recent trajectory would suggest, because the calculation is anchored to their earliest available full year.

Volatility figures are directional and based on monthly passenger counts. They reflect demand-side instability, not supply-side operational metrics. An airline can have highly volatile passenger numbers for external reasons (seasonality, COVID, competitor entry) that have nothing to do with its own financial health.
