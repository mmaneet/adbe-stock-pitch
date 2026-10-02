# C3 economics: methods (Subagent C, 2026-10-02)

## Host probe results (curl -m 12, research UA; re-probed with WebFetch where curl failed)
| host / page | curl | WebFetch | used |
|---|---|---|---|
| adobe.com IR transcript PDFs (q1fy25-q3fy26) | 200 | - | pypdf text extraction to scratchpad; quotes <25 words only |
| sec.gov / data.sec.gov (submissions, companyfacts, 10-Q/10-K/8-K HTML) | 200 | - | Adobe, Figma, Shutterstock, Getty filings parsed with BeautifulSoup |
| adobe.com/products/firefly/plans.html | 200 | OK | Firefly plan prices and credits (verified) |
| adobe.com/creativecloud/plans.html | 200 (research UA) | OK (served CAD prices) | CC Pro credits count not on page |
| helpx.adobe.com (generative-credits FAQ, both URLs) | 403 | 403 | UNAVAILABLE -> NEEDS_MANUAL; credits-per-image from search snippets (N) |
| business.adobe.com firefly-ai-approach (indemnity) | 000 | 503 x2 | UNAVAILABLE -> snippets (N) |
| canva.com (newsroom, pricing, Canva Shield) | 403 | 403 | WebSearch only (N) |
| investor.figma.com | 403 | - | figma.com/pricing 200 (verified); s206.q4cdn.com prepared-remarks PDF 200 (verified) |
| midjourney.com/pricing | 200 (JS shell, 4.9KB) | empty | plan data from secondary (N) |
| docs.midjourney.com | 403 | - | (N) |
| openai.com (api/pricing, business terms), help.openai.com | 403 | 403 | developers.openai.com/api/docs/pricing via WebFetch OK (token rates verified) |
| cloud.google.com Vertex pricing (redirects to gemini-enterprise-agent-platform/...) | 200 | truncated | curl + regex: Imagen 1-4 prices verified |
| ai.google.dev/gemini-api/docs/pricing | 200 (903B shell) | OK | Nano Banana / NB Pro / NB2 prices verified |
| cloud.google.com/terms/generative-ai-indemnified-services | 200 | - | verified |
| mckinsey.com PDF | 000 | - | UNAVAILABLE |
| deloitte.com press pages | - | OK | 2024 survey verified (35% IP concern) |
| fortune.com, forbes.com.au, sprinter.com.au, thesaascfo.com | - | OK | Canva letter numbers (secondary) |
| web.archive.org | blocked (not probed, per ENV notes) | | API price history uses dated announcement posts instead |

## Steps
1. Company: parsed condensed consolidated income statements from 8 Adobe filings (10-Q FY24Q1-FY26Q3, 10-K FY23-FY25) for subscription revenue, cost of subscription revenue, total revenue, cost of revenue, gross profit, operating income; Q4 = annual minus 9M. Non-GAAP operating income, diluted shares, OCF and capex from the 8-K press-release reconciliation tables (Q1 FY25-Q3 FY26). Cost-of-subscription driver table copied from MD&A "Components of % Change" (hosting/data center incl. AI inferencing, compensation, royalties, amortization). AI-first / AI-influenced ARR wording taken from the transcripts and 8-K headlines; all are "more than" lower bounds.
2. Peers: Figma 10-Qs/10-K income statements and MD&A cost-of-revenue paragraphs; Figma Q2 2026 prepared remarks PDF; Shutterstock and Getty Q2 2026 10-Q MD&A regex; Canva from press coverage of the Q2 2026 shareholder letter (canva.com blocked).
3. Price per generation = monthly list price / included generations (or credits / credits-per-image). Assumptions are in the CSV `assumptions` column. Midjourney uses ~60 images per fast hour (4-image grid ~1 fast minute, secondary). ChatGPT Plus has no published quota; 1,000 images/month assumed.
4. API price history: current vendor pricing pages for levels (verified), launch dates from vendor posts/press (N where not fetched). Wayback blocked.
5. Indemnity: Google terms page (verified); Adobe, OpenAI, Canva, Midjourney from legal/press summaries (N). Surveys: Deloitte Q1 2024 wave (verified), McKinsey/Gartner (snippets, N).
6. EPS: subscription GM -1pt on FY26 subscription revenue ~$25.8B (9M actual $19.196B + Q4 implied ~$6.6B from the $6.80-6.85B revenue guide; task brief said ~$25.3B) = -$258M operating income x (1-18%) / 390M shares = -$0.54. AI-first ARR offset: $100M x 45% x 0.82 / 390M = $0.095. Shares: Q3 FY26 actual 395M, Q4 guide 389M; 390M used per ENV notes.

## Palette / chart check
Team palette (navy, teal, amber, red, grey) run through dataviz validator: CVD and normal-vision separation PASS (worst adjacent dE 12.7 deutan / 20.8 normal); lightness/chroma FAIL on navy and grey (deliberately dark/neutral), amber contrast WARN. Relief applied: every bar directly labeled, legends present, single axes (no dual-axis), hollow markers for unverified points.

## Limitations
- Adobe does not disclose hosting cost in dollars; only the percentage-point contribution to cost-of-subscription growth. Semrush (consolidated from 2026-04-28) adds lower-margin subscription revenue and intangible amortization in Q2-Q3 FY26; Adobe does not break out its gross margin, so the -0.8pt YoY Q3 subscription GM move cannot be cleanly split between AI inference and Semrush mix. Amortization contribution to cost growth was negative (-5pts), so the hosting line is the driver.
- Q1 FY26 AI-first ARR dollar figure is not disclosed anywhere found (press release, transcript, 10-Q); ">$375M" is derived from ">3x" on ">$125M" and is labeled derived.
- Canva is private; every Canva number is press-reported from a letter we could not read. Figma Q3 2025 GAAP gross margin (69%) includes IPO-related stock compensation.
- Credits-per-image for Adobe partner models and Figma image features are from help-center summaries, not the pages themselves (403).
- Getty-Shutterstock merger was terminated 2026-07-07 (not closed, contrary to the brief's premise); Getty trading was halted 2026-09-29 (press, N).
