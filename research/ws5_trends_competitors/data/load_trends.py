#!/usr/bin/env python
"""Load manually exported Google Trends CSVs, chain comparison sets through a shared
anchor term, and draw charts/trends_<GEO>.png.

Expected inputs (see google_trends_MANUAL_EXPORT_INSTRUCTIONS.md):
    data/trends_A_<GEO>.csv   terms: photoshop, canva, figma, midjourney, adobe firefly
    data/trends_B_<GEO>.csv   terms: photoshop, cancel adobe, photoshop alternative, adobe express, adobe firefly
GEO is "US" or "WW".

Chaining: every Google Trends export is normalised so its max = 100. Set B is rescaled so that its
`photoshop` series matches Set A's `photoshop` series (least-squares scale factor through the origin),
which puts all eight terms on Set A's scale. `adobe firefly` appears in both sets only as a cross-check.

Usage:
    python data/load_trends.py                 # all geos whose files exist
    python data/load_trends.py --geo US
    python data/load_trends.py --synthetic-test  # runs on the clearly-labelled synthetic files only
"""
from __future__ import annotations

import argparse
import io
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
CHARTS = os.path.join(WS, "charts")

ANCHOR = "photoshop"
SET_A = ["photoshop", "canva", "figma", "midjourney", "adobe firefly"]
SET_B = ["photoshop", "cancel adobe", "photoshop alternative", "adobe express", "adobe firefly"]
GEO_LABEL = {"US": "United States", "WW": "Worldwide"}

COLORS = {
    "photoshop": "#1F3A5F",
    "canva": "#2A9D8F",
    "figma": "#E9A23B",
    "midjourney": "#C0392B",
    "adobe firefly": "#7F8C8D",
    "adobe express": "#2A9D8F",
    "cancel adobe": "#C0392B",
    "photoshop alternative": "#E9A23B",
}


def read_trends_csv(path: str) -> pd.DataFrame:
    """Parse a Google Trends multiTimeline.csv export into a DataFrame indexed by month.

    Handles the 'Category: ...' preamble, '<1' values, and column labels like
    'canva: (United States)'. Returns columns named by the bare search term.
    """
    with open(path, encoding="utf-8-sig") as fh:
        lines = fh.read().splitlines()
    # find the header row (first line that starts with Month/Week/Day)
    start = next(i for i, ln in enumerate(lines) if ln.split(",")[0].strip() in ("Month", "Week", "Day"))
    df = pd.read_csv(io.StringIO("\n".join(lines[start:])))
    date_col = df.columns[0]
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col)
    df.index.name = "month"
    df.columns = [c.split(":")[0].strip().lower() for c in df.columns]
    df = df.replace("<1", 0.5).apply(pd.to_numeric, errors="coerce")
    # if weekly/daily, roll up to monthly means so sets with different granularity still align
    if date_col != "Month":
        df = df.resample("MS").mean()
    return df


def chain(set_a: pd.DataFrame, set_b: pd.DataFrame, anchor: str = ANCHOR) -> tuple[pd.DataFrame, float, float | None]:
    """Rescale set_b onto set_a's scale using the anchor term; return merged frame, scale, cross-check gap."""
    common = set_a.index.intersection(set_b.index)
    a = set_a.loc[common, anchor].astype(float)
    b = set_b.loc[common, anchor].astype(float)
    mask = (a > 0) & (b > 0)
    if mask.sum() < 3:
        raise ValueError(f"anchor '{anchor}' has too few overlapping non-zero months to chain")
    # least-squares scale through the origin: minimise sum (a - k*b)^2  ->  k = sum(ab)/sum(bb)
    k = float((a[mask] * b[mask]).sum() / (b[mask] ** 2).sum())
    b_scaled = set_b.loc[common].astype(float) * k
    merged = set_a.loc[common].astype(float).copy()
    for col in b_scaled.columns:
        if col == anchor:
            continue
        if col in merged.columns:
            merged[col + " (set B, chained)"] = b_scaled[col]
        else:
            merged[col] = b_scaled[col]
    gap = None
    xcheck = [c for c in set_b.columns if c != anchor and c in set_a.columns]
    if xcheck:
        c = xcheck[0]
        gap = float((merged[c] - merged[c + " (set B, chained)"]).abs().mean())
    return merged, k, gap


def plot(merged: pd.DataFrame, geo: str, out_png: str, source_note: str) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(9, 7.5), sharex=True)
    fig.patch.set_facecolor("white")
    panels = [
        ("Brand / competitor terms (Set A scale, max = 100)", ["photoshop", "canva", "figma", "midjourney", "adobe firefly"]),
        ("Switching-intent terms (chained to Set A scale)", ["cancel adobe", "photoshop alternative", "adobe express"]),
    ]
    for ax, (title, cols) in zip(axes, panels):
        for c in cols:
            if c in merged.columns:
                ax.plot(merged.index, merged[c], label=c, color=COLORS.get(c, "#7F8C8D"), linewidth=1.8)
        ax.set_title(title, loc="left", fontsize=11)
        ax.set_ylabel("Relative search interest (index)")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(frameon=False, fontsize=8, ncol=3)
        ax.grid(axis="y", color="#EEEEEE")
    axes[-1].set_xlabel("Month")
    fig.suptitle(f"Google search interest, {GEO_LABEL.get(geo, geo)}, monthly", x=0.01, ha="left", fontsize=13)
    fig.text(0.01, 0.01, source_note, fontsize=8, color="#7F8C8D")
    fig.tight_layout(rect=(0, 0.03, 1, 0.96))
    fig.savefig(out_png, dpi=150)
    plt.close(fig)


def run(geo: str, file_a: str, file_b: str, out_dir: str, csv_out: str | None, label: str) -> None:
    a = read_trends_csv(file_a)
    b = read_trends_csv(file_b)
    missing_a = [t for t in SET_A if t not in a.columns]
    missing_b = [t for t in SET_B if t not in b.columns]
    if missing_a or missing_b:
        print(f"WARNING: unexpected columns. Missing from A: {missing_a}; from B: {missing_b}")
    merged, k, gap = chain(a, b)
    print(f"[{geo}] chained Set B onto Set A with scale factor k={k:.3f} via '{ANCHOR}'")
    if gap is not None:
        print(f"[{geo}] cross-check 'adobe firefly' mean abs gap after chaining: {gap:.2f} index points "
              f"(<3 is clean; larger means the sets were exported on different dates/settings)")
    if csv_out:
        merged.round(2).to_csv(csv_out)
        print(f"[{geo}] wrote {csv_out}")
    os.makedirs(out_dir, exist_ok=True)
    out_png = os.path.join(out_dir, f"trends_{geo}.png")
    plot(merged, geo, out_png, label)
    print(f"[{geo}] wrote {out_png}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--geo", choices=["US", "WW"], help="process only this geo")
    p.add_argument("--synthetic-test", action="store_true",
                   help="run on data/synthetic_example_trends_*.csv and write to a scratch dir (never charts/)")
    p.add_argument("--out-dir", default=None, help="override output directory for PNGs")
    args = p.parse_args()

    if args.synthetic_test:
        out_dir = args.out_dir or os.path.join(HERE, "_synthetic_test_output")
        fa = os.path.join(HERE, "synthetic_example_trends_A_US.csv")
        fb = os.path.join(HERE, "synthetic_example_trends_B_US.csv")
        run("US", fa, fb, out_dir, None,
            "SYNTHETIC EXAMPLE DATA - NOT GOOGLE TRENDS - loader smoke test only")
        return 0

    geos = [args.geo] if args.geo else ["US", "WW"]
    did_any = False
    for geo in geos:
        fa = os.path.join(HERE, f"trends_A_{geo}.csv")
        fb = os.path.join(HERE, f"trends_B_{geo}.csv")
        if not (os.path.exists(fa) and os.path.exists(fb)):
            print(f"[{geo}] skipped: need both {os.path.basename(fa)} and {os.path.basename(fb)} in data/")
            continue
        run(geo, fa, fb, args.out_dir or CHARTS, os.path.join(HERE, f"trends_chained_{geo}.csv"),
            "Source: Google Trends manual export (trends.google.com), web search, all categories, "
            "monthly, 2021-01 to export date; Set B rescaled to Set A via 'photoshop'.")
        did_any = True
    if not did_any:
        print("Nothing processed. Export the CSVs first (see google_trends_MANUAL_EXPORT_INSTRUCTIONS.md).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
