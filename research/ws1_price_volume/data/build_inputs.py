"""Build price_log.csv, revenue_quarterly.csv and sources.csv for WS1 (price vs volume).
All numbers below were retrieved via WebSearch snippets on 2026-10-02 (pages themselves are not
fetchable from this container; see ../methods.md). Nothing here is from memory."""
import csv, os
D = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(D)
ACC = "2026-10-02"
NOTE_WS = "retrieved via WebSearch snippet; page not fetchable from this environment"

# ---------------------------------------------------------------- price log
PL_COLS = ["effective_date","announce_date","product","plan_type","region","old_price","new_price",
           "pct_change","applies_to","source_url","notes"]
BLOG22 = "https://blog.adobe.com/en/publish/2022/03/22/creative-cloud-offering-price-update"
BLOG23 = "https://blog.adobe.com/en/publish/2023/09/13/ai-creative-cloud-release-pricing-update"
HELPX23_TEAMS = "https://helpx.adobe.com/x-productkb/policy-pricing/subscription-price-increase-2023-enterprise-teams.html"
HELPX23_IND = "https://helpx.adobe.com/sg/x-productkb/policy-pricing/subscription-price-increase-2023-individual-plans.html"
DPREV23 = "https://www.dpreview.com/news/1676880155/adobe-increases-creative-cloud-pricing-takes-firefly-out-of-beta/"
PETA23 = "https://petapixel.com/2023/09/15/adobe-hikes-creative-cloud-prices-as-it-reports-record-revenue/"
BLOG_PHOTO = "https://blog.adobe.com/en/publish/2024/12/15/all-new-photography-innovations-pricing-updates"
PETA_PHOTO = "https://petapixel.com/2024/12/18/adobe-is-ditching-their-cheapest-photography-plan-for-new-customers-now-what/"
HELPX25_IND = "https://helpx.adobe.com/account/individual/subscriptions-and-plans/plan-types-and-eligibility/changes-to-individual-plan.html"
HELPX25_TEAMS = "https://helpx.adobe.com/account/individual/subscriptions-and-plans/plan-types-and-eligibility/changes-to-teams-plan.html"
PETA25 = "https://petapixel.com/2025/05/20/if-you-have-adobe-creative-cloud-your-price-could-increase-next-month/"
FAST25 = "https://www.fastcompany.com/91337900/adobe-creative-cloud-pro"
SCHN_ACRO23 = "https://www.schneider.im/adobe-acrobat-pro-price-increase-reminder/"
COMM_ACRO23 = "https://community.adobe.com/t5/acrobat-discussions/2023-price-increase-for-adobe-pro/m-p/13536125"
TC_FF = "https://techcrunch.com/2025/02/12/adobe-launches-firefly-ai-subscriptions/"
PETA_FF = "https://petapixel.com/2025/02/18/adobe-now-sells-firefly-plans-but-photographers-dont-need-them-yet/"
HELPX_CREDITS = "https://helpx.adobe.com/creative-cloud/apps/generative-ai/generative-credits-faq.html"
FF_2026 = "https://aiproductivity.ai/pricing/adobe-firefly/"
ACRO_STUDIO = "https://news.adobe.com/news/2025/08/acrobat-studio-delivers-new-ai-powered-home-for-productivity-creativity"
SCHN_ACRO26 = "https://www.schneider.im/adobe-acrobat-standard-price-increase-announcement/"
SCHN_JUN26 = "https://www.schneider.im/adobe-acrobat-creative-cloud-others-price-increases/"
REDRESS26 = "https://redresscompliance.com/adobe-price-increase-2026-impact"
XODO = "https://xodo.com/blog/adobe-acrobat-pricing-explained"
RAVODY = "https://ravody.com/adobe-creative-cloud-acrobat-pricing-2026/"
G2_EXPRESS = "https://www.g2.com/products/adobe-express/pricing"
CGCH22 = "https://www.cgchannel.com/2022/03/adobe-to-raise-price-of-creative-cloud-subscriptions/"

def pct(o, n):
    return round((n / o - 1) * 100, 1)

price_log = [
 # 2022 wave (teams/enterprise + individual month-to-month)
 ["2022-04-27","2022-03-22","Creative Cloud for teams All Apps","teams, annual (per license/mo)","North America",79.99,84.99,pct(79.99,84.99),"renewal",BLOG22,"Applied at next renewal on/after 2022-04-27; enterprise (ETLA) also raised, amounts not public. Adobe blog."],
 ["2022-04-27","2022-03-22","Creative Cloud for teams Single App","teams, annual (per license/mo)","North America",33.99,35.99,pct(33.99,35.99),"renewal",CGCH22,"Teams single-app +$2; individual single-app plans explicitly unchanged in 2022."],
 ["2022-04-27","2022-03-22","Creative Cloud All Apps (individual)","individual, month-to-month","North America",79.49,82.49,pct(79.49,82.49),"renewal",BLOG22,"Only the month-to-month individual All Apps plan changed in 2022; annual plans unchanged."],
 # Acrobat 2022/2023
 ["2022-08-08","2022-08-08","Acrobat Pro (individual)","individual, annual billed monthly","US",14.99,19.99,pct(14.99,19.99),"new",SCHN_ACRO23,"Adobe described the Acrobat Pro increase as ~40% (some SKUs); community reports $15->$20/mo. New customers from 2022-08-08."],
 ["2023-07-01","2022-08-08","Acrobat Pro (individual) - existing subscribers","individual, annual billed monthly","US",14.99,19.99,pct(14.99,19.99),"renewal",COMM_ACRO23,"Existing subscribers with an active licence at 2022-08-08 repriced from 2023-07-01 at renewal."],
 # Nov 2023 wave (Firefly / generative credits)
 ["2023-11-01","2023-09-13","Creative Cloud All Apps (individual)","individual, annual billed monthly","NA, Central/South America, Europe",54.99,59.99,pct(54.99,59.99),"all",BLOG23,"New subscribers immediately; existing at next renewal. Firefly generative credits bundled. Adobe blog + helpx."],
 ["2023-11-01","2023-09-13","Creative Cloud All Apps (individual)","individual, month-to-month","NA, Central/South America, Europe",82.49,89.99,pct(82.49,89.99),"all",DPREV23,"dpreview quotes $82.50->$90."],
 ["2023-11-01","2023-09-13","Creative Cloud Single App (Photoshop, Illustrator, Premiere Pro etc.)","individual, annual billed monthly","NA, Central/South America, Europe",20.99,22.99,pct(20.99,22.99),"all",HELPX23_IND,"PetaPixel: $21->$23/mo annual-billed-monthly."],
 ["2023-11-01","2023-09-13","Creative Cloud Single App","individual, month-to-month","NA, Central/South America, Europe",31.49,34.49,pct(31.49,34.49),"all",PETA23,"PetaPixel/dpreview: $31.50->$34.50."],
 ["2023-11-01","2023-09-13","Creative Cloud for teams All Apps","teams, annual (per license/mo)","NA, Central/South America, Europe",84.99,89.99,pct(84.99,89.99),"renewal",HELPX23_TEAMS,"helpx 'Creative Cloud for teams and enterprise 2023 pricing changes'."],
 ["2023-11-01","2023-09-13","Creative Cloud for teams Single App","teams, annual (per license/mo)","NA, Central/South America, Europe",35.99,37.99,pct(35.99,37.99),"renewal",HELPX23_TEAMS,""],
 ["2023-11-01","2023-09-13","Firefly Premium (100 credits/mo) - NEW SKU","individual, monthly","Global","",4.99,"","new",DPREV23,"New add-on SKU, not a price change (excluded from price model)."],
 ["2024-03-05","2023-09-13","Nov-2023 wave extended to Africa, Asia, Australia","individual + teams","Africa, Asia, Australia","","","~10","all",HELPX23_IND,"Same ~10% structure as Nov-2023; local-currency amounts not captured."],
 # Jan 2025 photography / Lightroom
 ["2025-01-15","2024-12-15","Photography plan 20GB (Photoshop+Lightroom)","individual, annual billed monthly","Worldwide",9.99,14.99,pct(9.99,14.99),"renewal",BLOG_PHOTO,"Existing monthly-billed subscribers +50% at renewal; could keep $9.99 equivalent by switching to prepaid annual ($119.88). Retired for NEW subscribers."],
 ["2025-01-15","2024-12-15","Photography plan - new-subscriber entry point (20GB retired, 1TB only)","individual, annual billed monthly","Worldwide",9.99,19.99,pct(9.99,19.99),"new",PETA_PHOTO,"Mix effect for new subscribers only; 1TB plan price itself unchanged at $19.99."],
 ["2025-01-15","2024-12-15","Lightroom (1TB) plan","individual, annual billed monthly","Worldwide",9.99,11.99,pct(9.99,11.99),"all",BLOG_PHOTO,"Prepaid annual unchanged at $119.88; Lightroom Classic added to plan."],
 # Firefly standalone plans 2025
 ["2025-02-12","2025-02-12","Firefly Standard - NEW SKU","individual, monthly","Global","",9.99,"","new",TC_FF,"Launch (promotional) price; Adobe said subject to change 2025-03-15. New SKU, excluded from price model (mix)."],
 ["2025-02-12","2025-02-12","Firefly Pro - NEW SKU","individual, monthly","Global","",29.99,"","new",PETA_FF,"Launch price $29.99. By 2026 the lineup is Standard $9.99 / Pro $19.99 / Pro Plus $49.99 / Premium $199.99 (re-tier date UNAVAILABLE)."],
 ["2026-09-01","","Firefly lineup as of Sep-2026: Standard/Pro/Pro Plus/Premium","individual, monthly","US","",'9.99/19.99/49.99/199.99',"","new",FF_2026,"Third-party price tracker; Pro Plus & Premium 30% off first year through 2026-08-26. Date of re-tier from $29.99 Pro UNAVAILABLE."],
 ["2025-06-17","2025-05-20","Firefly generative credit add-on pack (100 credits)","add-on","Global","",4.99,"","new",HELPX_CREDITS,"helpx Generative credits FAQ; larger packs (2,000/4,000/7,000 credits) exist, prices not captured. Credit-tracking enforced from 2025-06-17 (PetaPixel 2025-06-24)."],
 # June 2025 CC Pro wave (North America)
 ["2025-06-17","2025-05-20","Creative Cloud All Apps -> Creative Cloud Pro (individual)","individual, annual billed monthly","North America",59.99,69.99,pct(59.99,69.99),"all",HELPX25_IND,"Existing All Apps members auto-renamed to Pro; new price at first renewal on/after 2025-06-17. New subscribers immediately."],
 ["2025-06-17","2025-05-20","Creative Cloud Standard (individual) - NEW lower tier","individual, annual billed monthly","North America",59.99,54.99,pct(59.99,54.99),"new",FAST25,"Downgrade option for existing All Apps members (-8.3% vs old All Apps price); fewer generative credits. Realised uplift on base therefore < list +16.7%."],
 ["2025-06-17","2025-05-20","Creative Cloud for teams All Apps -> Creative Cloud Pro for teams","teams, annual (per license/mo)","North America",89.99,99.99,pct(89.99,99.99),"renewal",HELPX25_TEAMS,"Teams All Apps renamed Pro for teams; old 'Pro Edition' renamed 'Pro Plus'."],
 ["2025-06-17","2025-05-20","Creative Cloud Single App (individual)","individual, annual billed monthly","North America",22.99,22.99,0.0,"all",HELPX25_IND,"Explicitly NO price change for single-app subscribers in June 2025."],
 ["2025-06-17","2025-05-20","Creative Cloud for teams Single App","teams, annual (per license/mo)","North America",37.99,37.99,0.0,"all",HELPX25_TEAMS,"Unchanged at $37.99 (licenseware summary)."],
 # Acrobat 2025-2026
 ["2025-08-19","2025-08-19","Acrobat Studio - NEW SKU (individual $24.99 / teams $29.99)","individual + teams, annual billed monthly","US","",24.99,"","new",ACRO_STUDIO,"Upsell tier above Acrobat Pro ($19.99); existing Standard/Pro customers offered up to 15% off to upgrade through 2026-10-31. Mix, not price."],
 ["2026-01-15","","Acrobat / Creative Cloud consumer 'broad increase' (claimed)","individual","US","","","","renewal",RAVODY,"LOW CONFIDENCE: only secondary blogs (ravody, redresscompliance) assert a 2026-01-15 consumer increase; no Adobe page or major outlet found. Acrobat Standard individual now lists $14.99 vs earlier $12.99 (+15.4%) per xodo/photutorial, date of that change UNAVAILABLE."],
 ["2026-04-01","2026-02-05","Acrobat Standard for business (Teams/Enterprise, VIP)","teams, annual (per license/mo)","Global (VIP)","","","","renewal",SCHN_ACRO26,"Adobe reseller notice; percentage NOT disclosed in sources. Current teams list $16.99/user/mo (xodo)."],
 ["2026-06-01","2026-02-01","VIP Marketplace list-price increase, most Creative Cloud & Acrobat SKUs (teams/enterprise)","teams/enterprise, annual","Global (VIP)","","","5 to 22 (range claimed)","renewal",SCHN_JUN26,"Schneider IT: broad increase esp. volume tiers (>=10 licences); Express, Stock, AI Assistant, Sign out of scope. Redress: Acrobat Pro teams $22.99->$23.99 (+4.3%); claims 5-22% by SKU. Enterprise ETLAs protected to term end."],
 ["2026-06-01","2026-02-01","Acrobat Pro for teams","teams, annual (per license/mo)","Global (VIP)",22.99,23.99,pct(22.99,23.99),"renewal",REDRESS26,"Secondary source (licensing consultancy)."],
 # Express
 ["2023-01-01","","Adobe Express Premium","individual, monthly or annual","US",9.99,9.99,0.0,"all",G2_EXPRESS,"No price change found 2023-2026: $9.99/mo or $99.99/yr throughout (G2/Capterra listings). Date column = start of observation window."],
]
with open(os.path.join(D,"price_log.csv"),"w",newline="") as f:
    w = csv.writer(f); w.writerow(PL_COLS); w.writerows(price_log)

# ---------------------------------------------------------------- quarterly revenue
RQ_COLS = ["fiscal_quarter","quarter_end","total_revenue_m","total_yoy_pct","total_yoy_cc_pct",
           "cmp_sub_rev_m","cmp_yoy_pct","cmp_yoy_cc_pct","bpc_sub_rev_m","bpc_yoy_pct","bpc_yoy_cc_pct",
           "digital_media_rev_m","dm_yoy_pct","dm_yoy_cc_pct","creative_rev_m","document_cloud_rev_m",
           "digital_media_arr_b","total_adobe_arr_b","total_arr_yoy_pct","semrush_rev_m","source_url","notes"]
SEC = "https://www.sec.gov/Archives/edgar/data/796343/"
Q124=SEC+"000079634324000057/adbeex991q124.htm"; Q224=SEC+"000079634324000140/adbeex991q224.htm"
Q324=SEC+"000079634324000200/adbeex991q324.htm"; Q424=SEC+"000079634324000250/adbeex991q424.htm"
Q125=SEC+"000079634325000052/adbeex991q125.htm"; Q225=SEC+"000079634325000064/adbeex991q225.htm"
Q325=SEC+"000079634325000102/adbeex991q325.htm"; Q425=SEC+"000079634325000135/adbeex991q425.htm"
Q126=SEC+"000079634326000048/adbeex991q126.htm"; Q226=SEC+"000079634326000109/adbeex991q226.htm"
Q326="https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm"
TENQ326="https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000156/adbe-20260828.htm"
rev = [
 ["FY24Q1","2024-03-01",5182,"","","3560","","","1330","","",3820,"","","","",15.76,"","","",Q124,"Total rev & DM ARR per press release. C&MP/BP&C DERIVED from FY25 recast growth rates (3.92B/1.10, 1.53B/1.15) - rounded. DM rev derived from Q1 FY25 release ('up from $3.82B')."],
 ["FY24Q2","2024-05-31",5309,"","","3655","","","1391","","",3880,"","","","",16.25,"","","",Q224,"C&MP/BP&C DERIVED (4.02B/1.10, 1.60B/1.15). DM rev derived (4.35B/1.12)."],
 ["FY24Q3","2024-08-30",5405,"","","3709","","","1433","","",4000,"","","","",16.76,"","","",Q324,"C&MP/BP&C DERIVED (4.117B/1.11, 1.648B/1.15). DM rev from Q3 FY25 release ('up from $4.00B')."],
 ["FY24Q4","2024-11-29",5614,"","","3829","","","1496","","",4160,"","","","",17.33,"","","",Q424,"FY24 total $21.51B; DM $15.86B; Document Cloud FY24 $3.18B. C&MP/BP&C DERIVED (4.25B/1.11, 1.72B/1.15). DM rev derived (4.62B/1.11)."],
 ["FY25Q1","2025-02-28",5714,10,11,3920,10,"",1530,15,"",4227,11,"","","",17.63,23.50,"","",Q125,"C&MP $3.92B/BP&C $1.53B from recast disclosure (rounded). Total Adobe ARR DERIVED from Q1 FY26 ($26.06B, +10.9%)."],
 ["FY25Q2","2025-05-30",5870,11,"",4020,10,"",1600,15,"",4350,12,"","","",18.09,24.08,"","",Q225,"Total Adobe ARR $24.08B as restated at FY26 currency rates (Q2 FY26 10-Q)."],
 ["FY25Q3","2025-08-29",5990,11,"",4117,11,"",1648,15,"",4459,12,11,"","",18.59,24.73,"","",Q325,"C&MP/BP&C exact from Q3 FY26 10-Q comparatives (orchestrator starting facts, matched by WebSearch '4.12B/1.65B'). Total ARR DERIVED from Q3 FY26 ($27.50B, +11.2%)."],
 ["FY25Q4","2025-11-28",6190,10,"",4250,11,10,1720,15,"",4620,11,"","","",19.20,25.66,"","",Q425,"FY25 total $23.77B (+11%). Total ARR $25.20B revalued to $25.66B at FY26 rates (FX). Digital Media ARR $19.2B (+11.5%)."],
 ["FY26Q1","2026-02-27",6400,12,11,4389,12,11,1782,16,"","","","","","","",26.06,10.9,0,Q126,"BP&C growth quoted as 16% in one snippet and 15% in another (1782/1530=16.5%). Semrush not yet owned."],
 ["FY26Q2","2026-05-29",6620,13,"",4537,13,11,1853,16,15,"","","","","","",27.10,12.5,40,Q226,"Semrush closed 2026-04-28: ~$40M revenue and ~$480M ARR in Q2. Q2 C&MP/BP&C back-solved from 9M FY26 totals (13,577 and 5,540) less Q1 and Q3; press release rounds to $4.54B/$1.85B. ARR growth 12.5% vs $24.08B restated."],
 ["FY26Q3","2026-08-28",6760,13,12,4651,13,12,1905,16,15,"","","","","","",27.50,11.2,120,Q326,"Semrush Q3 revenue NOT disclosed; 120 = ESTIMATE (FY26 guide includes ~$280M Semrush: 280-40 over Q3+Q4; Semrush Q4-25 standalone $117.7M; ARR $480M/4). AI-first ARR >$650M (+150%). 10-Q: "+TENQ326],
]
with open(os.path.join(D,"revenue_quarterly.csv"),"w",newline="") as f:
    w = csv.writer(f); w.writerow(RQ_COLS); w.writerows(rev)

# ---------------------------------------------------------------- sources.csv
S_COLS = ["claim","value","url","date_accessed","notes"]
src = [
 ["Adobe Q3 FY26 revenue","$6.76B, +13% reported / +12% cc",Q326,ACC,NOTE_WS],
 ["Adobe Q3 FY26 C&MP subscription revenue","$4,651M vs $4,117M (+13% / +12% cc)",TENQ326,ACC,"orchestrator starting facts (10-Q Q3 FY26); growth rates matched by WebSearch snippet of 8-K Ex 99.1"],
 ["Adobe Q3 FY26 BP&C subscription revenue","$1,905M vs $1,648M (+16% / +15% cc)",TENQ326,ACC,"orchestrator starting facts (10-Q Q3 FY26); growth matched by WebSearch snippet"],
 ["Adobe Q3 FY26 total ending ARR","$27.50B, +11.2% YoY; AI-first ARR >$650M (+150%)",Q326,ACC,NOTE_WS],
 ["Adobe Q2 FY26 revenue / C&MP / BP&C","$6.62B (+13%); C&MP $4.54B (+13% / +11% cc); BP&C $1.85B (+16% / +15% cc)",Q226,ACC,NOTE_WS],
 ["Adobe Q2 FY26 ending ARR incl. Semrush","$27.10B incl ~$480M Semrush; +12.5% vs $24.08B restated at FY26 rates","https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000112/adbe-20260529.htm",ACC,NOTE_WS+"; restated base from Q2 FY26 10-Q"],
 ["Semrush revenue in Adobe Q2 FY26","~$40M of customer-group subscription revenue (approx. 1 month)",Q226,ACC,NOTE_WS],
 ["FY26 C&MP guide includes Semrush","~$280M Semrush in C&MP guide $18.21-18.27B (June 2026 raise)",Q226,ACC,NOTE_WS],
 ["Adobe Q1 FY26 revenue / C&MP / BP&C","$6.40B (+12% / +11% cc); C&MP $4,389M (+12% / +11% cc); BP&C $1,782M (+15-16%)",Q126,ACC,NOTE_WS+"; BP&C growth quoted 15% and 16% in different snippets"],
 ["Adobe Q1 FY26 ending ARR","$26.06B, +10.9% YoY",Q126,ACC,NOTE_WS],
 ["Adobe Q4 FY25 revenue; FY25 revenue","$6.19B (+10%); FY25 $23.77B (+11%); Digital Media Q4 $4.62B, FY $17.65B (+11%); DM ARR $19.2B (+11.5%)",Q425,ACC,NOTE_WS],
 ["Adobe Q4 FY25 recast customer groups","C&MP $4.25B (+11% / +10% cc); BP&C $1.72B (+15%)",Q425,ACC,NOTE_WS],
 ["Adobe FY25 ending ARR revaluation","$25.20B revalued to $25.66B at FY26 rates (+$460M, mainly FX)",Q425,ACC,NOTE_WS],
 ["Adobe FY26 initial targets (Dec 2025)","Revenue $25.90-26.10B; BP&C $7.35-7.40B; C&MP $17.75-17.90B",Q425,ACC,NOTE_WS],
 ["Adobe FY25 Q1-Q3 recast customer groups","Q1 C&MP $3.92B (+10%) / BP&C $1.53B (+15%); Q2 $4.02B (+10%) / $1.60B (+15%); Q3 $4.12B (+11%) / $1.65B (+15%)",Q325,ACC,NOTE_WS+"; recast series summarised across FY25 8-K exhibits"],
 ["Adobe Q1 FY25","Revenue $5.71B (+10% / +11% cc); Digital Media $4,227M; DM ARR $17.63B (+12.6%)",Q125,ACC,NOTE_WS],
 ["Adobe Q2 FY25","Revenue $5.87B (+11%); Digital Media $4.35B (+12%); DM ARR $18.09B (+12.1%)",Q225,ACC,NOTE_WS],
 ["Adobe Q3 FY25","Revenue $5.99B (+11%); Digital Media $4,459M (+12% / +11% cc); DM ARR $18.59B (+11.7%)",Q325,ACC,NOTE_WS],
 ["Adobe FY24 quarterly revenue","Q1 $5.18B, Q2 $5.31B, Q3 $5.41B, Q4 $5.61B; FY24 $21.51B; DM $15.86B; Document Cloud $3.18B; DM ARR 15.76/16.25/16.76/17.33",Q424,ACC,NOTE_WS],
 ["Semrush Q4 2025 and FY2025 revenue","Q4 $117.7M (+15%); FY25 $443.6M (+18%); ARR $471.4M at 2025-12-31","https://www.sec.gov/Archives/edgar/data/1831840/000162828026013251/semrush8-kexhibit991q42025.htm",ACC,NOTE_WS+"; also businesswire 2026-03-02"],
 ["Semrush Q1 2026 revenue","UNAVAILABLE: no standalone Q1-26 results published (no call/guidance due to Adobe close); analyst consensus ~$121M","https://www.semrush.com/news/448771-semrush-announces-fourth-quarter-and-full-year-2025-financial-results/",ACC,"consensus figure from search snippet, not a company figure"],
 ["Semrush acquisition close","2026-04-28, ~$1.87B (orchestrator)",Q226,ACC,"orchestrator starting facts; consistent with Q2 FY26 release language"],
 ["CC price change Apr-2022","Teams All Apps $79.99->$84.99; teams single app $33.99->$35.99; individual month-to-month All Apps $79.49->$82.49; effective at renewal on/after 2022-04-27",BLOG22,ACC,NOTE_WS+"; cgchannel 2022-03"],
 ["CC price change Nov-2023","All Apps individual $54.99->$59.99 (annual billed monthly), $82.49->$89.99 m2m; single app $20.99->$22.99; teams All Apps $84.99->$89.99; teams single app $35.99->$37.99; NA/LatAm/Europe 2023-11-01, APAC/Africa 2024-03-05",BLOG23,ACC,NOTE_WS+"; helpx 2023 teams & individual pages; PetaPixel; dpreview"],
 ["Firefly Premium add-on Nov-2023","$4.99/mo for 100 generative credits",DPREV23,ACC,NOTE_WS],
 ["Photography plan change Jan-2025","20GB plan $9.99->$14.99 for existing monthly-billed (annual prepaid $119.88 unchanged); 20GB retired for new subscribers (1TB $19.99 only); Lightroom 1TB $9.99->$11.99 annual-billed-monthly; effective 2025-01-15",BLOG_PHOTO,ACC,NOTE_WS+"; PetaPixel 2024-12-18; lightroomqueen"],
 ["Firefly standalone plans Feb-2025","Standard $9.99, Pro $29.99 (launch/promotional, subject to change 2025-03-15); Premium $199.99 later",TC_FF,ACC,NOTE_WS+"; PetaPixel 2025-02-18"],
 ["Firefly lineup 2026","Standard $9.99 / Pro $19.99 / Pro Plus $49.99 / Premium $199.99; 30% off Pro Plus/Premium first year to 2026-08-26",FF_2026,ACC,"third-party price tracker; re-tier date UNAVAILABLE"],
 ["Firefly credit packs","100 extra credits $4.99; add-on packs of 2,000/4,000/7,000 credits exist",HELPX_CREDITS,ACC,NOTE_WS],
 ["CC Pro change Jun-2025 (individual)","All Apps renamed Creative Cloud Pro; $59.99->$69.99 annual billed monthly, NA, at renewal on/after 2025-06-17; new Standard tier $54.99; single-app unchanged",HELPX25_IND,ACC,NOTE_WS+"; PetaPixel 2025-05-20; Fast Company"],
 ["CC Pro change Jun-2025 (teams)","Teams All Apps -> Pro for teams $89.99->$99.99; single app teams unchanged $37.99",HELPX25_TEAMS,ACC,NOTE_WS+"; licenseware summary"],
 ["Acrobat Pro price increase 2022-2023","~40% per Adobe; $14.99->$19.99/mo observed; new customers from 2022-08-08, existing from 2023-07-01",SCHN_ACRO23,ACC,NOTE_WS+"; Adobe community thread"],
 ["Acrobat Studio launch","2025-08-19; $24.99 individual / $29.99 teams early-access; up to 15% upgrade discount to 2026-10-31",ACRO_STUDIO,ACC,NOTE_WS+"; news.adobe.com blocked here"],
 ["Acrobat Standard business increase Apr-2026","Effective 2026-04-01 for VIP Teams/Enterprise; percentage not disclosed",SCHN_ACRO26,ACC,NOTE_WS+"; licensemysoftware 2026-02-05"],
 ["VIP list price increase Jun-2026","Most CC & Acrobat SKUs on VIP Marketplace from 2026-06-01, esp. >=10-licence tiers; Express/Stock/AI Assistant/Sign excluded; Acrobat Pro teams $22.99->$23.99",SCHN_JUN26,ACC,NOTE_WS+"; Redress Compliance claims 5-22% by SKU (secondary)"],
 ["Claimed Jan-15-2026 consumer increase","Secondary blogs assert broad consumer/SMB increase 2026-01-15; no primary confirmation found",RAVODY,ACC,"LOW CONFIDENCE; not used in base model"],
 ["Current Acrobat individual list","Standard $14.99, Pro $19.99, Studio $24.99 (annual billed monthly); teams Standard $16.99, Pro $23.99",XODO,ACC,"third-party; earlier Standard individual $12.99 - change date UNAVAILABLE"],
 ["Adobe Express Premium price","$9.99/mo or $99.99/yr, unchanged 2023-2026",G2_EXPRESS,ACC,"third-party listing; no Adobe price-change notice found"],
 ["Adobe Q3 FY26 call: freemium MAU","Creative freemium MAU >100M, +70% YoY; Firefly ARR +40% QoQ","https://www.adobe.com/cc-shared/assets/investor-relations/pdfs/adbe-q3fy26-transcript.pdf",ACC,NOTE_WS+"; no seat/subscriber count disclosed"],
]
with open(os.path.join(WS,"sources.csv"),"w",newline="") as f:
    w = csv.writer(f); w.writerow(S_COLS); w.writerows(src)
print("wrote price_log.csv rows:", len(price_log), "| revenue rows:", len(rev), "| sources:", len(src))
