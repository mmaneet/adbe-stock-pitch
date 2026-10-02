#!/usr/bin/env python
"""Build the C4 Google Trends ratios and the three signature charts from the raw request CSVs in data/.

Inputs (per GEO in {US, WW}; written by pytrends on 2026-10-02, or by a manual trends.google.com export renamed to
the same file names - both formats are accepted):
    trends_raw_R1_<GEO>.csv   photoshop, adobe, cancel adobe, photoshop alternative, adobe firefly   (anchor set)
    trends_raw_R2_<GEO>.csv   photoshop, adobe firefly, midjourney, canva ai, chatgpt image
    trends_raw_R3_<GEO>.csv   photoshop, canva, figma, adobe express, chatgpt
    trends_raw_R4_<GEO>.csv   cancel adobe, photoshop alternative, adobe alternative, cancel adobe subscription, adobe firefly
                              (churn-only set: on the R1 scale these terms round to 0-1, so they are pulled alone)
    trends_raw_R2b_<GEO>.csv  adobe firefly, midjourney, canva ai, chatgpt image, leonardo ai (AI-only set, better resolution)

Ratios (monthly, written to trends_ratios_<GEO>.csv):
    churn_intent_ratio_idx  = (cancel adobe + photoshop alternative)[R4] / (photoshop + adobe)[R1], indexed so 2019 avg = 1.00
                              (numerator and denominator come from different requests, so only the SHAPE is meaningful;
                               Google's per-request normalisation is a single constant, so indexing removes it)
    churn_intent_ratio_broad_idx = all four churn terms [R4] / (photoshop + adobe)[R1], 2019 = 1.00
    churn_intent_ratio_R1only    = same definition entirely inside R1 (integer-rounded; cross-check only)
    ai_share_ratio          = adobe firefly / (midjourney + canva ai) [R2b]  (same request -> level is meaningful)
    ai_share_ratio_R2       = same from R2 (cross-check)
    chatgpt_image_vs_photoshop = chatgpt image / photoshop [R2]
Charts: charts/trends_churn_intent_ratio.png, trends_ai_share_ratio.png, trends_chatgpt_image_vs_photoshop.png
Usage: python data/load_trends_ratios.py [--synthetic-test]
"""
import argparse, io, os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); WS = os.path.dirname(HERE); CHARTS = os.path.join(WS, "charts")
NAVY, TEAL, AMBER, RED, GREY = "#1F3A5F", "#2A9D8F", "#E9A23B", "#C0392B", "#7F8C8D"
GEO_LABEL = {"US": "United States", "WW": "Worldwide"}
PARTIAL_MONTH_CUTOFF = "2026-10-01"  # exclusive; first month NOT used
SOURCE = ("Source: Google Trends via pytrends, web search, all categories, monthly 2019-01 to 2026-09 (2026 = Jan-Sep YTD), "
          "pulled 2026-10-02; author's calc. Each Google request is normalised to max = 100 within the request.")


def read_trends_csv(path):
    """pytrends output (month,term,...) or a raw Google Trends multiTimeline.csv export (Category preamble, '<1')."""
    with open(path, encoding="utf-8-sig") as fh:
        lines = fh.read().splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.split(",")[0].strip().lower() in ("month", "week", "day", "date"))
    df = pd.read_csv(io.StringIO("\n".join(lines[start:])))
    dc = df.columns[0]; df[dc] = pd.to_datetime(df[dc]); df = df.set_index(dc); df.index.name = "month"
    df.columns = [c.split(":")[0].strip().lower() for c in df.columns]
    df = df.drop(columns=[c for c in df.columns if c == "ispartial"], errors="ignore")
    df = df.replace("<1", 0.5).apply(pd.to_numeric, errors="coerce")
    if dc.lower() != "month": df = df.resample("MS").mean()
    # drop the partial current month (pytrends flags it isPartial; the 2026-10-01 row holds one day of data)
    df = df[df.index < pd.Timestamp(PARTIAL_MONTH_CUTOFF)]
    return df


def load_geo(geo, folder):
    out = {}
    for r in ("R1", "R2", "R3", "R4", "R2b"):
        p = os.path.join(folder, f"trends_raw_{r}_{geo}.csv")
        if os.path.exists(p): out[r] = read_trends_csv(p)
    return out


def build_ratios(raw):
    r1, r2, r4, r2b = raw.get("R1"), raw.get("R2"), raw.get("R4"), raw.get("R2b")
    idx = r1.index
    out = pd.DataFrame(index=idx)
    denom = r1["photoshop"] + r1["adobe"]
    out["brand_denominator_R1"] = denom
    if r4 is not None:
        num = r4.loc[idx, "cancel adobe"] + r4.loc[idx, "photoshop alternative"]
        broad = num + r4.loc[idx, "adobe alternative"] + r4.loc[idx, "cancel adobe subscription"]
        out["churn_numerator_R4"] = num
        raw_ratio = num / denom; base = raw_ratio[raw_ratio.index.year == 2019].mean()
        out["churn_intent_ratio_idx"] = raw_ratio / base
        rb = broad / denom; out["churn_intent_ratio_broad_idx"] = rb / rb[rb.index.year == 2019].mean()
    out["churn_intent_ratio_R1only"] = (r1["cancel adobe"] + r1["photoshop alternative"]) / denom
    if r2b is not None:
        d = r2b.loc[idx, "midjourney"] + r2b.loc[idx, "canva ai"]
        out["ai_share_ratio"] = (r2b.loc[idx, "adobe firefly"] / d.replace(0, np.nan))
    if r2 is not None:
        d = r2.loc[idx, "midjourney"] + r2.loc[idx, "canva ai"]
        out["ai_share_ratio_R2"] = r2.loc[idx, "adobe firefly"] / d.replace(0, np.nan)
        out["chatgpt_image_R2"] = r2.loc[idx, "chatgpt image"]; out["photoshop_R2"] = r2.loc[idx, "photoshop"]
        out["chatgpt_image_vs_photoshop"] = r2.loc[idx, "chatgpt image"] / r2.loc[idx, "photoshop"]
    return out


def annual(series):
    s = series.dropna(); g = s.groupby(s.index.year).mean()
    return g


def style(ax):
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="y", color="#EEEEEE"); ax.set_axisbelow(True)


def lennox_panel(ax, series_by_geo, ylabel, label_fmt="{:.2f}", ytd_year=2026, first_year=None, ycap=None):
    """Lennox Fig. 1 style: annual-average points joined by a line, each labelled; faint monthly series behind."""
    colors = {"US": NAVY, "WW": TEAL}; markers = {"US": "o", "WW": "s"}
    for geo, s in series_by_geo.items():
        s = s.dropna()
        if first_year: s = s[s.index.year >= first_year]
        if ycap is not None and s.max() > ycap:
            pk = s.idxmax()
            ax.annotate(f"{GEO_LABEL[geo]} monthly peak {s.max():.1f} ({pk.strftime('%b %Y')}), clipped", (pk, ycap), xytext=(-8, -4),
                        textcoords="offset points", ha="right", va="top", fontsize=7.5, color=colors[geo])
        ax.plot(s.index, s.clip(upper=ycap).values if ycap else s.values, color=colors[geo], lw=0.8, alpha=0.3)
        a = annual(s); x = [pd.Timestamp(year=y, month=7, day=1) for y in a.index]
        ax.plot(x, a.values, color=colors[geo], lw=2, marker=markers[geo], ms=7, label=f"{GEO_LABEL[geo]} (annual avg)")
        for xi, yi, yr in zip(x, a.values, a.index):
            ax.annotate(label_fmt.format(yi), (xi, yi), xytext=(0, -14 if geo == "US" else 8), textcoords="offset points",
                        ha="center", fontsize=8, color="#333")
    if ycap is not None: ax.set_ylim(0, ycap * 1.02)
    ax.set_ylabel(ylabel); style(ax)
    yrs = sorted({y for s in series_by_geo.values() for y in s.dropna().index.year if not first_year or y >= first_year})
    ax.set_xticks([pd.Timestamp(year=y, month=7, day=1) for y in yrs])
    ax.set_xticklabels([f"{y} YTD" if y == ytd_year else str(y) for y in yrs], fontsize=9)
    ax.legend(frameon=False, fontsize=8, loc="upper left")


def plot_all(ratios, out_dir, source=SOURCE, tag=""):
    os.makedirs(out_dir, exist_ok=True)
    # 1. churn-intent ratio
    fig, ax = plt.subplots(figsize=(9, 4.8)); fig.patch.set_facecolor("white")
    lennox_panel(ax, {g: r["churn_intent_ratio_idx"] for g, r in ratios.items() if "churn_intent_ratio_idx" in r},
                 "Churn-intent ÷ brand search ratio (2019 avg = 1.00)", ycap=8.5)
    ax.axhline(1.0, color=GREY, lw=0.8, ls="--")
    ax.set_title(f"{tag}Figure 1. Google Trends: ('cancel adobe' + 'photoshop alternative') ÷ ('photoshop' + 'adobe')\n"
                 "Monthly, 2019-01 to 2026-09, indexed to 2019 average = 1.00; annual averages labelled", loc="left", fontsize=10.5)
    fig.text(0.01, 0.01, source + " Numerator from a churn-only request (R4), denominator from the anchor request (R1); level is arbitrary, shape is not.", fontsize=7, color=GREY, wrap=True)
    fig.tight_layout(rect=(0, 0.07, 1, 1)); fig.savefig(os.path.join(out_dir, "trends_churn_intent_ratio.png"), dpi=150); plt.close(fig)
    # 2. AI-share ratio
    fig, ax = plt.subplots(figsize=(9, 4.8)); fig.patch.set_facecolor("white")
    lennox_panel(ax, {g: r["ai_share_ratio"] for g, r in ratios.items() if "ai_share_ratio" in r},
                 "'adobe firefly' ÷ ('midjourney' + 'canva ai')", first_year=2023)
    ax.set_title(f"{tag}Figure 2. Google Trends: 'adobe firefly' ÷ ('midjourney' + 'canva ai')\n"
                 "Monthly from Firefly launch (Mar 2023) to 2026-09; annual averages labelled", loc="left", fontsize=10.5)
    fig.text(0.01, 0.01, source + " All three terms from one request (R2b), so the ratio level is meaningful.", fontsize=7, color=GREY, wrap=True)
    fig.tight_layout(rect=(0, 0.07, 1, 1)); fig.savefig(os.path.join(out_dir, "trends_ai_share_ratio.png"), dpi=150); plt.close(fig)
    # 3. chatgpt image vs photoshop (two panels, one axis each, same request)
    geos = [g for g in ("US", "WW") if g in ratios and "chatgpt_image_R2" in ratios[g]]
    fig, axes = plt.subplots(1, len(geos), figsize=(10, 4.6), sharey=True); fig.patch.set_facecolor("white")
    axes = np.atleast_1d(axes)
    for ax, g in zip(axes, geos):
        r = ratios[g]
        for col, lab, c in (("photoshop_R2", "photoshop", NAVY), ("chatgpt_image_R2", "chatgpt image", AMBER)):
            s = r[col].dropna(); ax.plot(s.index, s.values, color=c, lw=1.8, label=lab)
            a = annual(s)
            for yr, v in a.items():
                if yr >= 2023 or col == "photoshop_R2":
                    ax.annotate(f"{v:.0f}", (pd.Timestamp(year=yr, month=7, day=1), v), xytext=(0, 6 if col == "photoshop_R2" else -12),
                                textcoords="offset points", ha="center", fontsize=7.5, color="#333")
        ax.set_title(GEO_LABEL[g], loc="left", fontsize=11); style(ax); ax.legend(frameon=False, fontsize=8)
        ax.set_xticks([pd.Timestamp(year=y, month=7, day=1) for y in range(2019, 2027)]); ax.set_xticklabels([str(y) if y < 2026 else "2026 YTD" for y in range(2019, 2027)], fontsize=8)
    axes[0].set_ylabel("Search interest, index (request max = 100)")
    fig.suptitle(f"{tag}Figure 3. Google Trends: 'chatgpt image' vs 'photoshop', monthly (same request; annual averages labelled)", x=0.01, ha="left", fontsize=10.5)
    fig.text(0.01, 0.01, source, fontsize=7, color=GREY, wrap=True)
    fig.tight_layout(rect=(0, 0.06, 1, 0.94)); fig.savefig(os.path.join(out_dir, "trends_chatgpt_image_vs_photoshop.png"), dpi=150); plt.close(fig)
    print("charts written to", out_dir)


def synthetic(folder):
    """Write clearly-labelled synthetic_*.csv files in pytrends layout so the loader can be smoke-tested without network."""
    idx = pd.date_range("2019-01-01", "2026-10-01", freq="MS"); n = len(idx); rng = np.random.default_rng(0)
    def mk(cols, scale):
        return pd.DataFrame({c: np.clip(rng.normal(s, 2, n) + np.linspace(0, 5, n), 0, 100).round() for c, s in zip(cols, scale)}, index=idx)
    sets = {"R1": (["photoshop", "adobe", "cancel adobe", "photoshop alternative", "adobe firefly"], [45, 80, 1, 0, 1]),
            "R2": (["photoshop", "adobe firefly", "midjourney", "canva ai", "chatgpt image"], [70, 3, 12, 6, 6]),
            "R3": (["photoshop", "canva", "figma", "adobe express", "chatgpt"], [4, 15, 1, 0, 40]),
            "R4": (["cancel adobe", "photoshop alternative", "adobe alternative", "cancel adobe subscription", "adobe firefly"], [15, 6, 8, 8, 30]),
            "R2b": (["adobe firefly", "midjourney", "canva ai", "chatgpt image", "leonardo ai"], [8, 30, 15, 15, 5])}
    for g in ("US", "WW"):
        for r, (cols, sc) in sets.items():
            d = mk(cols, sc); d.index.name = "month"; d.to_csv(os.path.join(folder, f"synthetic_trends_raw_{r}_{g}.csv"))


def main():
    p = argparse.ArgumentParser(); p.add_argument("--synthetic-test", action="store_true"); p.add_argument("--out-dir"); a = p.parse_args()
    if a.synthetic_test:
        folder = os.path.join(HERE, "_synthetic_test_output"); os.makedirs(folder, exist_ok=True); synthetic(folder)
        # loader expects trends_raw_* names: point it at renamed synthetic copies inside the scratch folder
        for f in os.listdir(folder):
            if f.startswith("synthetic_trends_raw_"): os.replace(os.path.join(folder, f), os.path.join(folder, f.replace("synthetic_", "")))
        ratios = {g: build_ratios(load_geo(g, folder)) for g in ("US", "WW")}
        plot_all(ratios, folder, source="SYNTHETIC EXAMPLE DATA - NOT GOOGLE TRENDS - loader smoke test only.", tag="SYNTHETIC - ")
        for f in os.listdir(folder):  # leave only synthetic_*-named files behind
            if f.startswith("trends_"): os.replace(os.path.join(folder, f), os.path.join(folder, "synthetic_" + f))
        return 0
    ratios = {}
    for g in ("US", "WW"):
        raw = load_geo(g, HERE)
        if "R1" not in raw: print(f"[{g}] missing trends_raw_R1_{g}.csv; skipped"); continue
        r = build_ratios(raw); r.round(4).to_csv(os.path.join(HERE, f"trends_ratios_{g}.csv")); ratios[g] = r
        print(f"\n[{g}] annual averages:")
        cols = [c for c in ("churn_intent_ratio_idx", "churn_intent_ratio_broad_idx", "churn_intent_ratio_R1only", "ai_share_ratio", "ai_share_ratio_R2", "chatgpt_image_vs_photoshop") if c in r]
        print(r[cols].groupby(r.index.year).mean().round(3).to_string())
        print(f"[{g}] 2025-01 onward, monthly churn numerator (R4), denominator (R1), ratio idx:")
        print(r.loc["2025-01-01":, ["churn_numerator_R4", "brand_denominator_R1", "churn_intent_ratio_idx"]].round(2).T.to_string())
    plot_all(ratios, a.out_dir or CHARTS)
    return 0


if __name__ == "__main__": sys.exit(main())
