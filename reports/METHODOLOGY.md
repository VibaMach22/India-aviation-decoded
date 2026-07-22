# Methodology

This document explains how the numbers in this project were calculated, what assumptions were made, and where the data had problems that needed fixing before any analysis could happen.

## Data source

All data comes from the Directorate General of Civil Aviation (DGCA) and Ministry of Civil Aviation, aggregated and made available through a public GitHub repository (Vonter/india-aviation-traffic). Two files were used:

A carrier-level file with monthly passenger numbers per airline from 2015 to 2026, covering both scheduled and non-scheduled domestic and international traffic.

A route-level file with monthly passenger movements between city pairs over the same period, covering 2,122 directional route entries.

## Cleaning steps

The carrier file was filtered down to Scheduled Domestic flights only. Non-scheduled flights are mostly charters and cargo operations, which would distort any passenger market share calculation if mixed in with commercial airline traffic. Two pre-aggregated rows, "Total Domestic" and "Total International," were also removed, since these are DGCA's own summary totals rather than individual airlines. Leaving them in would risk double-counting if the Airline column is ever summed directly.

The route file had a data quality issue that needed fixing before any route-level calculation would be reliable. Some city pairs were logged twice in the same month, once in each direction (for example, "Delhi to Mumbai" and "Mumbai to Delhi" as separate rows), and the two rows often had very different passenger counts for what should be roughly the same volume of travel. Checking a few cases directly showed clear reporting inconsistency rather than genuine asymmetric demand. To handle this, every route was treated as direction-agnostic: the two city names were sorted alphabetically into one consistent key, and passenger numbers from both directions and both raw columns were summed into a single monthly total per route. This reduced the dataset from 2,122 directional entries to 1,910 unified routes.

After cleaning, 1,753 carrier-month rows and 64,480 route-month rows remained as the basis for everything that follows.

## CAGR (Compound Annual Growth Rate)

CAGR was used to measure long-term growth per airline and per route. The formula used is the standard one: (End Value divided by Start Value) raised to the power of (1 divided by number of years), minus one.

A complication came up almost immediately. Several years in the dataset are not fully reported, either because an airline started or exited mid-year, or because data collection for the most recent year is still ongoing. Using a partial year as a CAGR start or end point would distort the result, since growth would be compared between a full year of traffic and a few months of traffic. To avoid this, only years with all 12 months reported were used as valid CAGR endpoints for airlines.

The same logic applies to routes, with a slightly looser threshold of 10 or more months reported, since route-level reporting is sparser than airline-level reporting across the dataset.

A second issue surfaced during the route CAGR calculation specifically. Several routes have scattered, incomplete reporting across the decade, where only two or three years happen to be fully complete, sometimes positioned close together in time rather than spanning the route's actual history. An early version of this calculation picked up Mumbai-Port Blair as the fastest-growing route in the dataset at 185 percent annual growth, which on inspection turned out to be based on just 2022 and 2023, two complete years sitting inside a decade of otherwise sparse, partial reporting for that route. The fix was to require a genuine span of at least 6 years between the first and last complete year used, not just any two complete years that happened to exist. This dropped the number of routes with a valid long-term CAGR from over 400 down to 339, and removed several similarly distorted results along with Mumbai-Port Blair.

## Volatility

Volatility was calculated as the rolling 6-month standard deviation of month-over-month percentage change in passenger numbers, applied separately to each airline. Percentage change was used rather than raw passenger numbers so that volatility is comparable across airlines of very different sizes. A large airline and a small airline can both register as "stable" if their relative month-to-month swings are both small, even though their absolute passenger counts are nothing alike.

This metric was used specifically to test whether Jet Airways and Go First, India's two most significant airline collapses in this dataset's time window, showed rising instability before they stopped operating, or whether that is a narrative applied after the fact without real support in the numbers.

The two cases turned out differently. Jet Airways' volatility stayed low and steady through most of 2018, then rose sharply starting in February 2019, climbing from roughly 4 to over 40 by the time the airline grounded its last flights in April 2019. This is a genuine early warning pattern, visible months in advance in the raw passenger numbers.

Go First's volatility does not show the same pattern. It was actually at its highest in mid-2022, nearly a year before the airline's bankruptcy filing, and had been declining steadily through early 2023, the months immediately preceding the collapse. The only sharp spike appears in May 2023 itself, which is the collapse being recorded rather than predicted. Go First's exit was driven by externally reported factors including grounded aircraft and a supplier dispute, which is consistent with a sudden event rather than a gradual erosion that would show up as rising volatility beforehand. The two airlines are presented separately rather than combined into one "instability precedes collapse" claim, because the data only supports that claim for one of them.

## Route concentration (Pareto analysis)

To measure how concentrated India's domestic air traffic is across routes, all routes with fewer than 100 total passengers across the entire decade were excluded first. There are 233 such routes in the raw data, several with literally zero recorded traffic, which appear to be routes registered under regional connectivity schemes that never gained meaningful usage. Including them would inflate the total route count without representing real demand, which would understate how concentrated the genuine traffic actually is.

After this exclusion, 1,677 routes remained, accounting for just over 1.35 billion total passenger movements across the decade. Routes were ranked by total traffic and cumulative share was calculated at several thresholds. The result: the top 100 routes, just 6 percent of all routes with meaningful traffic, account for 73.3 percent of all passenger movement. The top 10 routes alone, well under 1 percent of the network, carry 22.5 percent of total traffic.

## Known limitations

The carrier file and the route file cannot be joined at the airline-route level. The carrier file records which airline flew how many passengers in a given month; the route file records how many passengers traveled between two cities in a given month, but does not record which airline operated those flights. This means it is not possible, from this data, to say which specific airline serves which specific route, or to attribute a route's growth or decline to a particular carrier's decisions. The two layers of this analysis, airline performance and route network structure, are presented as parallel, complementary views rather than one merged dataset, because the data does not support merging them honestly.

All figures in this project come directly from the calculations described above, run against the cleaned data. Where an initial calculation produced a result that did not hold up under inspection, such as the Mumbai-Port Blair CAGR figure, the underlying issue is documented here rather than quietly corrected without explanation.
