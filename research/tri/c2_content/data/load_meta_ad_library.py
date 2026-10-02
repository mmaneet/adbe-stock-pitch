#!/usr/bin/env python3
"""Loader for manually collected Meta Ad Library counts (see meta_ad_library_PROTOCOL.md).

Usage:
  python load_meta_ad_library.py                      # loads data/meta_ad_library_wave*.csv (real collections)
  python load_meta_ad_library.py --include-synthetic  # also loads *_SYNTHETIC_EXAMPLE.csv (labelled test data)
  python load_meta_ad_library.py --out charts/meta_ad_library_active_ads.png

Reads every CSV matching the glob, keeps rows with a parseable date and active_ads, builds a brand x date panel,
prints the N/20 tally (brands with higher active ads than in their first wave) and charts:
  (1) active ads per brand over time (log scale, one line per brand, coloured by sector)
  (2) median index across brands (wave 1 = 100).
Synthetic rows are flagged in the chart title in red. Never present synthetic output as real data.
"""
import argparse, glob, os, sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
PALETTE = {"CPG": "#1F3A5F", "Retail": "#2A9D8F", "Auto": "#E9A23B", "Travel": "#C0392B", "QSR": "#7F8C8D"}

def load(include_synthetic: bool) -> pd.DataFrame:
    files = sorted(glob.glob(os.path.join(HERE, "meta_ad_library_wave*.csv")))
    if include_synthetic:
        files += sorted(glob.glob(os.path.join(HERE, "meta_ad_library_*SYNTHETIC*.csv")))
    frames = []
    for f in files:
        df = pd.read_csv(f)
        df["source_file"] = os.path.basename(f)
        df["synthetic"] = "SYNTHETIC" in os.path.basename(f).upper()
        frames.append(df)
    if not frames:
        sys.exit("No filled CSVs found (expected data/meta_ad_library_wave*.csv). Fill the template first.")
    d = pd.concat(frames, ignore_index=True)
    d["date"] = pd.to_datetime(d["date"], errors="coerce")
    d["active_ads"] = pd.to_numeric(d["active_ads"], errors="coerce")
    d = d.dropna(subset=["date", "active_ads"])
    return d

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--include-synthetic", action="store_true")
    ap.add_argument("--out", default=os.path.join(HERE, "..", "charts", "meta_ad_library_active_ads.png"))
    a = ap.parse_args()
    d = load(a.include_synthetic)
    panel = d.pivot_table(index="date", columns="brand", values="active_ads", aggfunc="mean").sort_index()
    first = panel.iloc[0]
    last = panel.iloc[-1]
    up = int((last > first * 1.10).sum()); n = int(last.notna().sum())
    print(f"Brands with active ads >10% above wave 1: {up}/{n} (dates {panel.index[0].date()} -> {panel.index[-1].date()})")
    idx = (panel / first * 100).median(axis=1)
    print("Median index (wave1=100):\n", idx.round(1).to_string())
    is_syn = bool(d["synthetic"].any())
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), dpi=150)
    sectors = d.drop_duplicates("brand").set_index("brand")["sector"].to_dict()
    for b in panel.columns:
        axes[0].plot(panel.index, panel[b], marker="o", ms=3, lw=1.2, color=PALETTE.get(sectors.get(b), "#7F8C8D"), alpha=0.8)
    axes[0].set_yscale("log"); axes[0].set_title("Active US ads per brand (Meta Ad Library, manual counts)")
    axes[0].set_ylabel("active ads (log)")
    axes[1].plot(idx.index, idx.values, marker="o", color="#1F3A5F", lw=2)
    axes[1].axhline(100, color="#7F8C8D", lw=0.8, ls="--"); axes[1].set_title("Median brand index (wave 1 = 100)")
    for ax in axes:
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(axis="x", rotation=30)
    if is_syn:
        fig.suptitle("SYNTHETIC EXAMPLE DATA - NOT REAL OBSERVATIONS", color="#C0392B", fontweight="bold")
    fig.text(0.01, 0.01, "Source: manual Meta Ad Library collection per data/meta_ad_library_PROTOCOL.md; small non-random sample.",
             fontsize=7, color="#7F8C8D")
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    fig.savefig(a.out, facecolor="white"); print("wrote", a.out)

if __name__ == "__main__":
    main()
