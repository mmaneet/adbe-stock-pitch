# C4 "Users are coming to Adobe, not leaving" - methods (Subagent D, 2026-10-02)

## Host probes (curl -m 12, 2026-10-02 ~17:28 UTC)
| host / URL | result |
|---|---|
| adobe.com/cc-shared/assets/investor-relations/pdfs/adbe-q{1-4}fy25, q{1-3}fy26-transcript.pdf | 200 (all 7 downloaded, 19-21 pp each) |
| sec.gov EDGAR company browse + Archives folders for CIK 796343 | 200 |
| news.adobe.com/ | 200 (JS shell; individual release pages fetch at 200 but carry no metrics) |
| news.adobe.com/en/news-releases, /en/news | 404 |
| trends.google.com/trends/explore (bare curl) | 429 - but pytrends WORKED (see below) |
| web.archive.org | not probed; blocked per _ENV_NOTES_v2 |
| similarweb.com, play.google.com | not fetched (ToS: manual protocols instead) |

Scratchpad (raw PDFs/HTML, not in repo): /tmp/claude-0/.../scratchpad/c4_users/. Nothing raw is saved under research/.

## Task 1 - company data (data/mau_quarterly.csv, 73 rows)
- Source: the 7 earnings-call transcripts (FY25Q1-FY26Q3, call dates 2025-03-12, 06-12, 09-11, 12-10, 2026-03-12, 06-11, 09-10) and the
  matching 8-K Exhibit 99.1 press releases on sec.gov (accessions 25-000052, -000064, -000102, -000135, 26-000048, -000109, -000147).
- Extraction: pypdf text -> regex sweep for monthly active / MAU / freemium / AI-first / generations / downloads / first-time; every hit
  read in context; quotes kept < 25 words. `lower_bound_flag = Y` wherever the company said "more than/over/surpassed/crossed".
- Columns: quarter, metric, value, lower_bound_flag, quote<25w, url. Growth rates are separate rows (metric suffix _pct or _x).
- Non-company numbers inside the file are flagged in the metric name (ANALYST_ESTIMATE, IMPLIED, ACQUIRED).
- Starting facts: all VERIFIED. Total MAU >1B (+>20%) Q3 FY26; Acrobat+Express MAU >700M (Q2 FY25) -> >750M (Q4 FY25) -> >850M
  (Q2 FY26) -> >900M (Q3 FY26); creative freemium MAU >50M (Q2 FY25, retrospective) -> >70M -> >80M -> >90M -> >100M;
  AI-first ARR >$125M (Q1 FY25) -> >$250M (Q3 FY25) -> >3x YoY (Q1 FY26) -> >$500M (Q2 FY26) -> >$650M (Q3 FY26).
- MAX 2025 (3 releases fetched), Summit 2026 and the Apr-2026 Firefly creative-agent release: no MAU, download or cumulative-generation
  figures (checked by fetch; only "unlimited generations through Dec 1 2025"). MAX 2026 is Oct 28-30 2026 - not yet held.
  Cumulative generations were last disclosed at 29B (Q3 FY25); FY26 calls switched to credit-consumption growth rates.

## Task 2 - Google Trends (pytrends 4.9.2, worked)
- Two fixes were needed: (a) pytrends passes `method_whitelist` to urllib3 2.x -> monkey-patched Retry to map it to `allowed_methods`
  (retries=2, backoff_factor=10 as specified); (b) pytrends does `self.geo = geo or self.geo`, so a worldwide call (geo='') after a US call
  silently re-uses US - the first run's "WW" files were byte-identical to US and were discarded; run 2 used a fresh TrendReq per geo.
- Requests (timeframe 2019-01-01 to 2026-10-01, web search, all categories, 15-30 s random sleep between calls): R1-R3 as specified
  (anchor "photoshop" in each). Two additional requests were added because on the R1 scale "cancel adobe" and "photoshop alternative"
  round to 0-1 (Google reports integers on a max=100 scale): R4 = churn-only set [cancel adobe, photoshop alternative, adobe alternative,
  cancel adobe subscription, adobe firefly] and R2b = AI-only set [adobe firefly, midjourney, canva ai, chatgpt image, leonardo ai].
  One 429 occurred (R4 worldwide, attempt 1); the 60 s wait-and-retry succeeded. 11 CSVs in data/trends_raw_<R>_<US|WW>.csv.
- Ratios (data/trends_ratios_<geo>.csv, built by data/load_trends_ratios.py):
  churn_intent_ratio_idx = (cancel adobe + photoshop alternative)[R4] / (photoshop + adobe)[R1], indexed to 2019 avg = 1.00. Numerator and
  denominator come from different requests, so the LEVEL is arbitrary; because Google's per-request normalisation is one constant, the
  SHAPE (and "new highs") is valid. A broad variant (all four churn terms) and an R1-only integer cross-check move the same way.
  ai_share_ratio = adobe firefly / (midjourney + canva ai) within R2b (level meaningful). chatgpt_image_vs_photoshop within R2.
- The partial month 2026-10 (one day of data) is excluded; 2026 = Jan-Sep YTD. Annual averages are simple means of monthly values.
- Charts: charts/trends_churn_intent_ratio.png (signature; Lennox Fig. 1 style: annual-average points labelled, faint monthly line,
  US navy / WW teal, y capped at 8.5 with the WW Feb-2026 peak noted), trends_ai_share_ratio.png, trends_chatgpt_image_vs_photoshop.png.
- Caveat: Google re-samples per pull; a hand export before publication is listed in NEEDS_MANUAL.md. The loader accepts raw
  multiTimeline.csv exports under the same file names. Worldwide churn numerators are 1-20 on their own scale, so WW is noisier than US.
- Event check (WebSearch, verified=N): Feb-Mar 2026 spike coincides with the $150M DOJ settlement over cancellation-fee disclosures
  (Mar 2026) and the UK CMA probe (2026-03-19); Jun 2026 spike coincides with 12-25% list-price increases effective 2026-06-01.
  Excluding both spike months, 2026 YTD US still averages 3.50x 2019 vs 1.89 in 2025.

## Task 3/4 - Similarweb and Google Play
Manual protocols only (no scraping): data/similarweb_PROTOCOL.md + similarweb_template.csv + load_similarweb.py;
data/google_play_PROTOCOL.md (exact Wayback URLs per app/year) + google_play_template.csv + load_google_play.py. Both loaders were
smoke-tested on clearly-labelled synthetic files only (data/_synthetic_test_output/*SYNTHETIC*). Rows appended to research/tri/NEEDS_MANUAL.md.

## Task 5 - MAU -> AI-first ARR (data/build_mau_arr.py -> mau_to_arr_ratio.csv, charts/mau_vs_ai_first_arr.png)
- Descriptive ratio, NOT causal: AI-first ARR also contains Acrobat AI Assistant, Firefly Services/Foundry and GenStudio (enterprise),
  none of which is sold to creative-freemium users. Inputs are company lower bounds; implied values are flagged (Q1 FY25 MAU = 80/1.5;
  Q3 FY25 MAU = 100/1.7; Q1 FY26 ARR = 3 x 125). Headline (as briefed): (650-250)/(100-50) = $8.0 per incremental MAU; other periods $9.3-15.0.
- EPS: $100M ARR x 45% incremental operating margin x (1 - 18% non-GAAP tax) / 390M diluted shares = $0.0946 ~ $0.095 per $100M.
  Scenario table: if freemium MAU reaches 150M and $8/MAU holds -> +$400M ARR -> +$0.38 EPS; 200M -> +$800M -> +$0.76 (at $5/MAU: +$0.24 / +$0.47).

## Charts
Palette per _ENV_NOTES_v2 (navy/teal/amber/red/grey), white background, no top/right spines, 150 dpi, grey source line. The dataviz
validator flags this mandated palette (navy below the lightness band, grey below the chroma floor, amber contrast 2.1:1); mitigated by using
at most two series per chart, distinct markers (circle/square), and direct value labels so identity is never colour-alone.

## Limitations
Company MAU definitions changed across calls (Acrobat+Express vs "BP&C" vs "all businesses") and are lower bounds; Google Trends is a
relative index sampled per request; no independent user-count source could be fetched inside ToS (Similarweb/Play are manual);
peer user counts are reused from ws5 (snippet-sourced). Time box ~90 min.
