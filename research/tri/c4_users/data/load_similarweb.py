#!/usr/bin/env python
"""Load the manually filled similarweb_template.csv (see similarweb_PROTOCOL.md) and draw
charts/similarweb_visits_by_domain.png: total visits per month, one line per domain, on ONE axis (log scale,
because chatgpt.com/canva.com dwarf the Adobe subdomains). Usage:
    python data/load_similarweb.py                      # reads data/similarweb_template.csv (filled rows only)
    python data/load_similarweb.py --synthetic-test     # reads synthetic_similarweb_example.csv, writes to a scratch dir
"""
import argparse, os, re, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); WS = os.path.dirname(HERE); CHARTS = os.path.join(WS, "charts")
ORDER = ["firefly.adobe.com", "express.adobe.com", "acrobat.adobe.com", "adobe.com", "canva.com", "figma.com", "midjourney.com", "chatgpt.com"]
COLORS = {"firefly.adobe.com": "#1F3A5F", "express.adobe.com": "#2A9D8F", "acrobat.adobe.com": "#E9A23B", "adobe.com": "#7F8C8D",
          "canva.com": "#C0392B", "figma.com": "#6C5B7B", "midjourney.com": "#355C7D", "chatgpt.com": "#99B898"}
STYLES = {"adobe.com": "--", "canva.com": "-", "figma.com": "-.", "midjourney.com": ":", "chatgpt.com": "--"}

def parse_visits(v):
    """Accept 12400000, '12.4M', '850K', '1.2B'."""
    if pd.isna(v) or str(v).strip() == "": return float("nan")
    s = str(v).strip().replace(",", "")
    m = re.match(r"^([0-9.]+)\s*([KMB]?)$", s, re.I)
    if not m: return float("nan")
    mult = {"": 1, "K": 1e3, "M": 1e6, "B": 1e9}[m.group(2).upper()]
    return float(m.group(1)) * mult

def load(path):
    df = pd.read_csv(path, dtype=str)
    df["total_visits"] = df["total_visits"].map(parse_visits)
    df = df.dropna(subset=["total_visits"])
    df["month"] = pd.to_datetime(df["month"], format="%Y-%m", errors="coerce")
    return df.dropna(subset=["month"])

def plot(df, out_png, source_note):
    fig, ax = plt.subplots(figsize=(9, 5)); fig.patch.set_facecolor("white")
    for dom in ORDER:
        sub = df[df["domain"] == dom].sort_values("month")
        if sub.empty: continue
        ax.plot(sub["month"], sub["total_visits"], marker="o", ms=5, lw=2, ls=STYLES.get(dom, "-"), color=COLORS.get(dom, "#7F8C8D"), label=dom)
        ax.annotate(dom, (sub["month"].iloc[-1], sub["total_visits"].iloc[-1]), xytext=(5, 0), textcoords="offset points", fontsize=8, va="center", color="#333")
    ax.set_yscale("log"); ax.set_ylabel("Total visits per month (log scale)"); ax.set_xlabel("Month")
    ax.set_title("Web visits by domain (Similarweb, manual collection)", loc="left", fontsize=12)
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="y", color="#EEEEEE", which="both"); ax.legend(frameon=False, fontsize=8, ncol=2)
    fig.text(0.01, 0.01, source_note, fontsize=7, color="#7F8C8D"); fig.tight_layout(rect=(0, 0.04, 1, 1))
    os.makedirs(os.path.dirname(out_png), exist_ok=True); fig.savefig(out_png, dpi=150); plt.close(fig); print("wrote", out_png)

def main():
    p = argparse.ArgumentParser(); p.add_argument("--synthetic-test", action="store_true"); p.add_argument("--out-dir"); a = p.parse_args()
    if a.synthetic_test:
        df = load(os.path.join(HERE, "synthetic_similarweb_example.csv"))
        plot(df, os.path.join(a.out_dir or os.path.join(HERE, "_synthetic_test_output"), "similarweb_visits_by_domain_SYNTHETIC.png"),
             "SYNTHETIC EXAMPLE DATA - NOT SIMILARWEB - loader smoke test only"); return 0
    df = load(os.path.join(HERE, "similarweb_template.csv"))
    if df.empty: print("No filled rows in similarweb_template.csv yet; follow similarweb_PROTOCOL.md"); return 1
    coll = ", ".join(sorted(df["date_collected"].dropna().unique()))
    plot(df, os.path.join(a.out_dir or CHARTS, "similarweb_visits_by_domain.png"),
         f"Source: similarweb.com/website/<domain> free overview, collected manually {coll}; modelled estimates, web only (no apps).")
    return 0
if __name__ == "__main__": sys.exit(main())
