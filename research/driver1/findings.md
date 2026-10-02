# Driver 1 tests: "the 2026 net new ARR slowdown is mostly deferred pricing + freemium, not paid churn"

Date: 2026-10-02. Inputs: research/ws1_price_volume (price log, price/volume decomposition), ws5_trends_competitors, tri/concessions (net new ARR rebuilt at Dec-2025 FX; management quotes), tri/c1_mix, tri/c3_economics, tri/c4_users (Google Trends pulls), ws4_call_nlp transcripts (FY23–FY24 net new ARR). One verification search was run for two dates (FTC/DOJ complaint 6/17/24; $150M settlement 3/13/26). Everything marked ESTIMATE is the author's; nothing else is new data. Scripts and tables: `run_tests.py`, `data/`. Charts are 3.1" x 1.6" at 300 dpi in `charts/`.

**Overall: PARTLY SUPPORTED, confidence medium-low.** On an H2-to-H2 basis, price-wave timing plus management's two self-attributed choices (deferred Creative Cloud price actions, freemium routing) more than cover the $0.40B gap. On a full-year, price-adjusted basis the organic decline is still ~22%, H1 FY26 fell ~28% ex-price before the freemium shift was announced, and search-measured cancellation intent has roughly doubled its baseline in 2026. The data rule out a visible paid migration to Canva; they do not rule out paid churn.

## Test 1. Price-adjusted bridge (H2 FY25 vs H2 FY26)

**Assumptions (ESTIMATE, from WS1).** Base = Creative & Marketing Professionals subscription revenue run-rate, Q4 FY25 $4.25B x 4 = $17.0B (the base WS1's "share repriced" scenarios apply to). Share repriced by the 6/17/25 Creative Cloud Pro increase: 10% / 20% / 30% (low / base / high). Blended list uplift 11.1% / 15% / 16.7% (teams +11.1%, individual +16.7%, NA only). Renewal timing: month-to-month share 0% / 20% / 30% repriced at once, annual plans uniformly over 12 months. 2026 actions (VIP list +5% from 6/1/26, Acrobat Standard business 4/1/26) add $0.05–0.12B in H2 FY26. Net new ARR is organic Total Adobe ARR at Dec-2025 rates (tri/concessions); Q1 FY25 estimated; Q4 FY26 implied by the 10.2% target.

| $B | H1 FY25 | H1 FY26 | H2 FY25 | H2 FY26e | FY25 | FY26e |
|---|---|---|---|---|---|---|
| Reported organic net new ARR | 1.05 | 0.96 | 1.58 | 1.18 | 2.63 | 2.14 |
| June-2025 price wave landing in period (base) | 0 | 0.20 | 0.29 | 0.02 + 0.09 (2026 actions) | 0.29 | 0.31 |
| Ex-price (base) | 1.05 | 0.76 | 1.29 | 1.07 | 2.34 | 1.83 |
| Change, reported | | −9% | | **−25%** | | −19% |
| Change, ex-price (base; low–high range) | | **−28%** (−17% to −37%) | | **−17%** (−3% to −25%) | | **−22%** (−20% to −22%) |

Bridge, H2 FY25 → H2 FY26 (base): price-wave lapping −$0.18B (range −$0.03B to −$0.40B, i.e., 7–100% of the gap); deferred Creative Cloud price actions −$0.24B and freemium routing −$0.24B (management's ~$0.48B organic cut, "maybe half" each, Q2 FY26 call); residual +$0.26B. The identified non-churn items over-explain the H2 gap, which means management's $0.48B overlaps the lapping wave (the deferred "line optimizations" were the wave that would have replaced it) or is overstated.

**Result.** SUPPORTS on the H2 framing: price timing and management's own choices exceed the H2 gap. WEAKENS on the full year: the June-2025 wave put almost as much ARR into FY26 (H1 renewals) as into FY25, so ex-price FY26 is still down ~22%, and H1 FY26 fell 17–37% ex-price despite a price tailwind. The CFO had already said in March 2026 that the freemium offerings "have a near-term impact on ARR," so part of H1 is the same choice, but no quantity was given. Confidence: medium-low (every price input is an estimate; Q4 FY26 is implied; the $0.48B is management's own attribution).

## Test 2. History: net new ARR around price actions

Series (quarterly, $M). Digital Media net new ARR from the earnings calls: FY23 410 / 470 / 464 / 569; FY24 432 / 487 / 504 / 578; FY25 410 / 460 / 500 / 610 (derived from reported ending ARR). Total Adobe ARR at Dec-2025 rates: FY25 470e / 580 / 660 / 920; FY26 400 / 560 (ex-Semrush) / 400 / 780 implied. Price actions marked: Apr-22 teams +6%; Aug-22 and Jul-23 Acrobat Pro +33%; Nov-23 All Apps +9%, teams +6% (NA, LatAm, Europe; APAC Mar-24); Jan-25 Photography; Jun-25 CC Pro +16.7%, teams +11.1% (NA); Apr/Jun-26 VIP.

| Window | YoY change in net new ARR (like basis) | Read |
|---|---|---|
| 4 quarters after Nov-23 wave (FY24 Q1–Q4, DM) | +5%, +4%, +9%, +2% | Rise, but Creative Cloud net new ARR fell YoY in Q1–Q2 FY24 (289 vs 307; 322 vs 354); the lift came from Document Cloud after the Acrobat Pro increases |
| Lapping year (FY25 Q1–Q3, DM) | −5%, −6%, −1% | Dip, as the mechanism predicts |
| After Jun-25 wave (FY25 Q4, DM / total) | +6% / n.a. | Rise |
| FY26 (total basis) | −15%, −3%, −39%, −15%e | Q1–Q2 fell before the wave lapped (they carried a price tailwind); Q3 is the first lapping quarter |

**Result.** Direction SUPPORTS: price waves have produced a rise-then-dip cycle twice. Magnitude WEAKENS: the historical lapping dip was 1–6%; FY26's dips are 3–39%, three to seven times larger, and two of them occurred before lapping. History says price timing is a minority of the 2026 decline. Confidence: medium (basis changes from Digital Media to Total Adobe ARR in FY26; FY25 DM figures derived; the 12/13/23 call already flagged the first sub-$400M Creative net new ARR quarter since 2018).

## Test 3. Migration: rivals and freelance platforms vs Adobe

| Entity | Prior | Latest | Source |
|---|---|---|---|
| Figma revenue | FY25 +41% | Q2 2026 **+48%**; NDR 136% | 10-Q / 8-K |
| Canva | CY25 ARR +43% (est.) | Q2 2026 revenue **+25%**; 2026 guide cut 30% → 20% | press-verified; letter private |
| Adobe BP&C subscription | Q4 FY25 +15% | Q3 FY26 **+16%** | 8-K |
| Adobe C&MP subscription | Q4 FY25 +11% | Q3 FY26 **+13%** (incl. ~2.9 pts Semrush) | 8-K |
| Adobe C&MP organic cc | ~10% | **~9.1%** | WS1 (Semrush ESTIMATE) |
| Upwork GSV | Q1 2026 AI-related GSV +40% | Q2 2026 **−4%** (AI-related +22%) | SEC release |
| Fiverr revenue | FY25 | Q2 2026 **−10%**; FY26 guide −14% to −17% | 8-K |

Share of the Adobe-C&MP + Figma + Canva pool (WS5, latest annualized): Adobe 78.3% of stock, 63.6% of the increment; Figma 6.2% / 14.3%; Canva 15.5% / 22.1%.

**Result.** SUPPORTS on the consumer leg: a paid migration from Adobe's individual base would show up at Canva, and Canva's growth has instead halved and its 2026 guide was cut. Mild WEAKENS on the enterprise leg: Figma is accelerating with 136% net retention, which is share gain in product/UX seats, where Adobe's teams/enterprise Creative Cloud is nonetheless described as strong. Fiverr and Upwork show demand destruction at the low end (seat compression), not migration. Adobe's organic C&MP slowdown is about one point, not a migration signature. Confidence: medium.

## Test 4. Churn-search timing

Google Trends "cancel adobe", US, monthly (churn-only request R4; October 2026 partial month dropped). Annual average index: 10 (2019), 13, 11, 16, 16, 17 (2024), 21 (2025), **51 (2026 YTD)**. Event-window lift (event month plus next month vs trailing 12 months): Nov-23 price −5%; FTC/DOJ complaint 6/17/24 +9%; Photography plan 1/15/25 +18%; CC Pro 6/17/25 +13%; $150M settlement 3/13/26 and CMA probe 3/19/26 +15%; VIP/list price rises 6/1/26 **+68%**. The largest spike (Feb 2026 = 100) precedes the settlement by two to four weeks; the only dated candidate in our logs is a claimed mid-January 2026 consumer price increase (secondary blogs only, unverified). Between the two 2026 spikes the index ran 32–48, about twice the 2025 average.

**Result.** Spikes align with Adobe's own price dates more than with the DOJ case (the 2024 complaint produced a +9% lift; the June 2026 price rises +68%). That is consistent with Driver 1's mechanism (price-led revenue provokes cancellation intent) but it is NEUTRAL-to-WEAKENS for "not paid churn": the 2026 baseline doubled between events, and search intent is not a churn measure. Confidence: medium (relative index, re-sampled per pull; same-day re-pull matched).

## What would settle it

Q4 FY26 net new ARR against the ~$0.78B implied by guidance; whether management quantifies the freemium drag; Survey B questions 1 and 5 (cancelled or downgraded; expect to keep Creative Cloud) in the channel check.

## Memo-ready evidence sentence (58 words)

Price timing and Adobe's own choices account for the H2 FY26 net-new-ARR gap: the June-2025 increase added roughly $0.2–0.3B to H2 FY25, deferred price actions and freemium routing cost about $0.48B, Canva's growth halved rather than absorbing Adobe refugees, and cancellation searches spiked on Adobe's price dates, not on the DOJ case.

Source notes: Adobe IR data sheet 9/10/26 (Total ARR at Dec-2025 rates); Q2 FY26 call 6/11/26 (~$0.48B organic cut, "maybe half" deferred pricing); price-wave sizing is the author's ESTIMATE from the WS1 price log and scenarios; Canva Q2 2026 figures press-verified (Startup Daily, B&T, Fortune, Forbes AU); Google Trends via pytrends 10/2/26; FTC press release 6/17/24; Bloomberg 3/13/26.

## Files

- `data/test1_price_adjusted_bridge.csv`, `data/test1_bridge_steps.csv`
- `data/test2_net_new_arr_history.csv`, `data/test2_yoy_like_basis.csv`, `data/test2_price_actions.csv`
- `data/test3_migration_table.csv`, `data/test3_share_of_pool.csv`
- `data/test4_cancel_adobe_spikes.csv`, `data/test4_event_window_lift.csv`, `data/test4_cancel_adobe_annual_avg.csv`
- `charts/driver1_fig1_bridge.png`, `charts/driver1_fig2_nnarr_history.png`, `charts/driver1_fig3_migration.png`, `charts/driver1_fig4_cancel_adobe.png`
- Palette note: the project palette fails the dataviz chroma check on navy and grey; every chart carries direct value labels and a legend or title naming the single series as relief.
