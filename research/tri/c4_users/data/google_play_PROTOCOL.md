# Google Play manual collection protocol (install-tier milestones)

**Why manual:** Google Play's ToS forbids automated scraping, and web.archive.org is blocked from the research
container. Everything below is done by hand in a browser (~20 minutes). Record numbers only; no screenshots in the repo.

## Apps and package IDs
| app | package_id | listing URL |
|---|---|---|
| Adobe Express | com.adobe.spark.post | https://play.google.com/store/apps/details?id=com.adobe.spark.post |
| Adobe Firefly | com.adobe.firefly | https://play.google.com/store/apps/details?id=com.adobe.firefly |
| Photoshop Express | com.adobe.psmobile | https://play.google.com/store/apps/details?id=com.adobe.psmobile |
| Adobe Acrobat Reader | com.adobe.reader | https://play.google.com/store/apps/details?id=com.adobe.reader |
| Canva | com.canva.editor | https://play.google.com/store/apps/details?id=com.canva.editor |
| CapCut | com.lemon.lvoverseas | https://play.google.com/store/apps/details?id=com.lemon.lvoverseas |

(If a package ID 404s, search the app name on play.google.com and copy the `id=` from the URL into `package_id`.)

## Today's values (one row per app, snapshot_date = today)
1. Open the listing URL. Under the app title, read the three tiles: rating ("4.6 star"), review count ("832K reviews")
   and install tier ("100M+ Downloads"). Record `install_tier` exactly as shown (e.g. `100M+`), `reviews` as a number
   (832K -> 832000), `rating` (4.6). `source_url` = the listing URL.

## Historical milestones via the Wayback Machine (one row per snapshot)
For each app open the calendar view and pick ~2 snapshots per year, 2021-2026 (Jan and Jul if available):
- https://web.archive.org/web/2021*/https://play.google.com/store/apps/details?id=com.adobe.spark.post
- https://web.archive.org/web/2022*/https://play.google.com/store/apps/details?id=com.adobe.spark.post
- https://web.archive.org/web/2023*/https://play.google.com/store/apps/details?id=com.adobe.spark.post
- https://web.archive.org/web/2024*/https://play.google.com/store/apps/details?id=com.adobe.spark.post
- https://web.archive.org/web/2025*/https://play.google.com/store/apps/details?id=com.adobe.spark.post
- https://web.archive.org/web/2026*/https://play.google.com/store/apps/details?id=com.adobe.spark.post
Repeat with `id=com.adobe.firefly` (2025*, 2026* only; app launched mid-2025), `id=com.adobe.psmobile`,
`id=com.adobe.reader`, `id=com.canva.editor`, `id=com.lemon.lvoverseas`.
On each snapshot record the same three tiles; `snapshot_date` = the Wayback timestamp (YYYY-MM-DD); `source_url` = the
full web.archive.org URL of that snapshot. Older (pre-2022) snapshots show "Installs 100,000,000+" in a details table
instead of a tile; record it as `100M+`.

## Notes
- Install tiers are coarse (10M+, 50M+, 100M+, 500M+, 1B+); a tier change dates a milestone only to within the
  snapshot interval. Review counts are the finer-grained proxy for cumulative adoption.
- Google Play covers Android only; iOS App Store does not publish download tiers (ratings count is the only proxy).

## Then
`python data/load_google_play.py` draws `charts/google_play_reviews_by_app.png` (review count over snapshot dates,
install-tier changes annotated). `--synthetic-test` runs on a clearly-labelled synthetic file only.
