# Shared environment notes for all workstreams (read first)

Date: 2026-10-02. Repo: /home/user/adbe-stock-pitch. Python venv: /home/user/adbe-stock-pitch/.venv
(activate with `. /home/user/adbe-stock-pitch/.venv/bin/activate`; pandas, requests, matplotlib, openpyxl,
beautifulsoup4, lxml, pytrends already installed).

## NETWORK: this container's egress proxy blocks almost every host. Verified 2026-10-02:
REACHABLE
- raw.githubusercontent.com (curl/requests OK) -> any public GitHub file by raw URL
- github.com repo pages via the WebFetch tool only (file listings work; code search needs login; curl to github.com returns 403)
- pypi.org (pip works)
- WebSearch tool (standard + extended modes). Returns search-result snippets AND a synthesized summary with figures and URLs.
  This is the PRIMARY channel for any number from the SEC, BLS, Adobe IR, news, competitor filings.
BLOCKED (both curl and WebFetch): sec.gov, efts.sec.gov, bls.gov, api.bls.gov, download.bls.gov, data.bls.gov,
  fred.stlouisfed.org, web.archive.org (Wayback), stooq.com, finance.yahoo.com/query1, onetcenter.org, onetonline.org,
  adobe.com, news.adobe.com, fool.com, seekingalpha.com, stockanalysis.com, benzinga.com, investing.com, roic.ai,
  investor.figma.com, canva.com, trends.google.com, wikipedia.org, huggingface.co, kaggle.com, zenodo.org, wpp.com,
  macrotrends.net, wagedex.com, datalumos.org, api.github.com, codeload.github.com, gist.githubusercontent.com.
Do NOT burn time re-testing blocked hosts. One quick probe of a NEW host is fine (curl -m 10 -o /dev/null -w "%{http_code}").

## How to source numbers in this environment
1. WebSearch (use mode "extended" for specific numeric facts; it is much richer). Phrase queries to surface the primary
   document (e.g. "Adobe Q2 fiscal 2026 press release Creative and Marketing Professionals subscription revenue 8-K").
   Record in sources.csv the URL of the primary document that the search result cites (e.g. the sec.gov 8-K exhibit URL),
   and in `notes` write "retrieved via WebSearch snippet; page not fetchable from this environment".
2. GitHub raw files for datasets (Indeed Hiring Lab, OpenAI GPTs-are-GPTs, AIOE-Data/AIOE, any public mirror you find).
   Use requests with headers={"User-Agent": "adbe-pitch-research/1.0 (mmaneet2007@gmail.com)"} and time.sleep(1) between calls.
3. If a number cannot be found this way, write `UNAVAILABLE: <reason>` in findings/methods and leave the cell blank. NEVER invent.
   Your own recollection of a figure is NOT a source. You may use recollection to decide what to search for, nothing more.
4. Numbers given in the orchestrator's "starting facts" may be used, cited as source="orchestrator starting facts (10-Q Q3 FY26)",
   but verify via WebSearch where cheap, and flag any discrepancy.

## Required deliverables per workstream folder
data/ (raw + clean CSV), charts/ (PNG), methods.md, findings.md (<=300 words, 3-5 findings with numbers, confidence
high/med/low, SUPPORTS / WEAKENS / NEUTRAL to the long thesis), sources.csv with columns exactly:
claim,value,url,date_accessed,notes

## Chart style (matplotlib)
White background, no top/right spines, one accent color family (navy #1F3A5F, teal #2A9D8F, amber #E9A23B, red #C0392B,
grey #7F8C8D), 150 dpi, figsize ~ (9,5), title in sentence case, axis labels with units, and a source line in small grey
text at the bottom: fig.text(0.01, 0.01, "Source: ...", fontsize=8, color="#7F8C8D"). Save to charts/<descriptive_name>.png.

## Time box
~75 minutes. Write a first draft of findings.md by minute 30 and update it; partial results with clear notes beat nothing.
Do NOT run git commands; the orchestrator commits. Do not write outside your workstream folder.
