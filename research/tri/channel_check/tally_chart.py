#!/usr/bin/env python
"""
tally_chart.py -- tally a filled channel-check CSV and draw the Lennox-style
stacked horizontal bar chart (Table 1 in inputs/Maneet_Mehta_YSIG2026Pitch.pdf, p. 4).

Usage
  python tally_chart.py data/responses_A_template.csv --survey A \
      --title "Table 1. Creative-ops channel check, October 2026" \
      --out charts/channel_check_A.png
  python tally_chart.py data/responses_B_template.csv --survey B --include-examples \
      --title "Table 2. Freelancer and student channel check, October 2026" \
      --out charts/channel_check_B_EXAMPLE.png

Behaviour
  * Rows whose respondent_id starts with EXAMPLE_ are dropped unless --include-examples
    is passed; with it, the title is suffixed "(EXAMPLE DATA)".
  * q1..q5 are tallied Yes / No (case-insensitive; Y/N accepted). Blanks or other
    values count as "not answered" and are reported but not drawn.
  * Prints a markdown tally table ("17/20" style) plus medians of the numeric items
    present (q2_pct_change, q6_headcount_pct).
  * Chart: blue #2F6DB5 = Yes (count printed inside, white), grey #BFBFBF = No
    (count inside, dark), x-axis 0..n "Respondents (n = N)", legend at bottom,
    source line "Author's channel check, <month>; small, non-random sample."
Requires pandas + matplotlib (both in the repo venv).
"""
import argparse
import sys
import textwrap
from datetime import date
from pathlib import Path

import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

BLUE = "#2F6DB5"   # Yes
GREY = "#BFBFBF"   # No
INK = "#222222"
MUTED = "#6B6B6B"

# Chart labels, and what a "Yes" means for the long thesis (used in the printed table).
QUESTIONS = {
    "A": [
        ("q1", "Has your team's Creative Cloud seat count fallen in the last 2 years?",
         "Yes WEAKENS (seat-compression concession)"),
        ("q2", "Has the number of creative assets produced per campaign increased since 2024?",
         "Yes SUPPORTS C2"),
        ("q3", "Do you pay for Adobe AI (Firefly credits, Firefly Services, GenStudio)?",
         "Yes SUPPORTS C3"),
        ("q4", "Have you replaced any Adobe product with an AI-native tool (Canva, Figma, ChatGPT, Midjourney)?",
         "Yes WEAKENS C4 (falsifier)"),
        ("q5", "Does your organization require commercially safe / indemnified AI for production content?",
         "Yes SUPPORTS C3"),
    ],
    "B": [
        ("q1", "Have you cancelled or downgraded Creative Cloud in the last 2 years?",
         "Yes WEAKENS (individual-subscriber concession)"),
        ("q2", "Do you use Firefly (generative fill, text-to-image, credits)?",
         "Yes SUPPORTS C3/C4"),
        ("q3", "Have you moved any paid work to ChatGPT, Canva or Midjourney?",
         "Yes WEAKENS C4 (falsifier)"),
        ("q4", "Do clients require Adobe file formats (PSD, AI, INDD, PDF)?",
         "Yes SUPPORTS C1"),
        ("q5", "Do you expect to keep Creative Cloud next year?",
         "Yes SUPPORTS C4"),
    ],
}
NUMERIC = {"A": ["q2_pct_change", "q6_headcount_pct"], "B": []}


def norm_yn(v):
    s = str(v).strip().lower() if pd.notna(v) else ""
    if s in ("yes", "y", "true", "1"):
        return "Yes"
    if s in ("no", "n", "false", "0"):
        return "No"
    return None


def month_label(df, override):
    if override:
        return override
    if "date" in df.columns:
        d = pd.to_datetime(df["date"], errors="coerce").dropna()
        if len(d):
            return d.max().strftime("%B %Y")
    return date.today().strftime("%B %Y")


def draw(tally, n, title, out, month, wrap=42):
    rows = list(reversed(tally))  # first question at the top
    labels = [textwrap.fill(q, wrap) for _, q, _, _, _ in rows]
    yes = [y for _, _, y, _, _ in rows]
    no = [k for _, _, _, k, _ in rows]
    y = range(len(rows))
    max_lines = max(l.count("\n") + 1 for l in labels)
    fig_h = 1.6 + len(rows) * (0.34 + 0.17 * max_lines)
    fig, ax = plt.subplots(figsize=(7.6, fig_h), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    h = 0.62
    ax.barh(y, yes, height=h, color=BLUE, edgecolor="white", linewidth=1.0)
    ax.barh(y, no, left=yes, height=h, color=GREY, edgecolor="white", linewidth=1.0)
    for i, (a, b) in enumerate(zip(yes, no)):
        if a:
            ax.text(a / 2, i, str(a), ha="center", va="center", color="white",
                    fontsize=10, fontweight="bold")
        if b:
            ax.text(a + b / 2, i, str(b), ha="center", va="center", color=INK, fontsize=10)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=8.5, color=INK)
    ax.set_xlim(0, n)
    step = 1 if n <= 25 else (2 if n <= 50 else 5)
    ax.set_xticks(range(0, n + 1, step))
    ax.tick_params(axis="x", labelsize=8, colors=INK, length=3)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel(f"Respondents (n = {n})", fontsize=8.5, color=INK)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#444444")
        ax.spines[s].set_linewidth(0.8)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    fig.suptitle(textwrap.fill(title, 78), fontsize=10, color=INK, y=0.975, va="top")
    fig.legend(handles=[Patch(color=BLUE, label="Yes"), Patch(color=GREY, label="No")],
               loc="lower center", ncol=2, frameon=False, fontsize=8.5,
               bbox_to_anchor=(0.5, 0.055), handlelength=1.6, columnspacing=2.0)
    fig.text(0.5, 0.012, f"Author's channel check, {month}; small, non-random sample.",
             ha="center", va="bottom", fontsize=7, color=MUTED)
    top = 0.86 if len(title) < 80 else 0.82
    fig.subplots_adjust(left=0.40, right=0.97, top=top, bottom=0.27 if len(rows) <= 3 else 0.21)
    fig.patch.set_edgecolor("#888888")
    fig.patch.set_linewidth(0.8)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, facecolor="white", edgecolor=fig.patch.get_edgecolor())
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--survey", choices=["A", "B"], default=None,
                   help="question set; inferred from filename (_A_/_B_) if omitted")
    p.add_argument("--title", default=None)
    p.add_argument("--out", default=None)
    p.add_argument("--include-examples", action="store_true",
                   help="keep EXAMPLE_ rows (title gets an EXAMPLE DATA suffix)")
    p.add_argument("--month", default=None, help='source-line month, e.g. "October 2026"')
    p.add_argument("--wrap", type=int, default=42, help="label wrap width in characters")
    a = p.parse_args()

    survey = a.survey
    if survey is None:
        name = Path(a.csv).name.upper()
        survey = "B" if "_B" in name else "A"
    df = pd.read_csv(a.csv, dtype=str)
    df.columns = [c.strip() for c in df.columns]
    is_ex = df["respondent_id"].fillna("").str.startswith("EXAMPLE_")
    n_ex = int(is_ex.sum())
    if not a.include_examples:
        df = df[~is_ex]
    if len(df) == 0:
        sys.exit(f"No data rows in {a.csv} ({n_ex} EXAMPLE_ rows were dropped; pass --include-examples to keep them).")
    n = len(df)

    title = a.title or f"Channel check, survey {survey}"
    if a.include_examples and n_ex:
        title = f"{title} (EXAMPLE DATA)"
    month = month_label(df, a.month)
    out = a.out or f"charts/channel_check_{survey}.png"

    tally = []
    for col, text, reads in QUESTIONS[survey]:
        vals = df[col].map(norm_yn) if col in df.columns else pd.Series([None] * n)
        yes, no = int((vals == "Yes").sum()), int((vals == "No").sum())
        tally.append((col, text, yes, no, reads))

    print(f"Survey {survey}: {n} respondents" + (f" (incl. {n_ex} EXAMPLE_ rows)" if a.include_examples and n_ex else f" ({n_ex} EXAMPLE_ rows dropped)"))
    print()
    print("| # | Question | Yes | No | Yes share | What a Yes means |")
    print("|---|---|---|---|---|---|")
    for col, text, yes, no, reads in tally:
        answered = yes + no
        na = n - answered
        share = f"{yes}/{answered}" + (f" ({yes/answered:.0%})" if answered else "")
        if na:
            share += f", {na} n/a"
        print(f"| {col} | {text} | {yes} | {no} | {share} | {reads} |")
    for col in NUMERIC[survey]:
        if col in df.columns:
            s = pd.to_numeric(df[col], errors="coerce").dropna()
            if len(s):
                print(f"\n{col}: n={len(s)}, median={s.median():+.0f}%, mean={s.mean():+.1f}%, "
                      f"min={s.min():+.0f}%, max={s.max():+.0f}%")
    draw(tally, n, title, out, month, wrap=a.wrap)
    print(f"\nChart written: {out}")


if __name__ == "__main__":
    main()
