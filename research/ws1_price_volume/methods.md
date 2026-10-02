# WS1 – Price vs volume: methods

Workstream question: bear argument B1 — "price increases are masking seat losses". Tested neutrally by decomposing
Adobe customer-group subscription growth (FY25 Q1 – FY26 Q3) into FX, inorganic (Semrush), price, and an implied
volume/mix residual.

## Environment constraints (read first)
* **Wayback Machine (web.archive.org) is BLOCKED** in this container, as are adobe.com, helpx.adobe.com, news.adobe.com,
  sec.gov and most news sites. Every number was obtained from **WebSearch snippets** (standard + extended mode); the cited
  URL is the primary document the snippet pointed to, and `sources.csv` says "retrieved via WebSearch snippet; page not
  fetchable from this environment" where applicable. Nothing in the data files comes from memory.
* Orchestrator "starting facts" (Q3 FY26 10-Q) were used for the exact Q3 FY26 / Q3 FY25 customer-group figures and
  cross-checked against WebSearch snippets of the 8-K exhibit (growth rates match). Discrepancy noted: one snippet quotes
  Q1 FY26 BP&C growth as 16%, another 15% (exact $1,782M / ~$1,530M = 16.5%).

## Steps
1. **Price-change log** (`data/price_log.csv`, 31 rows, 2022–2026): Adobe blog / helpx notices where the search engine
   surfaced them, else PetaPixel, dpreview, Fast Company, TechCrunch, CG Channel, Adobe community threads, and licensing
   consultancies (Schneider IT, Redress Compliance, licenseware) for teams/VIP changes. Rows record list prices only;
   `applies_to` = new / renewal / all. Rows with blank prices are NEW SKUs (Firefly plans, credit packs, Acrobat Studio,
   Creative Cloud Standard) or events whose magnitude could not be tied to a URL.
2. **Quarterly revenue series** (`data/revenue_quarterly.csv`): total revenue, recast C&MP / BP&C subscription revenue,
   legacy Digital Media revenue, Digital Media ARR and Total Adobe ARR, FY24 Q1 – FY26 Q3. FY24 customer-group values and
   several FY24 Digital Media values are DERIVED by dividing FY25 figures by the disclosed growth rate (flagged in notes).
   FY26 Q2 C&MP/BP&C are back-solved from the 9-month 10-Q totals (13,577 / 5,540) less Q1 and Q3; press-release rounding
   ($4.54B / $1.85B) agrees. Legacy Creative vs Document Cloud quarterly revenue: UNAVAILABLE via snippets (blank).
3. **Price-contribution model** (`data/price_model.py` → `price_model.csv`, `decomposition.csv`):
   * Each price wave e has a blended list uplift u_e, an effective month, and a relative exposure r_e (1.0 for the broad
     waves Nov-2023 and Jun-2025; 0.3–0.4 for teams/VIP-only waves; 0.08 for the Photography plan).
   * Scenario share s = 10% / 20% / 30% (base 20%) = share of the customer group's subscription revenue that actually pays
     the new list price (i.e. excludes enterprise ETLAs, discounted/promo seats, the Standard downgrade, non-affected
     regions and SKUs). Effective exposure of a wave = s × r_e.
   * Renewal phase-in φ_e(t): annual plans renew uniformly, so the repriced fraction rises 1/12 per month for 12 months
     after the effective month (Adobe applies the new price "at next renewal"). Sensitivity: 100% at the effective date
     (month-to-month behaviour). Acrobat Pro new-customer-only increase (Aug-2022) phases in over 24 months.
   * Monthly price index P_g(t) = Π_e (1 + u_e · s · r_e · φ_e(t)); quarterly index = mean of the 3 months; price
     contribution to YoY growth = P_g(q)/P_g(q−4) − 1. `price_model.csv` gives the additive per-event approximation.
   * Implied volume/mix growth = (1 + organic cc growth) / (1 + price contribution) − 1.
4. **Organic constant-currency growth** = exact reported growth (from $ figures) − FX (reported minus constant-currency
   growth from the press release, integer-rounded, so ±0.5pt noise) − Semrush contribution in growth points.
5. **Semrush strip-out**: closed 2026-04-28; Adobe disclosed ~$40M revenue in Q2 FY26 (~1 month) and ~$480M ARR.
   Semrush's last standalone quarter was Q4-2025: $117.7M (+15% YoY), FY2025 $443.6M, ARR $471.4M. **Q1-2026 standalone
   revenue: UNAVAILABLE** (no results/guidance published ahead of the Adobe close). Q3 FY26 (full quarter) contribution is
   NOT disclosed; estimated at ~$120M from three consistent anchors: FY26 guide includes ~$280M Semrush (280 − 40 over
   Q3+Q4), Q4-25 run-rate $117.7M, and $480M ARR / 4. Range $110–125M → ±0.3pt on C&MP growth.
6. **Charts**: `charts/price_vs_volume_stacked.png` (C&MP; left panel base-case stacked bars with organic cc growth line,
   right panel implied volume under 10/20/30% and the month-to-month sensitivity); `charts/bpc_price_vs_volume_stacked.png`
   (same for BP&C).

## Assumptions and limitations (read before quoting any number)
* **List vs realised price.** The model uses list uplifts. Realised uplift is lower: existing All Apps members could
  downgrade to Creative Cloud Standard ($54.99, −8% vs the old $59.99), students/teachers and promo cohorts pay less, and
  Photography subscribers could keep ~$9.99 by prepaying annually. The scenario share s is the only lever capturing this,
  so "30% repriced" is a deliberately harsh case.
* **Enterprise agreements (ETLA) and VIP discounts** are multi-year and insulated from list changes until renewal;
  teams/VIP increases are therefore given r_e ≤ 0.4. The June-2026 VIP increase magnitude is a secondary-source claim
  (5–22% by SKU); the model uses +5%.
* **Downgrades/mix**: migration to Standard, Firefly/Express standalone plans, Acrobat Studio and AI Assistant add-ons all
  sit inside the "volume/mix" residual — the residual is NOT a seat count. A positive residual is consistent with flat seats
  plus up-sell; a negative residual would be strong evidence of seat loss.
* **Renewal timing is unobservable.** Uniform monthly renewals is an assumption; if renewals cluster (e.g. Black Friday
  cohorts) the quarterly phasing shifts by 1–2 quarters but the 4-quarter sum is unchanged.
* **FX**: constant-currency growth is only disclosed per customer group from Q4 FY25; earlier quarters use the company /
  Digital Media gap (noted per quarter in `decomposition.csv`). Integer rounding adds ±0.5pt noise.
* **Express / Firefly / AI-first ARR** are mix, not price: Express Premium has stayed $9.99 since 2023; Firefly plans are
  new SKUs (Pro re-tiered from $29.99 to $19.99 / Pro Plus $49.99 — date UNAVAILABLE). AI-first ARR >$650M (+150%) is
  ~2.4% of total ARR and is part of the residual.
* **Unverified events** (Acrobat Standard individual $12.99→$14.99, date unknown; Acrobat Standard business April-2026
  magnitude unknown; secondary-blog claim of a 15-Jan-2026 consumer increase) are excluded from the base and shown in the
  `incl_unverified` columns.
* **Seat counts**: Adobe last disclosed Creative Cloud subscribers in FY2018 (17M); nothing here measures seats directly.
* FY24 customer-group values are derived from rounded growth rates (±1%); FY24 quarters are context only and not used in
  the decomposition.
