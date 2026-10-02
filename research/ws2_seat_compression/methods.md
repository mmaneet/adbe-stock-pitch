# WS2 — Seat compression: methods

Date: 2026-10-02. Bear argument tested: **B2 "AI makes designers more productive, so companies cut design headcount and Creative Cloud seats regardless of product quality."** Tested neutrally; evidence against the long is reported first in findings.md.

## 1. BLS OEWS employment (heart of the workstream) — `data/bls_oews_employment.csv`, `data/bls_oews_employment_wide.csv`
- Target: national May estimates, SOC 27-1024, 27-1011, 27-1014, 27-4032, 27-4021 (the "creative5") and 11-2021, 13-1161 (the "marketing2"), May 2019–May 2025 (May 2025 is the latest release).
- bls.gov is blocked here. Route used: **GitHub mirrors of the BLS national files**, located with GitHub code search for exact `OCC_CODE + TOT_EMP` string pairs, then downloaded from raw.githubusercontent.com:
  - 2019: `axtex/255-AI` `bls_cleaned.csv` (TOT_EMP_2019, derived from oesm19nat); graphic designers 215,930 also in `tejas-kale/blog` series; marketing managers 263,680 and art directors 42,890 also in `lisaphaaaam/Data-Vis-Project-1 all_data_M_2019.csv`.
  - 2020: `ericsson-c/DMT-homework2 occupations-truncated.csv` (full May 2020 national table). 7 of 7 values cross-checked against bls.gov page snippets returned by WebSearch (27-1024 201,440; 27-1011 40,950; 27-1014 26,460; 27-4032 22,410; 27-4021 41,600; 11-2021 270,200; 13-1161 690,160).
  - 2021: `openai/GPTs-are-GPTs data/national_May2021_dl.csv` (verbatim BLS file).
  - 2022: `arieldklein/ai-employment-paper bls_2022_clean.csv` (from oesm22nat.zip), identical to `augw999` and `axtex` mirrors.
  - 2023: `augw999/ai-labor-market-impact_analysis cleaned_data_2023.csv`; 6 of 7 values cross-checked vs bls.gov snippets.
  - 2024: `Budget-Lab-Yale/AI-Employment-Model resources/national_M2024_dl.csv` (verbatim), identical to `theodorewright11` and `augw999` mirrors.
  - 2025: `theodorewright11/ai-workforce-exposure-dataset-construction-public data/oews_national_2025.csv` (verbatim), identical to `arieldklein bls_2025_clean.csv`; 3 values cross-checked vs bls.gov snippets.
- Every code-year is **ACTUAL** (no interpolation was needed). `source_url` in the CSV is the canonical bls.gov page for that code-year; the `mirror` column names the file actually read. Mean wage = OEWS A_MEAN where the mirror carried it (2019/2023 wages from the `KNguyen37/h1b-econ-paper` 2017–2024 panel).
- Caveats: OEWS counts **wage-and-salary** jobs only (no freelancers, who are a large share of creative work); estimates pool three years of semi-annual samples, so year-to-year changes are noisy for small occupations (27-1014 swings 20–36k). Employment is **US only**; Adobe revenue is global.

## 2. BLS projections — `data/bls_projections_2024_34.csv`
2024–34 percent changes and (where found) 2024/2034 levels from BLS Employment Projections / OOH via WebSearch snippets. BLS released 2025–35 projections in Sep 2026 (OOH updated); those are recorded in separate columns. EP levels include self-employed, so they exceed OEWS levels.

## 3. Indeed Hiring Lab — `data/indeed_postings_monthly.csv`
Downloaded `job_postings_by_sector_US.csv` and `aggregate_job_postings_US.csv` from the hiring-lab GitHub repo (raw, with contact User-Agent). Kept total postings (SA and NSA) and sectors Media & Communications, Arts & Entertainment, Marketing, Software Development; monthly mean of the daily index (Feb 1 2020 = 100). "Creative avg" = simple mean of the three creative sectors.

## 4. Agency headcount — `data/agency_headcount.csv`
Year-end employees from 10-K / 20-F / URD / preliminary results via WebSearch snippets. Omnicom closed the Interpublic acquisition on 26 Nov 2025; Omnicom's FY2025 10-K figure (~120,000) is the combined company, so the chart shows Omnicom + IPG combined (pro forma) for all years. Publicis 2025 is "around 114,000" (press), flagged approximate.

## 5. Adobe anchors — `data/adobe_revenue.csv`
Total, Digital Media, Creative and Document Cloud revenue FY2019–FY2024 from 10-K / 8-K Ex.99.1 via WebSearch snippets; FY2025 total ($23.77B) and Digital Media ($17.65B) found; **FY2025 Creative vs Document Cloud split UNAVAILABLE** in snippets (Adobe moved to customer-group disclosure; Q4 FY25 Creative & Marketing Professionals subscription revenue $4.25B, +11%). FY26 facts from orchestrator starting facts (10-Q Q3 FY26); Q3 FY26 ending ARR $27.50B and C&MP subscription revenue $4.65B (+12%) confirmed via WebSearch of the Q3 FY26 8-K.

## 6. Indices and scenarios — `data/rev_per_worker_index.csv`, `data/scenarios.csv`
- Index each series to 2019 = 100 (Adobe fiscal year ending ~Nov 30 vs OEWS May reference; ~6-month offset ignored). Revenue-per-worker index = revenue index / creative5 employment index. Presented as indices only because the numerator is global and the denominator is US wage-and-salary employment.
- Required per-worker growth to sustain ~10% ARR growth: `1.10/(1+h) − 1` for h = 0, −3%, −7%.
- Employment projections to 2027–28 (May reference, i.e. roughly FY27–FY28): (a) BLS 2024–34 and 2025–35 percent changes weighted by May-2025 OEWS employment, converted to a CAGR; (b) postings-based: latest 3-month YoY change in the Indeed creative-avg index (+4.9%) × an assumed employment-to-postings elasticity β = 0.15 (postings are a flow; the empirical 2022→2025 ratio of employment change to postings-level change was 0.16); (c) 2019–25 trend CAGR; (d) stress = repeat of the May-2024→May-2025 −4.9% drop.

## 7. Charts
matplotlib, env-notes palette (navy/teal/amber/red/grey), white background, no top/right spines, 150 dpi, source line. The dataviz validator flags navy/grey as low-chroma and amber as low-contrast on white; mitigated by direct end-labels with text on every series plus legends (identity never color-alone). No dual axes; two-panel figure used where scales differ.
