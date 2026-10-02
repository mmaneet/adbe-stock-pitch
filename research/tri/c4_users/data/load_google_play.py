#!/usr/bin/env python
"""Load google_play_template.csv (filled by hand per google_play_PROTOCOL.md) and draw
charts/google_play_reviews_by_app.png: review count by snapshot date, one line per app, install-tier changes annotated.
    python data/load_google_play.py
    python data/load_google_play.py --synthetic-test
"""
import argparse, os, re, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); WS = os.path.dirname(HERE); CHARTS = os.path.join(WS, "charts")
PALETTE = ["#1F3A5F", "#2A9D8F", "#E9A23B", "#C0392B", "#7F8C8D", "#6C5B7B"]

def parse_num(v):
    if pd.isna(v) or str(v).strip() == "": return float("nan")
    s = str(v).strip().replace(",", "").replace("+", "")
    m = re.match(r"^([0-9.]+)\s*([KMB]?)$", s, re.I)
    if not m: return float("nan")
    return float(m.group(1)) * {"": 1, "K": 1e3, "M": 1e6, "B": 1e9}[m.group(2).upper()]

def load(path):
    df = pd.read_csv(path, dtype=str)
    df["reviews_n"] = df["reviews"].map(parse_num)
    df["snapshot_date"] = pd.to_datetime(df["snapshot_date"], errors="coerce")
    return df.dropna(subset=["snapshot_date", "reviews_n"]).sort_values(["app", "snapshot_date"])

def plot(df, out_png, source_note):
    fig, ax = plt.subplots(figsize=(9, 5)); fig.patch.set_facecolor("white")
    for i, (app, sub) in enumerate(df.groupby("app", sort=False)):
        c = PALETTE[i % len(PALETTE)]
        ax.plot(sub["snapshot_date"], sub["reviews_n"], marker="o", ms=5, lw=2, color=c, label=app)
        ax.annotate(app, (sub["snapshot_date"].iloc[-1], sub["reviews_n"].iloc[-1]), xytext=(5, 0), textcoords="offset points", fontsize=8, va="center")
        prev = None
        for _, r in sub.iterrows():
            tier = str(r.get("install_tier", "")).strip()
            if tier and tier != prev and prev is not None:
                ax.annotate(f"-> {tier}", (r["snapshot_date"], r["reviews_n"]), xytext=(0, 9), textcoords="offset points", fontsize=7.5, ha="center", color=c)
            prev = tier or prev
    ax.set_yscale("log"); ax.set_ylabel("Google Play review count (log scale)"); ax.set_xlabel("Snapshot date")
    ax.set_title("Android adoption proxy: Play Store reviews, with install-tier changes", loc="left", fontsize=12)
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="y", which="both", color="#EEEEEE"); ax.legend(frameon=False, fontsize=8)
    fig.text(0.01, 0.01, source_note, fontsize=7, color="#7F8C8D"); fig.tight_layout(rect=(0, 0.04, 1, 1))
    os.makedirs(os.path.dirname(out_png), exist_ok=True); fig.savefig(out_png, dpi=150); plt.close(fig); print("wrote", out_png)

def main():
    p = argparse.ArgumentParser(); p.add_argument("--synthetic-test", action="store_true"); p.add_argument("--out-dir"); a = p.parse_args()
    if a.synthetic_test:
        plot(load(os.path.join(HERE, "synthetic_google_play_example.csv")),
             os.path.join(a.out_dir or os.path.join(HERE, "_synthetic_test_output"), "google_play_reviews_by_app_SYNTHETIC.png"),
             "SYNTHETIC EXAMPLE DATA - NOT GOOGLE PLAY - loader smoke test only"); return 0
    df = load(os.path.join(HERE, "google_play_template.csv"))
    if df.empty: print("No filled rows yet; follow google_play_PROTOCOL.md"); return 1
    plot(df, os.path.join(a.out_dir or CHARTS, "google_play_reviews_by_app.png"),
         "Source: play.google.com listings (today) and web.archive.org snapshots of the same URLs, collected manually; Android only.")
    return 0
if __name__ == "__main__": sys.exit(main())
