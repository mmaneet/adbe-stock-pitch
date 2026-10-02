# Shared environment notes for TRIANGULATION subagents (read first; supersedes research/_ENV_NOTES.md)

Date: 2026-10-02. Repo: /home/user/adbe-stock-pitch. Python venv: /home/user/adbe-stock-pitch/.venv
(`. /home/user/adbe-stock-pitch/.venv/bin/activate`; pandas, requests, matplotlib, openpyxl, beautifulsoup4, lxml, pytrends, pypdf installed).
Author's prior pitch (style/rigor standard): inputs/Maneet_Mehta_YSIG2026Pitch.pdf and extracted text inputs/Maneet_Mehta_YSIG2026Pitch.txt.
Read the .txt first (10 min max): dense prose, numbered footnotes, "Sources" appendix with terse citations, channel-check tallies like "17/20",
"small non-random sample" caveat, and every claim converted to EPS with the math shown in a footnote.

## NETWORK (re-probed 2026-10-02 after the user widened access)
NOW REACHABLE (HTTP 200 via curl): www.sec.gov (EDGAR full-text search efts.sec.gov likely too; use a descriptive User-Agent with
contact email, max 10 req/s per SEC fair-access policy), www.bls.gov, www.adobe.com (incl. helpx and IR PDFs under
adobe.com/cc-shared/assets/investor-relations/pdfs/), www.fool.com, www.onetonline.org, raw.githubusercontent.com, pypi.org,
trends.google.com (301 on probe; pytrends may now work, test it).
RETURNED 403 FROM THE SITE (bot protection, not the proxy): investor.figma.com, www.canva.com. Try the WebFetch tool on these
and on news.adobe.com, meta investor site, abc.xyz, wpp.com, publicisgroupe.com, omnicomgroup.com, docusign, fiverr, upwork, shutterstock,
getty — ONE probe each, then fall back to WebSearch.
STILL BLOCKED: web.archive.org (Wayback), stooq.com. Assume blocked unless your own single probe says otherwise.
FIRST ACTION: probe the hosts you need (curl -m 10 -o /dev/null -w "%{http_code}" URL) and record results at the top of methods.md.

## Sourcing rules (non-negotiable)
1. Primary pages first (SEC filings, Adobe IR transcripts/datasheets at adobe.com, BLS, company newsrooms).
2. If a host is blocked: WebSearch (mode "extended" for numbers), record the snippet's primary URL, mark verified=N and label VERIFY.
   Then check /home/user/adbe-stock-pitch/inputs/ for user-provided files, and append a row to
   /home/user/adbe-stock-pitch/research/tri/NEEDS_MANUAL.md (file name, URL, why) — append with `>>`, never overwrite; other agents append too.
3. NEVER fabricate. Unavailable -> "UNAVAILABLE: <reason>". Your recollection is not a source.
4. No ToS-violating scraping: no LinkedIn, no automated Meta Ad Library, Similarweb, Google Play, or paywalled sites. For those write a
   MANUAL COLLECTION PROTOCOL + CSV template + loader script.
5. Do NOT save raw third-party transcript or article text into the repo. Save derived data and short quotes (<25 words, with citation).
   Raw downloads go to the scratchpad: /tmp/claude-0/-home-user-adbe-stock-pitch/434e9d74-e598-592e-aa01-e9e6b55767df/scratchpad/<your_name>/
6. Label company claims vs independent evidence; "more than X" disclosures are LOWER BOUNDS.
7. Reuse prior work; do not redo it: research/SUMMARY.md, research/ws1_price_volume (price log, revenue_quarterly.csv, decomposition.csv),
   ws2_seat_compression (BLS OEWS 2019-2025 all 7 SOC codes, Indeed, agency headcount, scenarios), ws3_task_exposure,
   ws4_call_nlp (13 full transcripts parsed: data/analyst_questions.csv, forward_pe.csv, vocab_counts.csv, usage_term_first_mentions.csv;
   transcripts in ws4_call_nlp/data/transcripts/*.txt for FY23Q1-FY26Q2 except FY25Q2 — you MAY read these for exact quotes),
   ws5_trends_competitors (Figma/Canva metrics, growth_comparison.csv), ws6_channel_checks.

## Deliverables per folder research/tri/<name>/
data/ (raw + clean CSV), charts/ (PNG, white bg, no top/right spines, palette navy #1F3A5F teal #2A9D8F amber #E9A23B red #C0392B
grey #7F8C8D, 150 dpi, source line in small grey text at bottom via fig.text), methods.md (host probe results, steps, assumptions,
limitations), findings.md (<=300 words: key numbers, confidence, SUPPORTS/WEAKENS/NEUTRAL per contention, FALSIFIER status),
sources.csv with EXACT columns: claim,value,source_type,url,date_accessed,verified,notes  (source_type in company|peer|industry|alt|primary; verified Y/N).

## EPS conversion (recompute and show; do not just assert)
Each $100M of ARR ~ $0.09-0.10 EPS: $100M x ~45% incremental operating margin x (1 - 18% non-GAAP tax) / ~390M diluted shares.
State your inputs; the integrator will put a live-formula version in the workbook.

## Time box
~90 minutes. Write findings.md draft by minute 40 and update it. Partial results with clear notes beat nothing. Do NOT run git.
