"""WS1 price-contribution model.
Price index per customer group = product over price events of (1 + list_uplift * scenario_share * rel_exposure * phase_in(t)).
YoY price contribution in quarter q = P(q)/P(q-4) - 1. Implied volume/mix = (1+organic_cc_growth)/(1+price) - 1.
Outputs: price_model.csv (per event x scenario x quarter, additive approx.), decomposition.csv, two PNG charts."""
import csv, os, math
from datetime import date
import pandas as pd, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = os.path.dirname(os.path.abspath(__file__)); WS = os.path.dirname(D); CH = os.path.join(WS, "charts")
SCEN = {"low_10pct": 0.10, "base_20pct": 0.20, "high_30pct": 0.30}

# ---------------------------------------------------------------- price events (see price_log.csv for sources)
# uplift = blended list uplift of the wave (decimal); rel_exposure scales the scenario share for narrower waves
# (1.0 = the wave touches the whole scenario share of group revenue). phase = 'annual' (uniform monthly renewals over
# 12 months), 'new24' (new-customer-only: flows in as base turns over, 24 months), 'm2m' (100% at effective date).
EVENTS = [
 # group, id, effective (y,m), uplift, rel_exposure, phase, verified, note
 ("CMP","2022-04 teams/enterprise (+6%)",(2022,4),0.060,0.40,"annual",True,"Teams All Apps +6.3%, teams single app +5.9%; NA; enterprise amounts n/a"),
 ("CMP","2023-11 Firefly wave (~+8% blend)",(2023,11),0.078,1.00,"annual",True,"Indiv All Apps +9.1%, single app +9.5%, teams +5.6-5.9%; 60/40 indiv/teams blend; Americas+Europe"),
 ("CMP","2024-03 Nov-23 wave APAC/Africa",(2024,3),0.078,0.30,"annual",True,"Same structure, smaller regional base"),
 ("CMP","2025-01 Photography 20GB (+50% / retired)",(2025,1),0.50,0.08,"annual",True,"Small revenue base; many existing avoided via prepaid annual; new-subscriber entry 2x"),
 ("CMP","2025-06 CC Pro NA (~+14.5% blend)",(2025,6),0.145,1.00,"annual",True,"Indiv All Apps +16.7%, teams All Apps +11.1%; single app 0%; Standard downgrade -8.3% available; NA only"),
 ("CMP","2026-06 VIP list increase (+5% assumed)",(2026,6),0.050,0.30,"annual",True,"Schneider: most CC/Acrobat VIP SKUs; 5-22% claimed by secondary source; low end used; ETLAs protected"),
 ("BPC","2022-08 Acrobat Pro new customers (+33%)",(2022,8),0.334,0.50,"new24",True,"$14.99->$19.99 for new customers; flows in with base turnover"),
 ("BPC","2023-07 Acrobat Pro existing (+33%)",(2023,7),0.334,1.00,"annual",True,"Existing subscribers repriced at renewal from 2023-07-01"),
 ("BPC","2026-06 VIP Acrobat Pro teams (+4.3%)",(2026,6),0.043,0.30,"annual",True,"$22.99->$23.99 (Redress); VIP only"),
 ("BPC","2026-01 Acrobat Standard indiv $12.99->$14.99 (+15%) UNVERIFIED DATE",(2026,1),0.154,0.25,"annual",False,"Price level verified, date not; secondary blogs claim 2026-01-15 consumer increase"),
 ("BPC","2026-04 Acrobat Standard business (+10% ASSUMED)",(2026,4),0.10,0.30,"annual",False,"Effective date verified (Schneider), magnitude not disclosed"),
]

# fiscal quarters -> calendar months (Adobe FY ends ~Nov 28). FY25Q1 = Dec-2024..Feb-2025
def q_months(fy, q):
    start = {1:(fy-1,12), 2:(fy,3), 3:(fy,6), 4:(fy,9)}[q]
    y, m = start; out=[]
    for i in range(3):
        mm = m+i; yy = y
        if mm > 12: mm -= 12; yy += 1
        out.append((yy, mm))
    return out
QUARTERS = [(24,1),(24,2),(24,3),(24,4),(25,1),(25,2),(25,3),(25,4),(26,1),(26,2),(26,3)]
QLABEL = lambda fy,q: f"FY{fy}Q{q}"

def midx(y, m): return y*12 + (m-1)
def phase(ev, y, m, m2m_override=False):
    _,_,(ey,em),_,_,ph,_,_ = ev
    k = midx(y,m) - midx(ey,em) + 1          # months since effective, effective month = 1
    if k <= 0: return 0.0
    if m2m_override or ph == "m2m": return 1.0
    if ph == "new24": return min(1.0, k/24)
    return min(1.0, k/12)

def price_index(group, share, y, m, include_unverified=False, m2m=False):
    p = 1.0
    for ev in EVENTS:
        if ev[0] != group: continue
        if not include_unverified and not ev[6]: continue
        p *= 1 + ev[3]*share*ev[4]*phase(ev, y, m, m2m)
    return p

def q_index(group, share, fy, q, **kw):
    return float(np.mean([price_index(group, share, y, m, **kw) for (y,m) in q_months(2000+fy, q)]))

def price_contrib(group, share, fy, q, **kw):
    cur = q_index(group, share, fy, q, **kw); prev = q_index(group, share, fy-1, q, **kw)
    return cur/prev - 1

# ---------------------------------------------------------------- revenue inputs (from revenue_quarterly.csv)
rev = pd.read_csv(os.path.join(D,"revenue_quarterly.csv"))
rev = rev.set_index("fiscal_quarter")
def val(qlab, col):
    v = rev.loc[qlab, col]; return float(v) if pd.notna(v) and str(v)!="" else np.nan
# FX adjustment (reported minus constant currency, growth points; + = FX tailwind) from press-release integer rates
FX = {  # (CMP, BPC)
 "FY25Q1":(-1.0,-1.0,"total co. 10% rep / 11% cc; segment cc not disclosed -> company gap applied"),
 "FY25Q2":(0.0,0.0,"segment cc not found; DX sub 11% rep = cc -> 0 assumed"),
 "FY25Q3":(1.0,1.0,"Digital Media 12% rep / 11% cc applied to both groups"),
 "FY25Q4":(1.0,1.0,"C&MP 11% rep / 10% cc; BP&C cc not disclosed -> same gap"),
 "FY26Q1":(1.0,1.0,"C&MP 12% rep / 11% cc; BP&C cc not disclosed -> same gap"),
 "FY26Q2":(2.0,1.0,"C&MP 13% rep / 11% cc; BP&C 16% / 15%"),
 "FY26Q3":(1.0,1.0,"C&MP 13% rep / 12% cc; BP&C 16% / 15%"),
}
SEMRUSH = {"FY26Q2":40.0, "FY26Q3":120.0}   # $M, C&MP only; Q3 is an estimate (see revenue_quarterly notes)

# ---------------------------------------------------------------- price_model.csv (per event x scenario, additive approx.)
pm_rows=[]
for sname, s in SCEN.items():
    for ev in EVENTS:
        g,eid,(ey,em),u,r,ph,ver,note = ev
        row = {"scenario":sname,"scenario_share":s,"group":g,"event":eid,"effective":f"{ey}-{em:02d}","list_uplift_pct":round(u*100,1),
               "rel_exposure":r,"effective_share_of_group_rev_pct":round(s*r*100,1),"phase_in":ph,"verified":ver,"note":note}
        for (fy,q) in QUARTERS[4:]:
            cur = np.mean([phase(ev,y,m) for (y,m) in q_months(2000+fy,q)])
            prev = np.mean([phase(ev,y,m) for (y,m) in q_months(2000+fy-1,q)])
            row[f"contrib_pts_{QLABEL(fy,q)}"] = round(u*s*r*(cur-prev)*100, 2)
        pm_rows.append(row)
pd.DataFrame(pm_rows).to_csv(os.path.join(D,"price_model.csv"), index=False)

# ---------------------------------------------------------------- decomposition.csv
dec=[]
for (fy,q) in QUARTERS[4:]:
    ql = QLABEL(fy,q); pl = QLABEL(fy-1,q)
    for g, col in (("CMP","cmp_sub_rev_m"),("BPC","bpc_sub_rev_m")):
        cur, prev = val(ql,col), val(pl,col)
        rep = (cur/prev-1)*100
        fx = FX[ql][0 if g=="CMP" else 1]; fxnote = FX[ql][2]
        cc = rep - fx
        sem_m = SEMRUSH.get(ql,0.0) if g=="CMP" else 0.0
        sem_pts = sem_m/prev*100
        org = cc - sem_pts
        for sname, s in SCEN.items():
            pc = price_contrib(g,s,fy,q)*100
            vol = ((1+org/100)/(1+pc/100)-1)*100
            pc_m2m = price_contrib(g,s,fy,q,m2m=True)*100
            vol_m2m = ((1+org/100)/(1+pc_m2m/100)-1)*100
            pc_unv = price_contrib(g,s,fy,q,include_unverified=True)*100
            vol_unv = ((1+org/100)/(1+pc_unv/100)-1)*100
            dec.append({"fiscal_quarter":ql,"group":{"CMP":"Creative & Marketing Professionals","BPC":"Business Professionals & Consumers"}[g],
                        "scenario":sname,"scenario_share_repriced":s,
                        "sub_rev_m":cur,"prior_year_sub_rev_m":prev,"reported_growth_pct":round(rep,2),
                        "fx_adj_pts":fx,"cc_growth_pct":round(cc,2),"semrush_rev_m":sem_m,"semrush_pts":round(sem_pts,2),
                        "organic_cc_growth_pct":round(org,2),"price_contrib_pts":round(pc,2),"implied_volume_mix_growth_pct":round(vol,2),
                        "price_contrib_m2m_sensitivity_pts":round(pc_m2m,2),"implied_volume_mix_m2m_pct":round(vol_m2m,2),
                        "price_contrib_incl_unverified_pts":round(pc_unv,2),"implied_volume_incl_unverified_pct":round(vol_unv,2),
                        "fx_note":fxnote,
                        "notes":("Semrush Q3 contribution is an ESTIMATE (~$120M)" if (ql=="FY26Q3" and g=="CMP") else "")+
                                ("; Q2 C&MP/BP&C back-solved from 9M totals" if ql=="FY26Q2" else "")})
dec = pd.DataFrame(dec); dec.to_csv(os.path.join(D,"decomposition.csv"), index=False)

# ---------------------------------------------------------------- charts
NAVY, TEAL, AMBER, RED, GREY = "#1F3A5F","#2A9D8F","#E9A23B","#C0392B","#7F8C8D"
def style(ax):
    for s in ("top","right"): ax.spines[s].set_visible(False)
    ax.set_facecolor("white"); ax.grid(axis="y", color="#E5E5E5", lw=0.6); ax.set_axisbelow(True)

def make_chart(group_label, short, fname, title):
    d = dec[dec.group==group_label]
    qs = list(dict.fromkeys(d.fiscal_quarter)); x = np.arange(len(qs))
    fig, axes = plt.subplots(1,2, figsize=(13,5.2), facecolor="white")
    # left: base stacked bars
    ax = axes[0]; b = d[d.scenario=="base_20pct"].set_index("fiscal_quarter").loc[qs]
    ax.bar(x, b.implied_volume_mix_growth_pct, color=NAVY, width=0.62, label="Implied volume / mix growth")
    ax.bar(x, b.price_contrib_pts, bottom=b.implied_volume_mix_growth_pct, color=AMBER, width=0.62, label="Price contribution (base: 20% of revenue repriced)")
    ax.plot(x, b.organic_cc_growth_pct, color=TEAL, lw=2, marker="o", ms=5, label="Organic constant-currency growth (ex-Semrush)")
    ax.plot(x, b.reported_growth_pct, color=GREY, lw=1.2, ls="--", marker="s", ms=4, label="Reported growth")
    for i,(v,p) in enumerate(zip(b.implied_volume_mix_growth_pct, b.price_contrib_pts)):
        ax.text(i, v/2, f"{v:.1f}", ha="center", va="center", color="white", fontsize=8)
        if p>0.35: ax.text(i, v+p/2, f"{p:.1f}", ha="center", va="center", color="black", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(qs, fontsize=9); ax.set_ylabel("YoY growth, % / percentage points")
    ax.set_title(f"{short}: base scenario", loc="left", fontsize=11); style(ax); ax.axhline(0,color="black",lw=0.8)
    ax.set_ylim(0, max(b.reported_growth_pct.max(), b.organic_cc_growth_pct.max())*1.42)
    ax.legend(fontsize=8, frameon=False, loc="upper left", ncol=2)
    # right: implied volume under scenarios
    ax = axes[1]
    for sname, col, lab in (("low_10pct",TEAL,"10% repriced"),("base_20pct",NAVY,"20% repriced (base)"),("high_30pct",RED,"30% repriced")):
        s = d[d.scenario==sname].set_index("fiscal_quarter").loc[qs]
        ax.plot(x, s.implied_volume_mix_growth_pct, color=col, lw=2, marker="o", ms=4, label=f"Implied volume/mix, {lab}")
    s = d[d.scenario=="high_30pct"].set_index("fiscal_quarter").loc[qs]
    ax.plot(x, s.implied_volume_mix_m2m_pct, color=RED, lw=1.2, ls=":", label="30%, 100% repriced at effective date (m2m)")
    ax.plot(x, s.organic_cc_growth_pct, color=GREY, lw=1.2, ls="--", label="Organic cc growth (ceiling)")
    ax.set_xticks(x); ax.set_xticklabels(qs, fontsize=9); ax.set_ylabel("Implied volume / mix growth, % YoY")
    ax.set_title(f"{short}: sensitivity to share repriced", loc="left", fontsize=11); style(ax); ax.axhline(0,color="black",lw=0.8)
    ax.set_ylim(-5.5, d.organic_cc_growth_pct.max()*1.15)
    ax.text(len(qs)-0.5, 0.25, "zero volume growth", ha="right", va="bottom", fontsize=7.5, color=GREY)
    ax.legend(fontsize=8, frameon=False, loc="lower left")
    fig.suptitle(title, x=0.01, ha="left", fontsize=13)
    fig.text(0.01, 0.01, "Source: Adobe 8-K Ex.99.1 / 10-Q (FY25-FY26, recast customer groups), Adobe blog/helpx price notices, Semrush 8-K; WS1 model. "
                         "FY26 Q3 Semrush contribution estimated (~$120M). Price = list uplift x share repriced x renewal phase-in.", fontsize=7.5, color=GREY)
    fig.tight_layout(rect=(0,0.04,1,0.95)); fig.savefig(os.path.join(CH,fname), dpi=150, facecolor="white"); plt.close(fig)

make_chart("Creative & Marketing Professionals","C&MP subscription revenue","price_vs_volume_stacked.png",
           "Creative & Marketing Professionals: how much of growth is price vs volume/mix?")
make_chart("Business Professionals & Consumers","BP&C subscription revenue","bpc_price_vs_volume_stacked.png",
           "Business Professionals & Consumers: price vs volume/mix")

# ---------------------------------------------------------------- console summary
pd.set_option("display.width",250); pd.set_option("display.max_columns",30)
cols=["fiscal_quarter","scenario","reported_growth_pct","fx_adj_pts","semrush_pts","organic_cc_growth_pct","price_contrib_pts","implied_volume_mix_growth_pct","price_contrib_m2m_sensitivity_pts","implied_volume_mix_m2m_pct","implied_volume_incl_unverified_pct"]
for g in dec.group.unique():
    print("\n==", g); print(dec[dec.group==g][cols].to_string(index=False))
