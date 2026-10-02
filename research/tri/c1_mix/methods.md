# C1 (revenue mix) — methods

Subagent A, 2026-10-02. Contention C1: "Most revenue sits where AI makes Adobe harder to replace (documents, teams/enterprise)."
Falsifier: individual Creative Cloud > 50% of total ARR, or teams/enterprise Creative Cloud growth below individual growth.

## Host probes (curl -m 12, UA "adbe-pitch-research/1.0 (mmaneet2007@gmail.com)")
| host / URL | result | used for |
|---|---|---|
| www.sec.gov EDGAR browse + Archives | 200 (Archives need -L: 301 on /data/0000796343/...) | Adobe 8-K Ex.99.1 FY24Q1-FY26Q3, 10-Q Q3 FY26, 10-K FY25; DocuSign 8-K/10-Q; Figma 10-Q |
| efts.sec.gov full-text search | 500 | not used (browse-edgar index used instead) |
| adobe.com IR transcript PDFs (q2fy26, q3fy26) | 200 | pypdf text, saved in scratchpad only |
| adobe.com IR financial-documents page, investor datasheet PDFs (Sept 10 2026; Jun 11 2026), Summit 2026 Q&A, Investor Meeting Mar 12 2025 deck (109 pp, image-only) | 200 | ARR/RPO/cRPO/DX series; route-to-market and CC enterprise ARR slides (rendered with pdftoppm, read visually, donuts pixel-measured) |
| www.onetonline.org summary/details/demand pages, hot_tech list, Software_Skills CSV export | 200 (1.5 s between requests) | O*NET technology skills, In Demand posting shares, national Hot Technology posting counts |
| ramp.com/data, /data/ai-index (10 MB RSC payload with embedded JSON), /vendors/{canva,figma,openai}, /vendors/categories/* | 200; /vendors/adobe and 5 Adobe slug variants 404; /vendors/docusign 404 | Ramp AI Index series; Ramp Rate vendor pages |
| query1.finance.yahoo.com chart API | 200 | ADBE close 2026-10-01 = $241.28 (verified) |
| www.fool.com DocuSign Q2 FY27 transcript | 200 | DNR 103% quote |
| investor.docusign.com, investor.figma.com, www.canva.com, www.inc.com | 403/404 | fell back to EDGAR / WebSearch; logged in NEEDS_MANUAL |

## Steps
1. Verified starting facts: price $241.28 (Yahoo daily close 2026-10-01; 10-02 intraday 237.68), shares 389.2M (10-Q cover, as of 2026-09-18), Q3 FY26 C&MP $4,651M vs $4,117M, BP&C $1,905M vs $1,648M, 9M $13,577M/$12,058M and $5,540M/$4,777M (10-Q), ARR $27.50B (+11.2%), FY25 DX subscription $5.41B (8-K Q4 FY25), Semrush closed 2026-04-28 for $1.87B (10-Q Note 3), ~$480M ARR / ~$40M Q2 revenue (8-K Q2 FY26). All matched the prior revenue_quarterly.csv; FY24 C&MP/BP&C there were DERIVED, now replaced by Adobe's recast datasheet values (data/customer_group_revenue_quarterly.csv).
2. RPO/cRPO FY24Q1-FY26Q3 from 8-K press releases, 10-K FY25 and 10-Q Q3 FY26, cross-checked to the IR datasheet (data/rpo_series.csv).
3. Quotes (<25 words) extracted from the Q2/Q3 FY26 FactSet corrected transcripts with speaker and date (data/management_quotes.csv). Raw PDFs/text kept in scratchpad only.
4. Exposure tiers (data/exposure_tiers.csv): Total ARR allocated pro rata to Q3 FY26 subscription revenue (BP&C / DX / C&MP-ex-DX). Creative Cloud enterprise ARR taken from the Investor Meeting deck ($2.2B FY24, 15% CAGR) and grown 1.75 years. Route-to-market donuts (no printed %) were measured by sampling ring pixels at 720 angles: BP&C enterprise ~19%, C&MP enterprise ~46-50% (= Digital Experience $1.30B + ~$0.5B/qtr Creative Cloud enterprise in Q1 FY25, consistent with the $2.2B ARR disclosure). Individual vs teams is NOT disclosed: 40/50/60% sensitivity.
5. EPS at risk (data/eps_at_risk.csv): $100M ARR x margin x (1-18%) / 389.2M shares = $0.0948 (45%) / $0.0737 (35%); applied to 5/10/20% declines in the individual tier under each sensitivity; FY26 reference EPS = 9M $18.15 + Q4 guide midpoint $6.325 = $24.48.
6. Peers: DocuSign (8-K Q2 FY27, 10-Q, fool.com transcript), Figma (10-Q Q2 2026 on EDGAR), Canva (secondary; prior ws5 file) -> data/peer_metrics.csv.
7. Industry: O*NET In Demand pages expose "Percentage" = unique Lightcast postings mentioning the skill / all unique postings for the occupation, Jan 1-Dec 31 2025; Hot Technology list exposes national unique postings out of 46,885,153. Site updated Aug 25 2026; occupation pages "Updated 2026" (no numbered DB release printed on the page) -> data/onet_tech_skills.csv, data/onet_hot_tech_national.csv.
8. Alt: Ramp AI Index arrays (adoptionOverall, adoptionVendor, adoptionSize) parsed from the page payload; Ramp Rate vendor/category pages -> data/ramp_ai_index.csv.

## Assumptions and limitations
- ARR-by-tier is a reconstruction; Adobe discloses only two customer groups and total ARR. Pro-rata allocation assumes ARR/revenue ratio is uniform across groups (true ratio 1.049 overall).
- Creative Cloud enterprise ARR after FY24 is extrapolated (ESTIMATE). Express and consumer Firefly ARR are estimates ($0.3B/$0.2B).
- Donut pixel measurement: the calibration donut (customer groups, true C&MP share 72.3%) read 60-62% with a clipped render, so treat route shares as +/-5-10 pts; the BP&C and C&MP route donuts were sampled over the full ring (720/720 points) and are more reliable than the FY24 total donut.
- Teams vs individual growth is not disclosed; the falsifier's second leg is judged on (a) FY21-24 CC enterprise ARR CAGR 15% vs CC subscriptions ex-enterprise ~10% (deck p.85), and (b) FY26 management language (teams/enterprise "continued strength" vs individual ARR expectations lowered). Both are company sources.
- Peer evidence is adjacent, not identical: Figma competes in UI design, Canva in communicator/SMB design, DocuSign in agreements.
- O*NET posting shares are 2025 calendar-year postings; they measure stated skill requirements, not seat purchases.
- Ramp publishes no Adobe vendor data; Ramp Rate adoption rates are shares of buyers within a software category on Ramp's platform, not of all businesses.
