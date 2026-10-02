# Similarweb manual collection protocol (C4 "users are coming to Adobe")

**Why manual:** Similarweb's ToS forbids automated collection; nothing here is scraped. One person, one browser,
~15 minutes for 8 domains. Free (logged-out) pages show the last 3 months; a free account shows a few more.

## Domains (collect all 8, same day)
firefly.adobe.com, express.adobe.com, acrobat.adobe.com, adobe.com, canva.com, figma.com, midjourney.com, chatgpt.com

## Steps per domain
1. Open `https://www.similarweb.com/website/<domain>/` (e.g. https://www.similarweb.com/website/firefly.adobe.com/).
2. On the overview card record, for EACH of the three months shown in the "Total Visits" mini-chart (hover each bar):
   `month` (YYYY-MM), `total_visits` (write the number exactly as shown, e.g. "12.4M" -> 12400000).
3. From the "Engagement" block (these are last-month values): `bounce_rate_pct`, `pages_per_visit`, `avg_visit_duration`
   (mm:ss), and `top_country` + `top_country_share_pct` from "Top Countries".
4. Record `date_collected` (today), `account_type` (free / logged-in free / paid) and `source_url`.
5. Enter rows in `similarweb_template.csv` (one row per domain x month for visits; engagement fields repeat on each row
   of the same domain or are left blank on older months).
6. Subdomain pages (firefly.adobe.com, express.adobe.com, acrobat.adobe.com) may show "not enough data" on the free
   tier; if so, record `total_visits` blank and `notes = "not shown on free tier"`. Do not estimate.

## Cautions
- Similarweb desktop+mobile web only; app usage (Acrobat Reader, Express mobile) is NOT captured. Compare with the
  Google Play protocol for the app side.
- adobe.com includes commerce, help and sign-in traffic; use it as a brand-level context series only.
- Free-tier numbers are modelled estimates; treat month-over-month moves <10% as noise.
- Do NOT save screenshots into the repo; numbers only.

## Then
`python data/load_similarweb.py` draws `charts/similarweb_visits_by_domain.png` (visits per month per domain).
`python data/load_similarweb.py --synthetic-test` runs on a clearly-labelled synthetic file only.
