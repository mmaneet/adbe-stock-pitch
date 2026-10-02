# ADBE long pitch: alternative-data research summary

Prepared 2026-10-02 for the Citadel Fall 2026 Pitch Competition (first round). Thesis under test: the market prices
ADBE (~$241, ~10x FY26 non-GAAP EPS guide of $24.45-24.50) as if free cash flow never grows, on fears that AI destroys
Creative Cloud; we argue AI exposure is concentrated in a minority of revenue (individual/prosumer creative seats),
enterprise/document/marketing-platform revenue is protected or helped, and monetization is shifting from seats to usage.

Environment caveat: this container could reach only GitHub, PyPI and a web-search tool. Every SEC, BLS, Adobe IR and
news figure below was retrieved from search-result snippets citing the primary URL (recorded in each sources.csv);
the primary pages themselves were not fetchable. Wayback Machine, Google Trends and full earnings-call transcripts were
UNAVAILABLE. Treat snippet-sourced figures as "verify before slide" and re-pull from the cited URL where it matters.

---

## WHAT CUTS AGAINST US (every finding that weakens the long)

1. **US creative employment is now shrinking, and BLS blames AI (WS2, confidence high).** The five creative occupations
   fell 4.9% from May 2024 to May 2025 (366,000 to 348,240), the worst non-COVID year in the series; graphic designers
   fell 7.7% (214,260 to 197,830, a 2019-25 low). The BLS Occupational Outlook Handbook, updated September 2026, now
   projects graphic designers at -2% for 2025-35 and cites automated design tools; the prior vintage was +2.1%.
   Bear argument B2 (seat compression) is visible in the labor data.
2. **The most AI-exposed creative-workflow stages are seat-monetized (WS3, confidence medium).** Ideation (100% of task
   weight highly exposed), asset generation (98%) and editing/retouching (88%) are the most exposed stages, and all are
   served by per-seat Creative Cloud/Express plans. 72% of highly exposed creative task weight sits in seat-monetized
   stages versus 1% in usage-monetized stages (human labels; 62% vs 10% on GPT-4 labels). The data does not show usage
   monetization covering the exposed stages today.
3. **Underlying C&MP volume/mix growth is decelerating while headline growth accelerates (WS1, confidence medium-low).**
   Base-case implied volume/mix fell from 9.3% (FY25 Q1) to 6.1% (FY26 Q3) while reported growth rose from 10% to 13%.
   The FY26 "re-acceleration" is price (June 2025 Creative Cloud Pro repricing), Semrush and FX.
4. **Share is drifting away from Adobe (WS5, confidence medium).** Adobe holds ~78% of the Adobe C&MP + Figma + Canva
   revenue pool but only ~64% of the latest annualized increment; share fell ~2.4 points year over year. Figma is
   accelerating (+48% in Q2 2026, net dollar retention 136-139%, FY26 guide raised twice).
5. **The price lever is being reused (WS1, confidence medium).** VIP/teams list increases from June 2026 and Acrobat
   Standard business increases from April 2026 mean FY27 reported growth will again overstate volume as the June 2025
   wave laps in Q3 FY26.
6. **Agency headcount is falling at the largest Adobe enterprise customers (WS2, confidence medium).** Big-4 holding
   company headcount is down 5.2% from the 2023 peak; WPP is down 14.6% from 2022; Omnicom plus IPG cut ~8,200 in 2025.
7. **The analyst "AI fear" signal could not be measured with full transcripts (WS4).** See the WS4 section for what was
   recoverable and how much weight it can bear.

---

## WS1: price vs volume decomposition (tests B1: are price increases masking seat losses?)

- Price explains 25-50% of C&MP growth, not all of it: Q3 FY26 C&MP +13.0% reported, ~-1pt FX, ~-2.9pt Semrush
  (estimated $120M) gives ~9.1% organic constant-currency growth; the June 2025 repricing contributes 1.4 / 2.8 / 4.2pt
  at 10/20/30% of revenue repriced, leaving implied volume/mix of 7.6 / 6.1 / 4.7%.
- Implied volume/mix stays positive mid-single-digit in every quarter FY25 Q1 to FY26 Q3 and every scenario (floor 4.7%);
  zero volume growth would require more than 60% of C&MP revenue to have taken the full list uplift.
- BP&C (Acrobat/Express) growth of 15-16% is almost entirely volume/mix: no verified Acrobat or Express list change took
  effect between July 2024 and March 2026, so price adds ~0pt in FY26.
- Best chart: `ws1_price_volume/charts/price_vs_volume_stacked.png`
- Confidence: medium. Impact: SUPPORTS on B1 (no seat collapse in revenue), but finding 3 above WEAKENS the
  re-acceleration narrative.

## WS2: revenue per creative worker / seat compression (tests B2)

- Adobe Digital Media revenue grew +129% FY19-FY25 while US creative employment fell 5%; revenue per US creative worker
  index reached 241 (CAGR 15.8%). In FY25 alone employment fell 4.9% and Digital Media revenue grew 11.3% (+16.9% per
  worker). Seat count has not been the growth engine.
- Scenario math: per-worker growth needed to sustain ~10% ARR growth is 10.0% (flat headcount), 13.4% (-3%/yr) and
  18.3% (-7%/yr). Historical 14.4-15.8% CAGRs clear the -3% bar; 18.3% was achieved only in COVID-distorted 2020.
- Indeed creative postings (Media & Communications 71, Marketing 76, Arts & Entertainment 84 vs total 103, Feb 2020 =
  100) are depressed but +4.9% year over year after a 2025 trough.
- Best chart: `ws2_seat_compression/charts/revenue_per_creative_worker_index.png` (bear exhibit:
  `ws2_seat_compression/charts/oews_creative_employment_index.png`)
- Confidence: high on data, medium on causality. Impact: MIXED. B2 is real in the 2025 labor data (WEAKENS) but has not
  yet appeared in revenue (SUPPORTS); the long survives -3%/yr seat erosion on history, not -7%/yr.

## WS3: AI task-exposure synthesis (O*NET tasks x Eloundou/AIOE exposure x Adobe monetization)

- 102 O*NET 27.2 tasks across six occupations were classified into workflow stages (keyword rules then 100% hand review,
  85% agreement). The three most exposed creative stages (ideation 100%, asset generation 98%, editing 88% of task
  weight highly exposed) are seat-monetized; 72% of highly exposed creative task weight is in seat stages vs 1% in
  usage stages.
- Creative exposure is "LLM plus image tools" (E2), not direct LLM (E1): human alpha for graphic designers is 0.00 (15th
  percentile) but gamma is 0.82-0.90 (83rd-93rd percentile); image-generation AIOE puts all four creative occupations at
  the 98th-100th percentile. Exposure is a tooling story Adobe can own or lose.
- Marketing occupations are equally exposed (human gamma 0.92-0.94) but their dominant analytics tasks (59% of
  six-occupation weight, 93% exposed) map to Experience Platform/Analytics, an enterprise platform, not seats.
- Best chart: `ws3_task_exposure/charts/exposure_by_stage.png`
- Confidence: medium (labels date from early 2023; O*NET omits modern resize/localize work, so the usage-stage
  opportunity is understated). Impact: WEAKENS the "usage monetization covers the exposed stages" leg; SUPPORTS the
  "marketing/enterprise revenue is platform-protected" leg. Maneet to spot-check the 15 hand overrides.

## WS4: earnings-call text analysis

PENDING: workstream still running at the time of this draft; section will be replaced when it reports.

## WS5: search interest and competitor benchmarks

- The creative-tools pool (Adobe C&MP + Figma + Canva run-rates, ~$23.8B) grows ~16.5%/yr vs Adobe C&MP ~13%; Adobe
  holds 78% of the stock but 64% of the latest annualized increment ($2.14B of $3.36B). Adobe is not shrinking: it adds
  more creative dollars per year than Figma and Canva combined.
- Figma: FY25 revenue $1.056B (+41%); Q2 2026 $370M (+48%, third straight acceleration); net dollar retention 136%;
  customers over $100k ARR +46% to 1,635; FY26 guide $1.463-1.467B.
- Canva: ARR ~$4.0B at end-2025 (+43%, estimate; 265M MAU, 31M paid) but Q2 2026 revenue +25% and 2026 growth guide
  cut from 30% to ~20% on AI serving costs. Midjourney ~$500M 2025 revenue (third-party estimate).
- Google Trends: UNAVAILABLE (host blocked). Manual export instructions and a ready loader script are in
  `ws5_trends_competitors/data/`.
- Best chart: `ws5_trends_competitors/charts/incremental_revenue_dollars.png`
- Confidence: medium (Canva mixes ARR and revenue; Figma overlaps Creative Cloud only partly). Impact: MIXED. Pool is
  growing (SUPPORTS); Figma is a clear share-taker (WEAKENS).

## WS6: channel-check kit (no data)

- Deliverables: `ws6_channel_checks/interview_guide.md` (three one-page variants, 6-7 questions each with probes and a
  SUPPORTS/WEAKENS coding table), `google_form_questions.md` (screener + 14 items mapped to B1/B2/usage/competition),
  `responses_template.csv` (22 columns, two clearly labeled example rows), `outreach_message.md`.
- Sample target: 10-15 interviews and 30+ form responses; anecdotal by design.
- Confidence: n/a. Impact: NEUTRAL until responses are collected.

---

## Valuation inputs (Inputs tab of ADBE_alt_data.xlsx, all formulas)

Price $241.28 (Oct 1, 2026 close) x 389.2M shares = ~$93.9B market cap; net debt ~$0.7B; EV ~$94.6B. FY26 non-GAAP EPS
guide midpoint $24.475 gives ~9.9x. Nine-month FY26 operating cash flow $7,646M less capex $180M = $7,466M FCF
(~$9.95B annualized, ~9.5x EV/FCF, ~10.6% FCF yield on market cap before SBC of $1,582M for nine months).

## What completed, what failed

- Completed: WS1, WS2, WS3, WS5, WS6, workbook (Inputs, PriceVolume, SeatCompression, TaskExposure, Trends_Competitors,
  Sources), this summary, memo_snippets.md.
- Degraded: WS4 (see section). Google Trends (manual kit). Wayback price snapshots (replaced by help-article and news
  citations). All primary pages read via search snippets.
