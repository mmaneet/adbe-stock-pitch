#!/usr/bin/env python
"""Task 5: descriptive ratio of AI-first ARR added per incremental creative-freemium MAU, and the EPS bridge.
Writes data/mau_to_arr_ratio.csv and charts/mau_vs_ai_first_arr.png. Inputs are the company's disclosed
LOWER BOUNDS ("more than X") from mau_quarterly.csv; see methods.md. DESCRIPTIVE RATIO, NOT CAUSAL:
AI-first ARR also contains Acrobat AI Assistant, Firefly Services/Foundry and GenStudio (enterprise), none of which
is sold to creative-freemium users, so the ratio is a bookkeeping relationship, not an attribution."""
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); WS = os.path.dirname(HERE); CHARTS = os.path.join(WS, "charts")
NAVY, TEAL, AMBER, RED, GREY = "#1F3A5F", "#2A9D8F", "#E9A23B", "#C0392B", "#7F8C8D"

# quarter, call date, creative freemium MAU (M, lower bound unless noted), AI-first ARR ($M, lower bound unless noted), basis
pts = [
    ("FY25Q1", "2025-03-12", 53,  125, "MAU IMPLIED = 80/1.5 (Q1 FY26 '80M, +50% YoY'); ARR disclosed >$125M (Q1 FY25 PR)"),
    ("FY25Q2", "2025-06-12", 50,  None, "MAU disclosed retrospectively ('from 50 million to 90 million YoY', Q2 FY26 call); ARR level not disclosed"),
    ("FY25Q3", "2025-09-11", 59,  250, "MAU IMPLIED = 100/1.7 (Q3 FY26 '100M, +70% YoY'); ARR disclosed >$250M (Q3 FY25 PR)"),
    ("FY25Q4", "2025-12-10", 70,  None, "MAU disclosed >70M; ARR level not disclosed in Q4 FY25 PR/transcript"),
    ("FY26Q1", "2026-03-12", 80,  375, "MAU disclosed >80M; ARR IMPLIED = 3 x >125 ('more than tripled YoY', Q1 FY26 PR)"),
    ("FY26Q2", "2026-06-11", 90,  500, "MAU disclosed >90M; ARR disclosed >$500M (Q2 FY26 PR)"),
    ("FY26Q3", "2026-09-10", 100, 650, "MAU disclosed >100M; ARR disclosed >$650M (Q3 FY26 call)"),
]
df = pd.DataFrame(pts, columns=["quarter", "call_date", "creative_freemium_mau_m", "ai_first_arr_musd", "basis"])

# descriptive ratios by period (only where both endpoints have an ARR value)
periods = [("FY25Q3", "FY26Q3", "YoY; both ARR ends disclosed; Q3 FY25 MAU implied from Q3 FY26 +70% YoY"),
           ("FY25Q1", "FY26Q1", "YoY; Q1 FY25 MAU implied, Q1 FY26 ARR implied"),
           ("FY26Q1", "FY26Q2", "QoQ"), ("FY26Q2", "FY26Q3", "QoQ")]
rows = []
d = df.set_index("quarter")
for a, b, note in periods:
    dm = d.loc[b, "creative_freemium_mau_m"] - d.loc[a, "creative_freemium_mau_m"]
    da = d.loc[b, "ai_first_arr_musd"] - d.loc[a, "ai_first_arr_musd"]
    rows.append((f"{a}->{b}", d.loc[a, "creative_freemium_mau_m"], d.loc[b, "creative_freemium_mau_m"], dm,
                 d.loc[a, "ai_first_arr_musd"], d.loc[b, "ai_first_arr_musd"], da, round(da / dm, 2), note))
# headline version exactly as specified in the brief: (650-250)/(100-50)
rows.append(("FY25(Q2 MAU base, Q3 ARR base)->FY26Q3 [headline]", 50, 100, 50, 250, 650, 400, 8.0,
             "brief's headline ratio: (650-250)/(100-50) = $8.0 of AI-first ARR per incremental freemium MAU"))
ratio = pd.DataFrame(rows, columns=["period", "mau_start_m", "mau_end_m", "delta_mau_m", "arr_start_musd", "arr_end_musd",
                                    "delta_arr_musd", "arr_per_incremental_mau_usd", "note"])
ratio.insert(0, "label", "DESCRIPTIVE RATIO, NOT CAUSAL")

# EPS bridge: $100M ARR x 45% incremental op margin x (1-18% tax) / 390M diluted shares = $0.0946 ~ $0.095
EPS_PER_100M = 100 * 0.45 * (1 - 0.18) / 390
scen = []
for target_mau in (120, 150, 200, 250):
    for r in (8.0, 5.0):
        add_arr = (target_mau - 100) * r
        scen.append((target_mau, r, add_arr, 650 + add_arr, round(add_arr / 100 * EPS_PER_100M, 3)))
scen = pd.DataFrame(scen, columns=["freemium_mau_target_m", "assumed_arr_per_mau_usd", "incremental_ai_first_arr_musd",
                                   "implied_ai_first_arr_musd", "incremental_eps_usd"])
scen.insert(0, "label", "SCENARIO (if ratio holds; not a forecast)")
with open(os.path.join(HERE, "mau_to_arr_ratio.csv"), "w") as fh:
    fh.write("# Section 1: inputs (company lower bounds / implied values; see basis)\n"); df.to_csv(fh, index=False)
    fh.write("\n# Section 2: descriptive ratio by period (NOT causal)\n"); ratio.to_csv(fh, index=False)
    fh.write(f"\n# Section 3: EPS bridge. $100M ARR x 45% incr. op margin x (1-18% non-GAAP tax) / 390M diluted shares = ${EPS_PER_100M:.4f} EPS per $100M ARR\n")
    scen.to_csv(fh, index=False)
print(ratio.to_string()); print(scen.to_string()); print("EPS per $100M ARR:", round(EPS_PER_100M, 4))

# chart: two small panels on one figure (no dual axis)
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2)); fig.patch.set_facecolor("white")
x = range(len(df)); labels = df["quarter"].tolist()
ax = axes[0]
ax.bar(x, df["creative_freemium_mau_m"], color=[NAVY if "disclosed" in b.split(";")[0] else GREY for b in df["basis"]], width=0.62)
for i, (v, b) in enumerate(zip(df["creative_freemium_mau_m"], df["basis"])):
    ax.text(i, v + 1.5, f"{'>' if 'disclosed' in b.split(';')[0] else '~'}{v:.0f}M", ha="center", fontsize=8.5, color="#333")
ax.set_title("Creative freemium MAU (millions)", loc="left", fontsize=11); ax.set_xticks(list(x)); ax.set_xticklabels(labels, fontsize=8, rotation=0)
ax.set_ylim(0, 118); ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="y", color="#EEEEEE"); ax.set_axisbelow(True)
ax2 = axes[1]
m = df["ai_first_arr_musd"].notna()
ax2.bar([i for i in x if m[i]], df.loc[m, "ai_first_arr_musd"],
        color=[TEAL if "disclosed" in b.split(";")[-1] or "ARR disclosed" in b else GREY for b in df.loc[m, "basis"]], width=0.62)
for i in x:
    if m[i]:
        b = df.loc[i, "basis"]; disc = ("ARR disclosed" in b) or ("ARR level" not in b and "IMPLIED" not in b.split(";")[-1])
        ax2.text(i, df.loc[i, "ai_first_arr_musd"] + 10, f"{'>' if 'ARR disclosed' in b else '~'}${df.loc[i, 'ai_first_arr_musd']:.0f}M", ha="center", fontsize=8.5, color="#333")
    else:
        ax2.text(i, 12, "n/d", ha="center", fontsize=8, color=GREY)
ax2.set_title("AI-first ending ARR ($M)", loc="left", fontsize=11); ax2.set_xticks(list(x)); ax2.set_xticklabels(labels, fontsize=8)
ax2.set_ylim(0, 760); ax2.spines[["top", "right"]].set_visible(False); ax2.grid(axis="y", color="#EEEEEE"); ax2.set_axisbelow(True)
fig.suptitle("Adobe: creative freemium MAU vs AI-first ARR, FY25Q1-FY26Q3 (company lower bounds; grey = implied)", x=0.01, ha="left", fontsize=12)
fig.text(0.01, 0.015, "Source: Adobe earnings-call transcripts and 8-K press releases (adobe.com IR, sec.gov), FY25Q1-FY26Q3. 'More than X' shown at X (lower bound). "
         "Grey bars are implied from disclosed growth rates. n/d = level not disclosed. Ratio of the two is descriptive, not causal.", fontsize=7, color=GREY, wrap=True)
fig.tight_layout(rect=(0, 0.06, 1, 0.93)); os.makedirs(CHARTS, exist_ok=True)
fig.savefig(os.path.join(CHARTS, "mau_vs_ai_first_arr.png"), dpi=150); print("wrote chart")
