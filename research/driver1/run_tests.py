"""Driver 1 tests: price-adjusted bridge, net-new-ARR history vs price actions, migration table, churn-search timing.
All inputs come from existing research outputs; every assumption is printed and written to data/. ESTIMATE flags are explicit."""
import csv, json, os
import pandas as pd, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
R = os.path.dirname(os.path.abspath(__file__)); RES = os.path.dirname(R)
NAVY, TEAL, AMBER, RED, GREY = "#1F3A5F", "#2A9D8F", "#E9A23B", "#C0392B", "#7F8C8D"
plt.rcParams.update({"font.size": 5.5, "axes.titlesize": 6, "axes.labelsize": 5.5, "xtick.labelsize": 5, "ytick.labelsize": 5,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.5, "xtick.major.width": 0.4, "ytick.major.width": 0.4,
                     "legend.fontsize": 5, "figure.dpi": 300})
FIG = (3.1, 1.6)
def src(fig, text): fig.text(0.01, 0.005, text, fontsize=3.4, color=GREY, ha="left", va="bottom")

# ---------------------------------------------------------------- TEST 1: price-adjusted bridge
# Inputs (all from existing outputs)
nn = pd.read_csv(f"{RES}/tri/concessions/data/net_new_arr_fy25_vs_fy26.csv")  # Dec-2025-rate basis, organic
g = lambda q: float(nn.loc[nn.quarter == q, "organic_net_new_dec2025_rates_bn"].iloc[0])
H1_25, H2_25 = g("FY25Q1") + g("FY25Q2"), g("FY25Q3") + g("FY25Q4")
H1_26, H2_26 = g("FY26Q1") + g("FY26Q2"), g("FY26Q3") + g("FY26Q4E")
B = 4.25 * 4     # C&MP subscription revenue run-rate Q4 FY25 ($B) = base the WS1 'share repriced' scenarios apply to (ws1 revenue_quarterly)
scen = {"low": dict(s=0.10, u=0.111, m2m=0.0), "base": dict(s=0.20, u=0.15, m2m=0.2), "high": dict(s=0.30, u=0.167, m2m=0.3)}
# phase-in of the 17-Jun-2025 increase: m2m share immediate; annual share uniform over 12 months at renewal (WS1 methods)
months_to = {"FY25Q3": 2.4, "FY25Q4": 5.4, "FY26Q1": 8.4, "FY26Q2": 11.4, "FY26Q3": 12.0, "FY26Q4E": 12.0}
rows = []
for k, p in scen.items():
    P = B * p["s"] * p["u"]  # full-year ARR effect of the June-2025 wave ($B)
    cum = {q: p["m2m"] + (1 - p["m2m"]) * min(m / 12, 1) for q, m in months_to.items()}
    inc = {}; prev = 0
    for q in months_to: inc[q] = P * (cum[q] - prev); prev = cum[q]
    # 2026 actions (ws1 price_log: VIP/teams list increase 1-Jun-2026 ~+5%, Acrobat Standard business 1-Apr-2026): teams CC ARR ~$3.2B (c1 tiers) x 5% x phase-in to Nov-2026 (~45% + m2m)
    a2026 = {"low": 0.05, "base": 0.09, "high": 0.12}[k]
    price_H2_25 = inc["FY25Q3"] + inc["FY25Q4"]; price_H1_26 = inc["FY26Q1"] + inc["FY26Q2"]; price_H2_26 = inc["FY26Q3"] + inc["FY26Q4E"] + a2026
    rows.append(dict(scenario=k, share_repriced=p["s"], uplift=p["u"], m2m_share=p["m2m"], base_cmp_arr_bn=B, full_year_price_arr_bn=round(P, 3),
                     price_H2_FY25=round(price_H2_25, 3), price_H1_FY26=round(price_H1_26, 3), price_H2_FY26_incl_2026_actions=round(price_H2_26, 3),
                     H1_FY25_reported=round(H1_25, 2), H1_FY26_reported=round(H1_26, 2), H2_FY25_reported=round(H2_25, 2), H2_FY26_reported=round(H2_26, 2),
                     H1_FY25_exprice=round(H1_25, 2), H1_FY26_exprice=round(H1_26 - price_H1_26, 2),
                     H2_FY25_exprice=round(H2_25 - price_H2_25, 2), H2_FY26_exprice=round(H2_26 - price_H2_26, 2),
                     FY25_exprice=round(H1_25 + H2_25 - price_H2_25, 2), FY26_exprice=round(H1_26 + H2_26 - price_H1_26 - price_H2_26, 2)))
t1 = pd.DataFrame(rows)
t1["H2_change_reported_pct"] = round((H2_26 / H2_25 - 1) * 100, 1)
t1["H2_change_exprice_pct"] = ((t1.H2_FY26_exprice / t1.H2_FY25_exprice - 1) * 100).round(1)
t1["H1_change_reported_pct"] = round((H1_26 / H1_25 - 1) * 100, 1)
t1["H1_change_exprice_pct"] = ((t1.H1_FY26_exprice / t1.H1_FY25_exprice - 1) * 100).round(1)
t1["FY_change_reported_pct"] = round(((H1_26 + H2_26) / (H1_25 + H2_25) - 1) * 100, 1)
t1["FY_change_exprice_pct"] = ((t1.FY26_exprice / t1.FY25_exprice - 1) * 100).round(1)
t1.to_csv(f"{R}/data/test1_price_adjusted_bridge.csv", index=False)
print(t1.T)
# management-attributed FY26 cut (concessions/individual_subscriber_quotes): ~$0.48B organic (10.2% target held while Semrush added ~$0.48B); 'maybe half' deferred price actions
MGMT_CUT = 0.48; DEFERRED = 0.24; FREEMIUM = 0.24
b = t1.set_index("scenario").loc["base"]
gap_H2 = H2_25 - H2_26; price_timing = b.price_H2_FY25 - b.price_H2_FY26_incl_2026_actions
bridge = pd.DataFrame([("H2 FY25 organic net new ARR", H2_25), ("June-2025 price wave lapping (timing)", -price_timing),
                       ("Deferred CC price actions (mgmt, ~half of $0.48B)", -DEFERRED), ("Freemium routing (mgmt, other half)", -FREEMIUM),
                       ("Residual / overlap (unexplained)", H2_26 - (H2_25 - price_timing - DEFERRED - FREEMIUM)), ("H2 FY26 organic net new ARR (Q4 implied)", H2_26)],
                      columns=["step", "bn"])
bridge.to_csv(f"{R}/data/test1_bridge_steps.csv", index=False); print(bridge)

# chart 1: waterfall
fig, ax = plt.subplots(figsize=FIG); fig.subplots_adjust(left=0.11, right=0.99, top=0.84, bottom=0.30)
steps = bridge.bn.tolist(); labels = ["H2 FY25", "price-wave\nlapping", "deferred\npricing*", "freemium\nrouting*", "residual /\noverlap", "H2 FY26e"]
cum = 0; xs = range(len(steps))
for i, v in enumerate(steps):
    if i in (0, len(steps) - 1):
        ax.bar(i, v, color=NAVY, width=0.62); ax.text(i, v + 0.02, f"{v:.2f}", ha="center", va="bottom", fontsize=5); cum = v if i == 0 else cum
    else:
        bottom = cum + min(v, 0); ax.bar(i, abs(v), bottom=bottom, color=(RED if v < 0 else TEAL), width=0.62)
        ax.text(i, cum + max(v, 0) + 0.02, f"{v:+.2f}", ha="center", va="bottom", fontsize=5); cum += v
ax.set_xticks(list(xs)); ax.set_xticklabels(labels, fontsize=4.6); ax.set_ylabel("$B", fontsize=5); ax.set_ylim(0, 1.85)
ax.set_title("Net new ARR bridge, H2 FY25 to H2 FY26 (organic, $B; base case)", loc="left", fontsize=5.8)
src(fig, "Adobe IR data sheet 9/10/26 (Dec-25 rates); *Q2 FY26 call: ~$0.48B organic cut, 'maybe half' deferred pricing. Lapping = author ESTIMATE (20% repriced, 15% uplift).")
fig.savefig(f"{R}/charts/driver1_fig1_bridge.png"); plt.close(fig)

# ---------------------------------------------------------------- TEST 2: history vs price actions
hist = pd.DataFrame([
    ("FY23Q1", "2023-03", 410, "DM", "Q1 FY23 call"), ("FY23Q2", "2023-06", 470, "DM", "Q2 FY23 call"), ("FY23Q3", "2023-09", 464, "DM", "Q3 FY23 call"), ("FY23Q4", "2023-12", 569, "DM", "Q4 FY23 call"),
    ("FY24Q1", "2024-03", 432, "DM", "Q1 FY24 call"), ("FY24Q2", "2024-06", 487, "DM", "Q2 FY24 call"), ("FY24Q3", "2024-09", 504, "DM", "Q3 FY24 call"), ("FY24Q4", "2024-12", 578, "DM", "Q4 FY24 call"),
    ("FY25Q1", "2025-03", 410, "DM (derived from ending ARR)", "ws1 revenue_quarterly / concessions"), ("FY25Q2", "2025-06", 460, "DM (derived)", "same"), ("FY25Q3", "2025-09", 500, "DM (derived)", "same"), ("FY25Q4", "2025-12", 610, "DM (derived)", "same"),
    ("FY25Q1", "2025-03", 470, "Total Adobe (Dec-25 rates; Q1 est.)", "IR data sheet 9/10/26"), ("FY25Q2", "2025-06", 580, "Total Adobe", "same"), ("FY25Q3", "2025-09", 660, "Total Adobe", "same"), ("FY25Q4", "2025-12", 920, "Total Adobe", "same"),
    ("FY26Q1", "2026-03", 400, "Total Adobe", "same"), ("FY26Q2", "2026-06", 560, "Total Adobe (ex-Semrush $480M)", "same"), ("FY26Q3", "2026-09", 400, "Total Adobe", "same"), ("FY26Q4E", "2026-12", 780, "Total Adobe (implied by 10.2% target)", "Q3 FY26 8-K targets"),
], columns=["quarter", "call_month", "net_new_arr_musd", "basis", "source"])
# YoY on like basis
dm = hist[hist.basis.str.startswith("DM")].set_index("quarter").net_new_arr_musd
tot = hist[hist.basis.str.startswith("Total")].set_index("quarter").net_new_arr_musd
yoy = {}
for q in dm.index:
    fy, qq = q[:4], q[4:]; prior = f"FY{int(fy[2:]) - 1:02d}{qq}"
    if prior in dm.index: yoy[q] = round((dm[q] / dm[prior] - 1) * 100, 1)
for q in tot.index:
    fy, qq = q[:4], q[4:].replace("E", ""); prior = f"FY{int(fy[2:]) - 1:02d}{qq}"
    if prior in tot.index: yoy[q + " (total basis)"] = round((tot[q] / tot[prior] - 1) * 100, 1)
hist.to_csv(f"{R}/data/test2_net_new_arr_history.csv", index=False)
pd.Series(yoy, name="yoy_pct").to_csv(f"{R}/data/test2_yoy_like_basis.csv"); print(pd.Series(yoy))
actions = [("2022-04", "Teams +6% (NA)"), ("2022-08", "Acrobat Pro +33% (new)"), ("2023-07", "Acrobat Pro +33% (existing)"), ("2023-11", "CC All Apps +9%, teams +6%"),
           ("2025-01", "Photography +50% (new)"), ("2025-06", "CC Pro +16.7%, teams +11.1% (NA)"), ("2026-04", "Acrobat Std business (VIP)"), ("2026-06", "VIP list +5% (teams)")]
pd.DataFrame(actions, columns=["effective_month", "action"]).to_csv(f"{R}/data/test2_price_actions.csv", index=False)
# chart 2
fig, ax = plt.subplots(figsize=FIG); fig.subplots_adjust(left=0.10, right=0.99, top=0.84, bottom=0.26)
qs = ["FY23Q1","FY23Q2","FY23Q3","FY23Q4","FY24Q1","FY24Q2","FY24Q3","FY24Q4","FY25Q1","FY25Q2","FY25Q3","FY25Q4","FY26Q1","FY26Q2","FY26Q3","FY26Q4E"]
x = np.arange(len(qs)); w = 0.4
dmv = [dm.get(q, np.nan) for q in qs]; tv = [tot.get(q, np.nan) for q in qs]
ax.bar(x - w/2, dmv, width=w, color=NAVY, label="Digital Media net new ARR")
ax.bar(x + w/2, tv, width=w, color=TEAL, label="Total Adobe net new ARR (Dec-25 rates; Q4 FY26 implied)")
ax.bar([15 + w/2], [780], width=w, color="white", edgecolor=TEAL, linewidth=0.6, hatch="////")
for xm, lab in [(3.45, "Nov-23\nCC +9%"), (9.45, "Jun-25\nCC Pro +17%"), (13.45, "Jun-26\nVIP +5%")]:
    ax.axvline(xm, color=AMBER, lw=0.7, ls="--"); ax.text(xm + 0.12, 985, lab, fontsize=4.0, color=AMBER, va="top")
ax.set_xticks(x); ax.set_xticklabels([q.replace("FY", "").replace("Q", "Q") for q in qs], rotation=90, fontsize=4.2)
ax.set_ylabel("$M", fontsize=5); ax.set_ylim(0, 1000); ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.80), frameon=False, fontsize=4.0)
ax.set_title("Quarterly net new ARR vs Creative Cloud price actions (dashed)", loc="left", fontsize=5.8)
src(fig, "Adobe calls Q1 FY23-Q4 FY24 (Digital Media); FY25 from ending ARR; FY26 Total Adobe ARR, IR data sheet 9/10/26, ex-Semrush; actions per ws1 price log.")
fig.savefig(f"{R}/charts/driver1_fig2_nnarr_history.png"); plt.close(fig)

# ---------------------------------------------------------------- TEST 3: migration table
mig = pd.DataFrame([
    ("Figma", "revenue", "FY2025", 41.0, "Q2 2026", 48.3, "SEC 10-Q/8-K (ws5, tri/c1)", "Y"),
    ("Canva", "ARR (est.) / revenue", "CY2025 ARR +43% (est.)", 43.0, "Q2 2026 revenue; 2026 guide 20%", 25.2, "press-verified (tri/c3 canva_q2_2026_verification)", "Y (press)"),
    ("Adobe BP&C (Acrobat/Express)", "subscription revenue", "Q4 FY25", 15.0, "Q3 FY26", 15.6, "8-K Ex.99.1 (ws1 revenue_quarterly)", "Y"),
    ("Adobe C&MP (Creative + DX)", "subscription revenue", "Q4 FY25", 11.0, "Q3 FY26 (incl. ~2.9 pts Semrush)", 13.0, "8-K Ex.99.1 (ws1)", "Y"),
    ("Adobe C&MP organic cc (ex-Semrush, ex-FX)", "subscription revenue", "Q4 FY25", 10.0, "Q3 FY26", 9.1, "ws1 decomposition (Semrush ESTIMATE $120M)", "derived"),
    ("Upwork", "GSV", "Q1 2026 (AI-related GSV +40%)", np.nan, "Q2 2026 (AI-related GSV +22%)", -4.0, "SEC press release (tri/concessions)", "Y"),
    ("Fiverr", "revenue", "FY2025", np.nan, "Q2 2026; FY26 guide -14% to -17%", -10.0, "SEC 8-K Ex.99.1 (tri/concessions)", "Y"),
], columns=["entity", "metric", "prior_period", "prior_growth_pct", "latest_period", "latest_growth_pct", "source", "verified"])
mig.to_csv(f"{R}/data/test3_migration_table.csv", index=False)
pool = pd.DataFrame([("Adobe C&MP", 4651*4/1000, 2.136), ("Figma", 370.1*4/1000, 0.482), ("Canva", 921.9*4/1000, 0.742)], columns=["entity", "run_rate_bn", "annualized_increment_bn"])
pool["share_of_stock_pct"] = (pool.run_rate_bn / pool.run_rate_bn.sum() * 100).round(1); pool["share_of_increment_pct"] = (pool.annualized_increment_bn / pool.annualized_increment_bn.sum() * 100).round(1)
pool.to_csv(f"{R}/data/test3_share_of_pool.csv", index=False); print(mig[["entity", "latest_growth_pct"]]); print(pool)
# chart 3
fig, ax = plt.subplots(figsize=FIG); fig.subplots_adjust(left=0.36, right=0.97, top=0.84, bottom=0.22)
lab = ["Figma rev. Q2'26", "Canva rev. Q2'26\n(2026 guide 20%)", "Adobe BP&C Q3 FY26", "Adobe C&MP Q3 FY26", "Adobe C&MP organic cc", "Upwork GSV Q2'26", "Fiverr rev. Q2'26\n(FY26 guide -14 to -17%)"]
val = [48.3, 25.2, 15.6, 13.0, 9.1, -4.0, -10.0]; col = [TEAL, TEAL, NAVY, NAVY, NAVY, GREY, GREY]
y = np.arange(len(lab))[::-1]; ax.barh(y, val, color=col, height=0.62)
for yi, v in zip(y, val): ax.text(v + (0.8 if v >= 0 else -0.8), yi, f"{v:+.0f}%", va="center", ha="left" if v >= 0 else "right", fontsize=5)
ax.set_yticks(y); ax.set_yticklabels(lab, fontsize=4.6); ax.axvline(0, color="black", lw=0.5); ax.set_xlim(-18, 58)
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:.0f}%")); ax.set_title("Latest YoY growth: rivals vs Adobe vs freelance", loc="left", fontsize=5.8)
src(fig, "Figma 10-Q; Canva per press; Adobe 8-K Ex.99.1, ws1 decomposition; Upwork/Fiverr SEC releases. Teal = AI-native tools, navy = Adobe, grey = freelance.")
fig.savefig(f"{R}/charts/driver1_fig3_migration.png"); plt.close(fig)

# ---------------------------------------------------------------- TEST 4: churn-search timing
tr = pd.read_csv(f"{RES}/tri/c4_users/data/trends_raw_R4_US.csv"); tr["month"] = pd.to_datetime(tr["month"])
s = tr.set_index("month")["cancel adobe"].astype(float)
s = s[s.index <= pd.Timestamp("2026-09-01")]  # drop partial October 2026
roll = s.rolling(12, min_periods=6).mean().shift(1); z = (s - roll) / (s.rolling(12, min_periods=6).std().shift(1) + 1e-9)
events = [("2023-11-01", "CC +9% price (Nov-23)"), ("2024-06-17", "FTC/DOJ complaint"), ("2025-01-15", "Photography +50%"), ("2025-06-17", "CC Pro +17% price"),
          ("2026-03-13", "$150M DOJ settlement"), ("2026-03-19", "UK CMA probe"), ("2026-06-01", "VIP/list price rises")]
ev = pd.DataFrame(events, columns=["date", "event"]); ev["date"] = pd.to_datetime(ev.date)
top = s.sort_values(ascending=False).head(10)
out = []
for m, v in top.items():
    near = ev[(ev.date >= m - pd.offsets.MonthBegin(1)) & (ev.date < m + pd.offsets.MonthBegin(2))]
    out.append(dict(month=m.strftime("%Y-%m"), cancel_adobe_index=int(v), z_vs_trailing12=round(float(z.get(m, np.nan)), 1), yoy_pct=round(float(s[m] / s.get(m - pd.DateOffset(years=1), np.nan) - 1) * 100, 0) if (m - pd.DateOffset(years=1)) in s.index else np.nan,
                    events_within_pm1_month="; ".join(near.event.tolist()) or "none"))
t4 = pd.DataFrame(out); t4.to_csv(f"{R}/data/test4_cancel_adobe_spikes.csv", index=False); print(t4)
ann = s.groupby(s.index.year).mean().round(1); ann.to_csv(f"{R}/data/test4_cancel_adobe_annual_avg.csv"); print(ann)
# event-window test: mean index in event month and following month vs trailing-12 baseline
ew = []
for d, e in events:
    d = pd.Timestamp(d); m0 = pd.Timestamp(d.year, d.month, 1)
    base = s[(s.index < m0)].tail(12).mean(); win = s[(s.index >= m0) & (s.index < m0 + pd.offsets.MonthBegin(2))].mean()
    ew.append(dict(event=e, date=d.date(), trailing12_avg=round(base, 1), event_window_avg=round(win, 1), lift_pct=round((win / base - 1) * 100, 0)))
t4b = pd.DataFrame(ew); t4b.to_csv(f"{R}/data/test4_event_window_lift.csv", index=False); print(t4b)
# chart 4
fig, ax = plt.subplots(figsize=FIG); fig.subplots_adjust(left=0.09, right=0.98, top=0.84, bottom=0.20)
ax.plot(s.index, s.values, color=NAVY, lw=0.8)
for d, e, c, yy in [("2023-11-01", "Nov-23 price", AMBER, 100), ("2024-06-17", "DOJ/FTC suit", RED, 100), ("2025-06-17", "Jun-25 price", AMBER, 100), ("2026-03-13", "Settlement+CMA", RED, 62), ("2026-06-01", "Jun-26 prices", AMBER, 100)]:
    d = pd.Timestamp(d); ax.axvline(d, color=c, lw=0.6, ls="--"); ax.text(d - pd.Timedelta(days=12), yy, e, rotation=90, fontsize=3.8, color=c, ha="right", va="top")
ax.set_ylim(0, 105); ax.set_ylabel("Index (max = 100)", fontsize=5); ax.set_title("Google Trends 'cancel adobe', US monthly, with dated events", loc="left", fontsize=5.8)
ax.tick_params(axis="x", labelsize=4.5)
src(fig, "Google Trends via pytrends (c4 R4, pulled 10/2/26; Oct partial dropped); FTC 6/17/24; settlement 3/13/26; CMA 3/19/26; price dates per ws1.")
fig.savefig(f"{R}/charts/driver1_fig4_cancel_adobe.png"); plt.close(fig)
print("done")
