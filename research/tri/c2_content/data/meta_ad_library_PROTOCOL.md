# Meta Ad Library manual collection protocol (C2: content-volume channel check)

Purpose: independent ("alt") evidence on whether large advertisers are running MORE distinct creatives
(variants) over time, as AI-generated-creative claims by Adobe/Meta/Google would imply. Manual, visual
collection only. Do NOT automate (Meta ToS). No logins required; the Ad Library is public.

## Where
https://www.facebook.com/ads/library  ->  Ad category: "All ads"  ->  Country: United States  ->  search by advertiser Page.
Set filters: Platform = All; Media type = All; Active status = Active ads; Impressions by date = default (unset).
Use a desktop browser, English UI, logged out (or logged in; results are the same for non-political ads).

## Brand list (20; 5 sectors x 4; fixed across waves — do not swap brands mid-series)
| sector | brand page (search string) | notes |
|---|---|---|
| CPG | Tide (P&G) | use the "Tide" page, not P&G corporate |
| CPG | Dove (Unilever) | US Dove page |
| CPG | Coca-Cola | "Coca-Cola" US page |
| CPG | Pepsi (PepsiCo) | "Pepsi" page |
| CPG/food | Nestle (e.g., Nescafe or Purina) | pick ONE page in wave 1 and keep it |
| Retail | Walmart | |
| Retail | Target | |
| Retail | Amazon | "Amazon" main page (ads are numerous; cap at first 50 results) |
| Retail/apparel | Nike | |
| Auto | Toyota USA | |
| Auto | Ford Motor Company | |
| Auto | Chevrolet (GM) | |
| Auto | Hyundai USA | |
| Travel | Marriott Bonvoy | |
| Travel | Hilton | |
| Travel | Expedia | |
| Travel | Booking.com | |
| Travel | Airbnb | |
| QSR | McDonald's | |
| QSR | Starbucks | |

## Per-brand fields (one row per brand per collection date)
1. date (YYYY-MM-DD) and local time; collector initials.
2. active_ads: the "~N results" count the Library shows at the top for Active ads, US, all media types. Record the integer shown
   (Meta shows "~" approximations above ~1,000; record as shown and set notes="approx").
3. distinct_creatives_first50: scroll to load the FIRST 50 result cards. Count distinct creatives, where "distinct" = a different
   image/video OR different primary text. Same copy + different image/video counts as separate creatives (that is a variant).
   Language/size versions of the same image+copy count as ONE creative (they are shown under "multiple versions").
4. pct_with_multiple_versions: among the same first 50 cards, share (0-100) carrying the "This ad has multiple versions" label.
   Click 3 of them and note the number of versions shown (write the three counts in notes, e.g., "versions: 4/12/3").
5. notes: anything odd (page renamed, political-ad filter, regional pages, very long videos, AI-disclosure label
   "Made with AI"/"AI info" if visible — count how many of the 50 cards carry an AI label and record as ai_label_count=N).

## Cadence
Wave 1 now; then the first business day of each month for 6 months; plus one wave the week after Black Friday.
Each wave takes ~90-120 minutes for 20 brands. Keep the same collector where possible; if the collector changes, run 3 brands
by both collectors on the same day and record both rows (inter-rater check).

## Known biases / caveats (state in the write-up)
- Active-ad counts measure BREADTH of live creative, not spend. Retail/QSR counts spike around promotions; compare like-for-like months.
- "~" counts are rounded; treat changes <10% as noise.
- The first-50 ordering is Meta's relevance/recency sort and is not a random sample; it is a repeatable convenience sample.
- A rising count of versions is consistent with dynamic/Advantage+ creative (Meta's tools), not necessarily Adobe's. The check tests
  the CONTENT-VOLUME premise of C2, not Adobe's share of it.
- Small non-random sample (20 brands); report as "N/20 brands with higher active ads vs wave 1", in the style of the author's prior pitch.

## Files
- data/meta_ad_library_template.csv : blank template (columns fixed).
- data/load_meta_ad_library.py : loads all filled CSVs matching data/meta_ad_library_*.csv (excluding template/synthetic unless
  --include-synthetic), builds a brand x date panel, and charts active ads per brand over time plus the median index.
