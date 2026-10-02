# Google Trends: manual export instructions (for Maneet)

**Why manual:** `trends.google.com` is blocked by this container's egress proxy. Verified 2026-10-02 with one
pytrends attempt (`TrendReq(...).build_payload(["photoshop","canva"], geo="US")`), which failed in 0.8 s with
`ProxyError: Tunnel connection failed: 403 Forbidden`. No further automated attempts were made. Everything below
has to be done in a normal browser, then dropped into this `data/` folder; `load_trends.py` does the rest.

## What we need

| Parameter | Value |
|---|---|
| Date range | **Custom: 2021-01-01 to today** (gives monthly granularity automatically for ranges > ~3 years) |
| Geographies | **United States** and **Worldwide** (two separate exports per set) |
| Search type | Web Search (default) |
| Category | All categories (default) |
| Terms (8) | `cancel adobe`, `photoshop alternative`, `adobe firefly`, `adobe express`, `canva`, `midjourney`, `figma`, `photoshop` |

Enter each term as a plain **search term** (do NOT pick the "Topic" / "Software" entity suggestion that pops up; the
plain search-term row is the one labelled "Search term"). This keeps the eight terms on the same basis.

## Why comparison sets matter

Google Trends normalises every export so that the **largest monthly value across all terms in that comparison
set equals 100**. Values are therefore only comparable *within* one export. Trends allows at most 5 terms per
comparison. We chain two sets through a shared anchor term (`photoshop`) that appears in both; the loader
rescales Set B so that its `photoshop` series matches Set A's `photoshop` series, putting all 8 terms on one scale.

## Exact exports to make (4 CSV files)

| Set | Terms (enter in this order) | Geo | Save as |
|---|---|---|---|
| A | `photoshop`, `canva`, `figma`, `midjourney`, `adobe firefly` | United States | `data/trends_A_US.csv` |
| A | same | Worldwide | `data/trends_A_WW.csv` |
| B | `photoshop`, `cancel adobe`, `photoshop alternative`, `adobe express`, `adobe firefly` | United States | `data/trends_B_US.csv` |
| B | same | Worldwide | `data/trends_B_WW.csv` |

`photoshop` is the anchor (it is the highest-volume term, so it will carry the 100 in both sets and gives the
most precise rescaling). `adobe firefly` is intentionally in both sets as a cross-check: after chaining, the two
`adobe firefly` series should overlay closely; the loader prints the mean absolute gap so you can see whether
the chain is clean. Small low-volume terms (`cancel adobe`, `photoshop alternative`) may show `<1`; the loader
treats `<1` as 0.5.

## Step by step (per export, ~2 minutes each)

1. Open https://trends.google.com/trends/explore in a browser (log in to a Google account if prompted; exports
   sometimes fail when logged out).
2. In the search box type the first term (`photoshop`) and press Enter. Choose the row labelled **Search term**.
3. Click **+ Compare** and add the remaining four terms of the set, in the order listed above, each as
   **Search term**.
4. Set the geography dropdown (top-left) to **United States** or **Worldwide**.
5. Set the time dropdown to **Custom time range** -> From `2021-01-01` To today's date -> OK.
   Confirm the "Interest over time" chart shows monthly points (hover: dates like "Jan 2021").
6. Leave "Web Search" and "All categories" as is.
7. Click the **download icon (arrow)** at the top-right of the "Interest over time" card. This saves
   `multiTimeline.csv`.
8. Rename it to the filename in the table above and move it into
   `research/ws5_trends_competitors/data/`.
9. Repeat for the other three combinations (Set A WW, Set B US, Set B WW). Tip: once Set A is built, just
   change the geo dropdown and download again; then replace terms for Set B.

Expected file format (do not edit it; the loader handles it):

```
Category: All categories

Month,photoshop: (United States),canva: (United States),figma: (United States),midjourney: (United States),adobe firefly: (United States)
2021-01,78,32,5,0,0
2021-02,80,34,6,0,0
...
```

Worldwide exports label columns `: (Worldwide)` instead.

## Then run

```bash
. /home/user/adbe-stock-pitch/.venv/bin/activate
cd /home/user/adbe-stock-pitch/research/ws5_trends_competitors
python data/load_trends.py                # processes US and WW if the CSVs exist
python data/load_trends.py --geo US       # just one geo
```

Outputs: `charts/trends_US.png`, `charts/trends_WW.png` (two panels: competitor/brand terms, and
"cancellation / alternative" intent terms, all on the chained Set-A scale) and
`data/trends_chained_<GEO>.csv` (the merged, rescaled monthly table for anyone who wants the numbers).

## Interpretation guardrails (write these next to any chart)

* Trends values are **relative search interest**, not users or revenue. A rising `canva` line says nothing
  about Adobe's revenue on its own; pair it with the competitor-revenue table in `findings.md`.
* `cancel adobe` spikes historically align with pricing / terms-of-service news (e.g. June 2024 ToS backlash);
  treat spikes as event markers, not trend.
* `photoshop` includes many informational queries (tutorials, "photoshop free"), so a flat `photoshop` line is
  not evidence of flat demand for paid Creative Cloud.
* Seasonality: student-driven terms (`canva`, `photoshop`) dip every June-August and December.

## Synthetic example files

`data/synthetic_example_trends_A_US.csv` and `data/synthetic_example_trends_B_US.csv` are **made-up numbers**
used only to prove the loader runs end-to-end. They are not Google data and must not be used in any analysis.
The loader only picks them up when run with `--synthetic-test`, and writes that test chart to the scratch
directory, never to `charts/`.
