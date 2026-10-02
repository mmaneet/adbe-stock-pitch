#!/usr/bin/env python
"""Build charts/competitor_growth_vs_adobe.png and charts/incremental_revenue_dollars.png
from data/growth_comparison.csv, and print the share-of-incremental arithmetic used in findings.md."""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
CHARTS = os.path.join(WS, "charts")
os.makedirs(CHARTS, exist_ok=True)

NAVY, TEAL, AMBER, RED, GREY = "#1F3A5F", "#2A9D8F", "#E9A23B", "#C0392B", "#7F8C8D"

df = pd.read_csv(os.path.join(HERE, "growth_comparison.csv"))


def get(entity, metric, period, col="yoy_growth_pct"):
    row = df[(df.entity == entity) & (df.metric == metric) & (df.period == period)]
    assert len(row) == 1, (entity, metric, period, len(row))
    return float(row[col].iloc[0])


def style(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#EEEEEE")
    ax.set_axisbelow(True)


# ---------------------------------------------------------------- chart 1: YoY growth, grouped
groups = [
    # label, late-2025 value, latest value, late-2025 label, latest label, color
    ("Figma\nrevenue", get("Figma", "revenue", "Q4 2025"), get("Figma", "revenue", "Q2 2026"), "Q4'25", "Q2'26", TEAL),
    ("Canva\nARR / revenue", get("Canva", "ARR", "CY2025"), get("Canva", "revenue", "Q2 2026"), "CY25 ARR*", "Q2'26 rev", AMBER),
    ("Adobe\nC&MP subs", get("Adobe", "C&MP subscription revenue", "Q4 FY2025"), get("Adobe", "C&MP subscription revenue", "Q3 FY2026"), "Q4 FY25", "Q3 FY26", NAVY),
    ("Adobe\nBP&C subs", get("Adobe", "BP&C subscription revenue", "Q4 FY2025"), get("Adobe", "BP&C subscription revenue", "Q3 FY2026"), "Q4 FY25", "Q3 FY26", NAVY),
    ("Adobe\ntotal revenue", 10.0, get("Adobe", "total revenue", "Q3 FY2026"), "Q4 FY25", "Q3 FY26", NAVY),
]
fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor("white")
w = 0.36
for i, (lab, v_old, v_new, l_old, l_new, col) in enumerate(groups):
    ax.bar(i - w / 2, v_old, w, color=col, alpha=0.45, edgecolor="none")
    ax.bar(i + w / 2, v_new, w, color=col, edgecolor="none")
    ax.text(i - w / 2, v_old + 0.8, f"{v_old:.0f}%\n{l_old}", ha="center", va="bottom", fontsize=8, color="#333333")
    ax.text(i + w / 2, v_new + 0.8, f"{v_new:.0f}%\n{l_new}", ha="center", va="bottom", fontsize=8, color="#333333")
ax.set_xticks(range(len(groups)))
ax.set_xticklabels([g[0] for g in groups], fontsize=9)
ax.set_ylabel("Year-over-year growth (%)")
ax.set_ylim(0, 58)
ax.set_title("Competitors still grow 2-4x faster than Adobe, but Canva has slowed sharply", loc="left", fontsize=12)
ax.text(0.99, 0.97, "Light bars: late-2025 period   Dark bars: latest reported quarter",
        transform=ax.transAxes, ha="right", va="top", fontsize=8, color=GREY)
style(ax)
fig.text(0.01, 0.01,
         "Source: Figma 8-Ks (Feb/Aug 2026); Canva end-2025 ARR per company via Inc. (YoY per Sacra, *estimate), Q2-2026 revenue\n"
         "as reported Aug 2026 (The Information); Adobe 8-K Q4 FY25 and 10-Q Q3 FY26. Adobe BP&C includes Acrobat and Express.",
         fontsize=7.5, color=GREY)
fig.tight_layout(rect=(0, 0.07, 1, 1))
out1 = os.path.join(CHARTS, "competitor_growth_vs_adobe.png")
fig.savefig(out1, dpi=150)
plt.close(fig)
print("wrote", out1)

# ---------------------------------------------------------------- chart 2: incremental dollars
bars = [
    ("Adobe C&MP subs, Q3 FY26 YoY x4", get("Adobe", "C&MP subscription revenue", "Q3 FY2026", "annualized_incremental_musd"), NAVY, False),
    ("Adobe Digital Media, FY25 actual", get("Adobe", "Digital Media revenue", "FY2025", "annualized_incremental_musd"), NAVY, False),
    ("Canva ARR added, CY25 (est.)", get("Canva", "ARR", "CY2025", "annualized_incremental_musd"), AMBER, True),
    ("Adobe BP&C subs, Q3 FY26 YoY x4", get("Adobe", "BP&C subscription revenue", "Q3 FY2026", "annualized_incremental_musd"), NAVY, False),
    ("Canva revenue, Q2'26 YoY x4", get("Canva", "revenue", "Q2 2026", "annualized_incremental_musd"), AMBER, False),
    ("Figma revenue, Q2'26 YoY x4", get("Figma", "revenue", "Q2 2026", "annualized_incremental_musd"), TEAL, False),
    ("Figma revenue, FY25 actual", get("Figma", "revenue", "FY2025", "annualized_incremental_musd"), TEAL, False),
    ("Midjourney revenue, CY25 (est.)", get("Midjourney", "revenue", "CY2025", "annualized_incremental_musd"), RED, True),
]
bars = sorted(bars, key=lambda b: b[1])
fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor("white")
for i, (lab, v, col, est) in enumerate(bars):
    ax.barh(i, v / 1000, color=col, edgecolor="white" if est else "none", hatch="//" if est else None)
    ax.text(v / 1000 + 0.03, i, f"${v/1000:.2f}B", va="center", fontsize=9, color="#333333")
ax.set_yticks(range(len(bars)))
ax.set_yticklabels([b[0] for b in bars], fontsize=9)
ax.set_xlabel("Incremental annual revenue / ARR added year-over-year (USD billions)")
ax.set_xlim(0, 2.6)
ax.set_title("Adobe adds more creative dollars per year than Figma and Canva combined", loc="left", fontsize=12)
ax.text(0.99, 0.03, "Hatched = third-party estimate (private company)", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=8, color=GREY)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="x", color="#EEEEEE")
ax.set_axisbelow(True)
fig.text(0.01, 0.01,
         "Source: Adobe 10-Q Q3 FY26 and 8-K Q4 FY25; Figma 8-Ks; Canva per company (Inc., Feb 2026) and Sacra; Midjourney per\n"
         "Sacra/GetLatka. 'YoY x4' = latest-quarter year-over-year dollar increase multiplied by four.",
         fontsize=7.5, color=GREY)
fig.tight_layout(rect=(0, 0.07, 1, 1))
out2 = os.path.join(CHARTS, "incremental_revenue_dollars.png")
fig.savefig(out2, dpi=150)
plt.close(fig)
print("wrote", out2)

# ---------------------------------------------------------------- share-of-incremental arithmetic
adobe_inc = get("Adobe", "C&MP subscription revenue", "Q3 FY2026", "annualized_incremental_musd")
figma_inc = get("Figma", "revenue", "Q2 2026", "annualized_incremental_musd")
canva_inc = get("Canva", "revenue", "Q2 2026", "annualized_incremental_musd")
adobe_rr = get("Adobe", "C&MP subscription revenue", "Q3 FY2026", "value_musd") * 4
figma_rr = get("Figma", "revenue", "Q2 2026", "value_musd") * 4
canva_rr = get("Canva", "revenue", "Q2 2026", "value_musd") * 4
pool_rr = adobe_rr + figma_rr + canva_rr
pool_inc = adobe_inc + figma_inc + canva_inc
print(f"Run-rate pool (Adobe C&MP + Figma + Canva revenue): ${pool_rr/1000:.2f}B; Adobe share {adobe_rr/pool_rr*100:.1f}%")
print(f"Incremental pool (annualized latest-quarter YoY): ${pool_inc/1000:.2f}B; Adobe share of increment {adobe_inc/pool_inc*100:.1f}%")
print(f"Pool growth {pool_inc/(pool_rr-pool_inc)*100:.1f}% vs Adobe C&MP {adobe_inc/(adobe_rr-adobe_inc)*100:.1f}%")
prev_share = (adobe_rr - adobe_inc) / (pool_rr - pool_inc) * 100
print(f"Adobe share of pool: {prev_share:.1f}% a year ago -> {adobe_rr/pool_rr*100:.1f}% now ({adobe_rr/pool_rr*100-prev_share:+.1f} pts)")
# annual basis with Canva ARR
adobe_dm_inc = get("Adobe", "Digital Media revenue", "FY2025", "annualized_incremental_musd")
figma_fy = get("Figma", "revenue", "FY2025", "annualized_incremental_musd")
canva_arr = get("Canva", "ARR", "CY2025", "annualized_incremental_musd")
tot = adobe_dm_inc + figma_fy + canva_arr
print(f"CY/FY2025 annual basis (Adobe DM, Figma rev, Canva ARR est.): Adobe share of increment {adobe_dm_inc/tot*100:.1f}%")
