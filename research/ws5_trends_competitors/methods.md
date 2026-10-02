# WS5 methods: Google Trends, competitor growth, share-shift arithmetic

Date: 2026-10-02. Folder: `research/ws5_trends_competitors/`. All numbers were obtained through the WebSearch tool
(extended mode for figures) because every primary host (sec.gov, investor.figma.com, canva.com, adobe.com,
trends.google.com) is blocked by the container proxy. `sources.csv` records the primary URL each snippet cited.

## 1. Google Trends (not retrieved; manual kit provided)

* One pytrends attempt (`TrendReq(timeout=(10,20), retries=0).build_payload(["photoshop","canva"], geo="US")`)
  failed in 0.8 s with `ProxyError ... 403 Forbidden` (proxy CONNECT refused). No retries.
* `data/google_trends_MANUAL_EXPORT_INSTRUCTIONS.md`: step-by-step browser export, monthly, 2021-01 to today, US and
  Worldwide, 8 terms split into two <=5-term comparison sets that share `photoshop` as anchor (and `adobe firefly`
  as a cross-check). File naming `data/trends_<A|B>_<US|WW>.csv`.
* `data/load_trends.py`: parses the Google CSV format (preamble line, `<1` values, `term: (geo)` headers), rescales
  Set B onto Set A via a least-squares scale factor on the anchor, prints the cross-check gap, writes
  `data/trends_chained_<GEO>.csv` and `charts/trends_<GEO>.png` (two panels: brand terms; switching-intent terms).
* Smoke test: run with `--synthetic-test` on `data/synthetic_example_trends_{A,B}_US.csv` (12 months of made-up
  values, clearly labelled SYNTHETIC in filename and chart footer). Output went to the scratch directory, not `charts/`.
  Result: k = 1.005, cross-check gap 0.00. Nothing synthetic is used anywhere in findings.

## 2. Competitor metrics (`data/competitor_metrics.csv`)

* Figma: every quarter from Q1 2024 to Q2 2026. Q2-Q4 2024 revenue is DERIVED by dividing the 2025 quarter by
  (1 + reported growth) because the S-1 snippet did not list them; flagged in `notes`. NDR, >$10k and >$100k customer
  counts as disclosed; Q2 2025 NDR (129%) is derived from "131% up 2 pts QoQ".
* Canva (private): company-stated milestones (newsroom, Inc./Fortune interviews) and Sacra estimates are kept as
  separate rows with the basis in `notes`. Sacra's end-2024 ARR ($2.8B) conflicts with company statements of
  $2.3-2.55B in H2-2024; the CY2024 growth row is therefore flagged uncertain. Q2-2026 revenue ($921.9M, +25.2%) and the
  2026 growth-guide cut (30% to ~20%) come from Aug-2026 press reports of an investor update (first reported by The
  Information); no primary document is public.
* Midjourney: Sacra/GetLatka estimates only; labelled ESTIMATE.
* Adobe: FY23-FY25 Digital Media, Creative, Document Cloud and total revenue from 8-K press releases; Q4 FY25 and Q3
  FY26 customer-group revenue; Q3 FY26 anchors from the orchestrator (10-Q), cross-checked against WebSearch
  (C&MP $4.65B +12%, BP&C $1.91B +15%, ARR $27.50B +11.2%: consistent). FY24 Creative revenue is DERIVED as DM minus DC.

## 3. Growth comparison and incremental dollars (`data/growth_comparison.csv`, `data/build_growth_charts.py`)

* YoY growth = value / prior - 1 where both are available; otherwise the reported rate is used.
* "Annualized incremental" = latest-quarter YoY dollar increase x 4. For annual rows it is the FY/CY increase.
* Share-of-pool arithmetic (printed by the script): pool = Adobe C&MP + Figma + Canva, all on quarterly revenue x 4.
  Adobe share of stock vs share of increment indicates direction of share movement. A second cut uses FY25 Adobe
  Digital Media, Figma FY25 revenue and Canva CY25 ARR (estimate) for an annual view.
* Charts follow `_ENV_NOTES.md` style (white, no top/right spines, navy/teal/amber/red/grey, 150 dpi, source line).
  Hatched bars are third-party estimates.

## 4. TAM

Company-cited figures from Adobe's Investor Meeting at Summit (2024-03-26): TAM $205B (2024) to $293B (2027), 13% CAGR;
Creative Cloud $91B by 2027. Only secondary coverage (Futurum, Substack, BusinessWire notice) was reachable; labelled
ESTIMATE and used only as a sanity check.

## Caveats

* Figma (UX/product design, dev handoff, Make) overlaps only partly with Creative Cloud; Canva's ~$128 ARR per paid
  user is a different price tier from Adobe pro seats. The "pool" is a proxy, not a market-share measure.
* Canva ARR and revenue are mixed in press coverage; where possible the basis is stated in each row.
* Adobe BP&C contains Acrobat and Express, so it is not a pure creative comparator to Canva.

## UNAVAILABLE

* Google Trends series (host blocked).
* Adobe FY25 full-year Creative and Document Cloud revenue (disclosure discontinued / not surfaced).
* Adobe FY25 full-year C&MP and BP&C subscription totals (not surfaced; Q4 FY25 quarter used instead).
* Figma >$100k customer count at 2025-06-30 (only "more than 1,100" disclosed in snippet).
