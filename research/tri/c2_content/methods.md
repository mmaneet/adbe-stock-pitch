# C2 (content demand x Adobe content stack) - methods

Date: 2026-10-02. Subagent B. Time box ~90 min. Raw downloads in scratchpad only (`.../scratchpad/subB/`); repo holds derived CSVs, charts, <25-word quotes.

## Host probe results (curl -m 12, HTTP code)
| host / URL | code | used? |
|---|---|---|
| adobe.com IR transcript PDFs (adbe-q1fy25 ... adbe-q3fy26-transcript.pdf) | 200 x7 | Y (pypdf) |
| sec.gov EDGAR browse + data.sec.gov submissions JSON + Archives (10-Q/10-K/8-K EX-99.1) | 200 | Y |
| efts.sec.gov full-text search | 200 | not needed |
| bls.gov /oes/2025/may/oes271024.htm and /oes/2024/may/... | 301 -> /oes/home.htm (page moved) | replaced by /oes/special-requests/oesm25nat.zip and oesm24nat.zip (200); /oes/2023/may/oes271024.htm still 200 |
| fool.com transcripts (Meta, Alphabet, Omnicom) | 200 | Y (curl + BeautifulSoup; some slugs not found) |
| s21.q4cdn.com (Meta IR transcript PDFs), s206.q4cdn.com (Alphabet IR transcript PDF), s201.q4cdn.com (Omnicom IR PDFs) | 200 | Y |
| investor.atmeta.com | 403 (bot protection) | replaced by q4cdn PDFs |
| abc.xyz/investor | 200 (events page only) | fool.com / q4cdn used instead |
| wpp.com (307 -> /en) and cdn.wpp.com (AR 2025, H1 2026 transcript/presentation, strategy update PDFs) | 200 | Y |
| publicisgroupe.com /en/investors (404 via WebFetch); press-release PDFs and documents.publicisgroupe.com | 200 | Y (PDF text); HTML release pages via search snippets (verified=N) |
| omnicomgroup.com -> omc.com (301); investor.omc.com | 200 | Y |
| business.google.com (Think article on Hogarth AI production) | 200 via WebFetch | Y |
| facebook.com/ads/library | NOT probed (ToS: manual only) | protocol written |

## Steps
1. Adobe: downloaded 7 transcripts (Q1 FY25-Q3 FY26), split into sentences, filtered on content-stack keywords + numerals; cross-checked against 8-K EX-99.1 releases (Q1 FY24-Q3 FY26) and 10-Q/10-K segment notes. Output: data/adobe_content_stack_metrics.csv (70 rows). DX subscription revenue by quarter FY24Q1-FY25Q4 from releases/10-Qs; FY26 10-Qs state Adobe "combined our former segments ... into a single operating and reportable segment" so DX is not reported; recorded Creative & Marketing Professionals (CMP) customer-group subscription revenue as the closest proxy (it also contains Creative Cloud, so it is a weak proxy).
2. Ad platforms: fetched Meta (Q1 2024-Q2 2026, 10 calls; Q1/Q2 2024 and Q1/Q2 2025 from Meta IR PDFs, rest from fool.com), Alphabet (Q1 2024-Q2 2026, 9 calls; Q3 2024 and Q1 2025 not located), Omnicom (Q3 2025, Q1-Q2 2026). Regex pass for "advertisers/creative/generat/asset" sentences with numerals, then manual selection. Output: data/ad_platform_genai_disclosures.csv (29 rows), charts/ad_platform_genai_adoption.png.
3. Meta Ad Library: manual protocol + template + loader (tested on a synthetic file named *_SYNTHETIC_EXAMPLE.csv; chart file name carries SYNTHETIC_TEST). No real counts were collected.
4. Agencies: WPP AR 2025, H1 2026 transcript, WPP Production launch release, Hogarth/WPP piece on business.google.com; Publicis FY2025 results PDFs, H1 2026 release (globenewswire), Oct 2025 production CEO release; Omnicom Q2 2026 transcript/release/presentation. Output: data/agency_content_statements.csv (17 rows). Headcount reused from ws2 agency_headcount.csv.
5. Labor: reused ws2 rev_per_worker_index.csv (index 240.7 FY25, CAGR 15.8%); re-downloaded BLS OEWS national files (May 2024, May 2025) and recomputed graphic designers and creative5 totals; all matched ws2 to the unit. Output: data/labor_decoupling_check.csv.
6. EPS: data/eps_content_stack.csv and charts/content_stack_eps_scenarios.png. Conversion: $100m ARR x 45% incremental operating margin x (1-18% non-GAAP tax) / 390m diluted shares = $0.0946. Base = FY25 DX subscription revenue $5,409m (10-K) and, alternatively, Q4 FY25 run-rate $1.41bn x 4 = $5.64bn. Scenarios 8/12/16% one-year growth.

## Assumptions and limitations
- "More than X" and "over X%" are lower bounds (flag column). Adobe's product-level growth statements are floors, so a drop from ">30%" to ">20%" is not proof of deceleration, but the disclosed floor fell three quarters in a row (GenStudio: >30% Q1 FY26, >25% Q2, >20% Q3; AEP & Apps: >30%, >30%, >20%).
- DX subscription revenue is the falsifier series and is discontinued from FY26; CMP subscription growth (+12/+13/+13%) includes Creative Cloud and ~$40m/qtr Semrush from Q2 FY26, so it cannot prove DX >8% on its own.
- Ad-platform adoption counts are advertiser counts, not creative volumes; Meta's Q2 2026 figure is "small businesses", Google's are "asset generation tools" vs "AI Max" (different denominators). Only Google Q4 2025 (~70m assets/quarter) and Meta Q3 2024 (15m ads/month) are volume figures.
- WPP's "2.5x assets, flat headcount" is WPP internal data published in a Google marketing piece, not an audited disclosure; Publicis gives growth rates for its creative practice (low-single-digit in 2026), not asset counts.
- No Meta Ad Library observations yet; the protocol is a 20-brand non-random convenience sample.
- The "asset generations 4x" starting fact was not found in any Adobe transcript or release in scope; treated as UNAVAILABLE.
