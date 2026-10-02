# WS4 methods — earnings-call NLP (ADBE, FY23 Q1 – FY26 Q3)

Date run: 2026-10-02. Workstream folder: `research/ws4_call_nlp/`. Scripts: `scripts/parse_calls.py` (parsing, keyword classification, vocab; reads raw downloads from the session scratchpad) and `scripts/build_outputs.py` (hand labels, degraded rows, fear index, prices, forward P/E, charts); outputs in `data/` and `charts/`.

## Mode used: HYBRID (full text for 13 of 15 calls; degraded WebSearch reconstruction for 2)

All commercial transcript hosts are blocked from this container (fool, seekingalpha, stockanalysis, benzinga, investing.com, roic, gurufocus, discountingcashflows, equibles, alphastreet, marketbeat, insidermonkey, stocklight, alphaspread, biggo, financialcontent, stockstory, yahoo — all probed, all 403/egress-blocked). Full transcripts were found instead as files inside public GitHub repositories (GitHub code search via the GitHub MCP tool, then download via raw.githubusercontent.com, 2 s sleep between calls, UA with contact e-mail). Clean uniform copies are saved in `data/transcripts/<fy>_<q>.txt`.

| Call | Date | Source file (repo / path) | Format | Status |
|---|---|---|---|---|
| FY23 Q1 | 2023-03-15 | mustafaazad03/vectorsearch `src/data/ADBE_transcripts/20230315 …txt` | S&P CapIQ layout | full |
| FY23 Q2 | 2023-06-15 | same repo, `20230615 …` | CapIQ | full |
| FY23 Q3 | 2023-09-14 | same repo, `20230914 …` | CapIQ | full |
| FY23 Q4 | 2023-12-13 | same repo, `20231213 …` | CapIQ | full |
| FY24 Q1 | 2024-03-14 | same repo, `20240314 …` | CapIQ | full |
| FY24 Q2 | 2024-06-13 | same repo, `20240613 …` | CapIQ | full |
| FY24 Q3 | 2024-09-12 | Ngafney/garda-spring26 `amir/transcripts/adobe/2024/Q3/ADBE_2024-10-10_Q3.txt` (file name carries scrape date; content verified as the Sep-12-2024 call: revenue $5.41B) | Fool-style ("--" title lines) | full |
| FY24 Q4 | 2024-12-11 | same repo `2024/Q4/ADBE_2024-12-12_Q4.txt` | Fool-style | full |
| FY25 Q1 | 2025-03-12 | same repo `2025/Q1/ADBE_2025-03-13_Q1.txt` | Fool-style | full |
| FY25 Q2 | 2025-06-12 | **none found on GitHub** | — | **partial: WebSearch reconstruction (2 of ~12 questions)** |
| FY25 Q3 | 2025-09-11 | bencrowe0/citibank-arp `outputs/p2_adobe_ext2026_08_13/extracted/ADBE_FQ3_2025.txt` (press release + Insider Monkey transcript, single line) | "Name: text" one-liner | full |
| FY25 Q4 | 2025-12-10 | yurukatsu/lseg-transcript-web `data/transcripts/16547194.json` (LSEG structured JSON; Ngafney and citibank-arp copies used as cross-checks) | JSON turns | full |
| FY26 Q1 | 2026-03-12 | Ngafney/garda-spring26 `2026/Q1/ADBE_2026-03-13_Q1.txt` | "Name:" line style | full |
| FY26 Q2 | 2026-06-11 | bencrowe0/citibank-arp `…/ADBE_FQ2_2026.txt` | one-liner; **source contains Q&A only (no prepared remarks)** | full Q&A, prepared remarks UNAVAILABLE |
| FY26 Q3 | 2026-09-10 | **none found on GitHub** (call is 3 weeks old) | — | **partial: WebSearch reconstruction (6 of ~12 questions)** |

Exact raw URLs are in `sources.csv`.

## Parsing
Five format-specific parsers produce uniform turns (call, section prepared/Q&A, speaker, role mgmt/analyst/operator, firm, text) → `data/turns.csv`. Roles: Adobe surnames (Narayen, Wadhwani, Chakravarthy, Durn, Vaas, Day, Clark) = management; "Operator"; everything else = analyst. Q&A start = explicit section header where present, else the first operator turn that introduces a question. An **analyst question** = one analyst turn in the Q&A with ≥8 words and (a "?" or ≥25 words); consecutive turns by the same analyst with no management reply in between are merged; a follow-up after a management answer counts as a separate question. Firms come from the participant header (CapIQ/LSEG) or from the operator's "from X with Y" intro.

## Topic rubric (one primary topic per question)
Keyword regexes score each category by number of distinct hits; highest wins; ties broken in the order leadership > AI disruption > seats/pricing > AI monetization > margins > DX > macro/other; zero hits → macro/other.
- **ai_disruption_competition**: disrupt*, competit*, Canva, OpenAI/ChatGPT/GPT, Sora, Midjourney, Veo/Gemini/Imagen/Nano Banana, moat, commoditiz*, displace*, cannibal*, threat*, Figma, Runway, open-source, lose/take share, substitut*, deflation*, replace*, frontier/third-party/partner model, ad platform*, hyperscaler*.
- **seats_pricing_retention**: seat(s), per-user/per-seat, price/pricing/price increase, net retention/NRR, churn, retention, subscriber*, ARPU, tier(s), freemium, conversion/convert*, downgrade*, line optimization*, net new ARR, Digital Media/Creative ARR, ARR growth/guide, MAU/monthly active, user growth, discount*, packag*/bundle*, upsell, renewal*.
- **ai_monetization**: Firefly, generative credit*, credit pack*, credit(s), AI-first/AI-influenced, Firefly Services, GenStudio, AI Assistant, consumption, usage-based, monetiz*, generations, custom model*, book of business, agent(s)/agentic, AI revenue/ARR, video model*, LLM Optimizer, Brand Concierge, foundry, content supply chain.
- **digital_experience**: Digital Experience/DX, AEP, Experience Platform/Cloud, enterprise*, Workfront, Marketo, Journey Optimizer, Real-Time CDP, Semrush, CXO, agencies, marketing/marketer*/CMO*.
- **margins_ai_costs**: margin*, opex, cost*, GPU*, compute, capex, inference, investment level*, headcount/hiring, efficien*, cash flow, buyback*/repurchase*, capital allocation, tax, profitab*, operating income.
- **leadership**: CEO, CFO, succession, transition*, retire*, search, board, leadership, reorg*, leaving/departure/successor/interim.
- **macro_other**: macro*, demand environment, linearity, FX, guidance/guide/outlook, seasonal*, RPO/cRPO, billings/bookings, regulat*/DOJ/FTC/antitrust, termination fee, tariff*, budget*, sales cycle*, geographies, SMB.

**Hand review.** All 133 full-text questions were read by the analyst (first 230 chars for every question; full text for 14 ambiguous ones) and relabelled where the keyword rule was wrong: 37 overrides → keyword-vs-hand agreement **72.2%** (exceeds the ≥20% review requirement; the whole set was reviewed, so no sampling error, but single-rater). Typical errors: "enterprise" pulling Firefly questions into DX; "ARR/RPO" generic growth questions landing in seats/pricing; tribute preambles in FY26 Q1 scoring "leadership". `data/analyst_questions.csv` keeps `topic_auto`, `topic_final`, `hand_override`.

## Fear index (`data/fear_index.csv`)
- **strict** = (AI disruption/competition + seats/pricing/retention questions) / all analyst questions, on hand labels.
- **broad** = strict ∪ questions flagged as net-new-ARR / Digital-Media-ARR growth / deceleration questions (regex flag), because that is where seat-compression worry is usually voiced on Adobe calls.
- `fear_index_keyword_only` is the pre-review value, for transparency.
- FY25 Q2 (n=2) and FY26 Q3 (n=6) rows are **partial coverage, LOW confidence**; they are plotted as unconnected hollow markers.

## Vocabulary (`data/vocab_counts.csv`)
Counts over all management text (prepared remarks + answers) per call, word-boundary, case-insensitive, per 10,000 management words. Seat vocab: seat, seats, per user, license, licenses, subscriber, subscribers. Usage vocab: credit, credits, consumption, usage, generations, Firefly Services, API/APIs, outcome, outcomes. FY26 Q2 is Q&A-only (4,804 words, no prepared remarks) and is therefore not comparable; FY25 Q2 and FY26 Q3 are UNAVAILABLE. `data/usage_term_first_mentions.csv` records the first call where management used each usage-monetization term, with context.

## Valuation overlay (`data/prices_at_calls.csv`, `data/forward_pe.csv`)
Daily closes from a yfinance-derived CSV mirrored on GitHub (fja05680/brownbear, through 2026-07-30; identical closes in rosidotidev/algo1 through 2026-08-14). Price used = close on the **next trading day** after the (after-market) call. The 2026-09-11 close ($252.23) comes from a news snippet via WebSearch and is unverified by a second source; the 2026-09-10 close is UNAVAILABLE. Forward P/E = next-day close ÷ midpoint of the FY non-GAAP EPS guidance in force after the call. Guidance was read from the CFO's prepared remarks in each transcript (press-release 8-K ex99.1 URLs listed); where the FY range was not restated on the call (FY23 Q3, FY24 Q3) it is implied as 9-month actual EPS + Q4 target; FY24 Q1 carries the Dec-2023 range (not updated on the call); FY25 Q2 and FY26 Q3 ranges come from WebSearch snippets of the 8-K. Anchors verified: FY23 initial $15.15–15.45 (per FY23 Q1 transcript reference), FY24 initial $17.60–18.00, FY25 initial $20.20–20.50, FY26 current $24.45–24.50.

## Coverage table
| Call | Questions | Coverage | Confidence |
|---|---|---|---|
| FY23 Q1–Q4 | 10/10/11/10 | full | medium |
| FY24 Q1–Q4 | 10/13/8/10 | full | medium |
| FY25 Q1 | 13 | full | medium |
| FY25 Q2 | 2 recovered (typical 12–15) | partial coverage | LOW |
| FY25 Q3 | 10 | full | medium |
| FY25 Q4 | 8 | full | medium |
| FY26 Q1 | 10 | full | medium |
| FY26 Q2 | 10 | full Q&A; no prepared remarks | medium (Q&A) |
| FY26 Q3 | 6 recovered (typical 12–15) | partial coverage | LOW |

## Limitations
- Transcripts are third-party mirrors (CapIQ, Motley Fool, Insider Monkey, LSEG) with ASR/typo noise ("brand Zelnick", "Adele" for Adobe); numbers quoted from them were cross-checked against press-release URLs where possible.
- Single rater for hand labels; categories overlap (a question can be both disruption and monetization); the strict/broad split is reported to show sensitivity.
- Vocabulary counts measure management framing, not revenue mix; "credit" can also mean credit facility (rare), "usage" is counted in all senses.
- The two degraded calls bias the FY25/FY26 picture: FY25 Q2 contributes almost nothing; FY26 Q3 topics come from summaries and may over-represent AI questions.
- n per call is 8–13, so single questions move the index by ~0.1.
