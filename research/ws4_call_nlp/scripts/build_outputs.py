#!/usr/bin/env python3
"""Post-process parsed questions: apply hand labels, add degraded-mode calls, build fear index,
prices, forward P/E and charts. Writes to research/ws4_call_nlp/{data,charts}."""
import csv, json, os, re
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/home/user/adbe-stock-pitch/research/ws4_call_nlp/data"
CH = "/home/user/adbe-stock-pitch/research/ws4_call_nlp/charts"
RAW = "/tmp/claude-0/-home-user-adbe-stock-pitch/434e9d74-e598-592e-aa01-e9e6b55767df/scratchpad/raw"
NAVY, TEAL, AMBER, RED, GREY = "#1F3A5F", "#2A9D8F", "#E9A23B", "#C0392B", "#7F8C8D"
STRICT = {"ai_disruption_competition", "seats_pricing_retention"}

CALLS = ["FY23_Q1", "FY23_Q2", "FY23_Q3", "FY23_Q4", "FY24_Q1", "FY24_Q2", "FY24_Q3", "FY24_Q4",
         "FY25_Q1", "FY25_Q2", "FY25_Q3", "FY25_Q4", "FY26_Q1", "FY26_Q2", "FY26_Q3"]
DATES = {"FY23_Q1": "2023-03-15", "FY23_Q2": "2023-06-15", "FY23_Q3": "2023-09-14", "FY23_Q4": "2023-12-13",
         "FY24_Q1": "2024-03-14", "FY24_Q2": "2024-06-13", "FY24_Q3": "2024-09-12", "FY24_Q4": "2024-12-11",
         "FY25_Q1": "2025-03-12", "FY25_Q2": "2025-06-12", "FY25_Q3": "2025-09-11", "FY25_Q4": "2025-12-10",
         "FY26_Q1": "2026-03-12", "FY26_Q2": "2026-06-11", "FY26_Q3": "2026-09-10"}

# ---- hand labels (reviewed all 133 full-text questions from text; overrides listed) ----
HAND = [
    ("FY23_Q1", "I wanted to ask about that top of funnel", "seats_pricing_retention"),
    ("FY23_Q1", "David, for you first, when we spoke at MAX", "ai_monetization"),
    ("FY23_Q1", "I'd love to dig into Figma", "macro_other"),
    ("FY23_Q2", "it's probably for David again", "ai_monetization"),
    ("FY23_Q2", "This is Arsenije on for Alex Zukin", "macro_other"),
    ("FY23_Q2", "We've kind of talked from the beginning that a major differentiation", "ai_monetization"),
    ("FY23_Q2", "Shantanu, at summit, with the content supply chain", "digital_experience"),
    ("FY23_Q2", "This is Elizabeth Porter on for Keith Weiss", "ai_disruption_competition"),
    ("FY23_Q2", "why won't the DX", "macro_other"),
    ("FY23_Q3", "Anil, actually my question is for you", "digital_experience"),
    ("FY23_Q3", "So when I look at Firefly, the amount of image generation", "ai_monetization"),
    ("FY23_Q3", "perspective on kind of the third cloud", "macro_other"),
    ("FY23_Q3", "Shantanu, over the last decade or more", "macro_other"),
    ("FY23_Q4", "going into 2024, it definitely feels like the economy", "macro_other"),
    ("FY23_Q4", "As we think about the momentum within the DX", "digital_experience"),
    ("FY24_Q1", "the magnitude of the beat this quarter", "ai_disruption_competition"),
    ("FY24_Q1", "significantly ramping up your investments", "margins_ai_costs"),
    ("FY24_Q2", "Just how much GenAI demand did you see", "ai_monetization"),
    ("FY24_Q2", "David, on Express, you mentioned the success", "seats_pricing_retention"),
    ("FY24_Q2", "the Q side of the P times Q equation", "seats_pricing_retention"),
    ("FY24_Q2", "driving new Creative All Apps subscriptions from your website", "seats_pricing_retention"),
    ("FY24_Q3", "David, you said monetization. And will consumption", "ai_monetization"),
    ("FY24_Q3", "You touched on some of the drivers in Document", "macro_other"),
    ("FY24_Q3", "I wanted to ask you about the Digital Experience side", "digital_experience"),
    ("FY24_Q4", "AI being meaningful as part of growth narrative", "ai_monetization"),
    ("FY24_Q4", "I wanted to ask David to you if I could on Doc Cloud", "macro_other"),
    ("FY24_Q4", "I just wanted to specifically ask about consumption", "ai_monetization"),
    ("FY24_Q4", "In the past, you provided some good color", "ai_monetization"),
    ("FY24_Q4", "Dan, you noted that your current RPO", "macro_other"),
    ("FY25_Q1", "thank you for the additional disclosure", "macro_other"),
    ("FY25_Q1", "one bearish argument that one could make", "ai_disruption_competition"),
    ("FY25_Q1", "we've seen a lot of consolidation start to happen within the AI realm", "ai_disruption_competition"),
    ("FY25_Q1", "It's great to see the Firefly app tiers", "ai_monetization"),
    ("FY25_Q3", "this was kind of almost, I would say, a turning point quarter", "seats_pricing_retention"),
    ("FY25_Q3", "there’s a thesis out there for software in general", "ai_disruption_competition"),
    ("FY25_Q3", "it’s great to see agents for AEP", "digital_experience"),
    ("FY25_Q4", "partnership announcement and integration with ChatGPT", "ai_monetization"),
    ("FY26_Q1", "Can you talk to us a little bit more about those initiatives", "macro_other"),
    ("FY26_Q2", "with Daniel leaving", "leadership"),
    ("FY26_Q2", "a follow-up just on the decision to defer line optimizations", "seats_pricing_retention"),
    ("FY26_Q2", "there is a lot of debates right now around kind of the moats", "ai_disruption_competition"),
]
NAME_FIX = {"Zelnick": "Brad Zelnick", "Sang-Jin Byun": "Sang-Jin (John) Byun (for Brent Thill)", "unidentifiedparticipant": "Unidentified (for Mark Moerdler)",
            "Ivan Radojicic": "Ivan Radojicic (for Alex Zukin)", "Arsenije Edward Matovic": "Arsenije Matovic (for Alex Zukin)",
            "Elizabeth Mary Elliott Porter": "Elizabeth Porter (for Keith Weiss)"}

# ---- degraded-mode rows (WebSearch reconstruction; partial coverage) ----
DEGRADED = [
    # FY25_Q2 2025-06-12 : typical ~12 questions; 2 recovered with FY25-specific hooks (3 analysts confirmed present but their questions not recovered)
    dict(call="FY25_Q2", speaker="Unidentified analyst", firm="", question_text="[recovered topic] Growing adoption of Express within Acrobat and how pricing works for these products (answered by David Wadhwani).",
         topic_final="seats_pricing_retention", source="WebSearch snippet: stockstory 'The 5 Most Interesting Analyst Questions From Adobe's Q2 Earnings Call' (2025-07-07) via markets.financialcontent.com", coverage="partial coverage (2 of ~12 questions recovered)"),
    dict(call="FY25_Q2", speaker="Unidentified analyst", firm="", question_text="[recovered topic] What is driving the increase in video content on Adobe Stock, and how does Adobe's commercially-safe model strategy affect its market position.",
         topic_final="ai_disruption_competition", source="WebSearch snippet: stockstory 'The 5 Most Interesting Analyst Questions From Adobe's Q2 Earnings Call' (2025-07-07)", coverage="partial coverage (2 of ~12 questions recovered)"),
    # FY26_Q3 2026-09-10 : 6 recovered
    dict(call="FY26_Q3", speaker="Ivan (for Alex Zukin)", firm="Wolfe Research", question_text="[recovered topic] Which AI pricing model across Creative Cloud, Acrobat and enterprise (bundled credits, credit packs, premium tiers, per-seat, usage-based contracts) becomes the primary driver of AI revenue.",
         topic_final="ai_monetization", source="WebSearch snippet (Investing.com / Yahoo transcript pages)", coverage="partial coverage (6 of ~12 questions recovered)"),
    dict(call="FY26_Q3", speaker="Brent Thill", firm="Jefferies", question_text="[recovered topic] Firefly and credit-pack ARR continue to grow and credit consumption is accelerating: what is driving the acceleration, broad usage or certain generation types, and how does it evolve.",
         topic_final="ai_monetization", source="WebSearch snippet (Investing.com transcript summary)", coverage="partial coverage (6 of ~12 questions recovered)"),
    dict(call="FY26_Q3", speaker="Keith Weiss", firm="Morgan Stanley", question_text="[recovered topic] Adobe's differentiation in integrating third-party AI models, and the risk from advertising platforms building their own generative AI.",
         topic_final="ai_disruption_competition", source="WebSearch snippet (Investing.com transcript summary)", coverage="partial coverage (6 of ~12 questions recovered)"),
    dict(call="FY26_Q3", speaker="Brad Zelnick", firm="Deutsche Bank", question_text="[recovered topic] Freemium strategy and conversion: Anil Chakravarthy answered that it is first focused on acquiring new users; creative freemium MAU >100M, +70% y/y.",
         topic_final="seats_pricing_retention", source="WebSearch snippet (GuruFocus 'Earnings Call Highlights' via ca.investing.com / Yahoo)", coverage="partial coverage (6 of ~12 questions recovered)"),
    dict(call="FY26_Q3", speaker="Unidentified analyst", firm="", question_text="[recovered topic] RPO growth of 8% y/y, single digits for the first time since early FY23 and down sequentially.",
         topic_final="macro_other", source="WebSearch snippet (Yahoo Finance 'Adobe Q3 2026 earnings: 1 billion users, raised guidance')", coverage="partial coverage (6 of ~12 questions recovered)"),
    dict(call="FY26_Q3", speaker="Unidentified analyst", firm="", question_text="[recovered topic] Decline in net new ARR; management attributed it to deliberate emphasis on freemium adoption over near-term pricing and seasonality.",
         topic_final="seats_pricing_retention", source="WebSearch snippet (Yahoo Finance 'Adobe Q3 2026 earnings: 1 billion users, raised guidance')", coverage="partial coverage (6 of ~12 questions recovered)"),
]
DEGRADED_PRESENT = {"FY25_Q2": "Alex Zukin (Wolfe), Brent Thill (Jefferies), Jay Vleeschhouwer (Griffin), Kash Rangan (Goldman) confirmed on call; questions not recovered",
                    "FY26_Q3": "Michael Turrin (Wells Fargo), Saket Kalia (Barclays), Tyler Radke (Citi) confirmed on call; questions not recovered"}

# ---- guidance in force after each call (FY non-GAAP EPS, low/high) ----
SEC = "https://www.sec.gov/Archives/edgar/data/796343/"
GUIDE = {
    "FY23_Q1": ("FY23", 15.30, 15.60, "transcript (CFO prepared remarks)", SEC + "000079634323000044/adbeex991q123.htm", ""),
    "FY23_Q2": ("FY23", 15.65, 15.75, "transcript (CFO prepared remarks)", SEC + "000079634323000133/adbeex991q223.htm", ""),
    "FY23_Q3": ("FY23", 15.90, 15.95, "implied: 9M actual non-GAAP EPS 11.80 (3.80+3.91+4.09) + Q4 target 4.10-4.15 from transcript", SEC + "000079634323000198/adbeex991q323.htm", "FY range not restated in call text; implied from quarterly target"),
    "FY23_Q4": ("FY24", 17.60, 18.00, "transcript (CFO prepared remarks)", SEC + "000079634323000252/adbeex991q423.htm", ""),
    "FY24_Q1": ("FY24", 17.60, 18.00, "not updated on call (Q&A: analyst asked management to affirm; prior range carried)", SEC + "000079634324000057/adbeex991q124.htm", "carried from Dec-2023 guide"),
    "FY24_Q2": ("FY24", 18.00, 18.20, "transcript (CFO prepared remarks)", SEC + "000079634324000140/adbeex991q224.htm", ""),
    "FY24_Q3": ("FY24", 18.24, 18.29, "implied: 9M actual 13.61 (4.48+4.48+4.65) + Q4 target 4.63-4.68 from transcript", SEC + "000079634324000200/adbeex991q324.htm", "FY range not restated in call text; implied from quarterly target"),
    "FY24_Q4": ("FY25", 20.20, 20.50, "transcript (CFO prepared remarks)", SEC + "000079634324000250/adbeex991q424.htm", ""),
    "FY25_Q1": ("FY25", 20.20, 20.50, "transcript: 'reaffirm our fiscal '25 targets'", SEC + "000079634325000052/adbeex991q125.htm", ""),
    "FY25_Q2": ("FY25", 20.50, 20.70, "WebSearch snippet of Q2 FY25 press release (8-K ex99.1); transcript not available", SEC + "000079634325000064/adbeex991q225.htm", "retrieved via WebSearch snippet; page not fetchable"),
    "FY25_Q3": ("FY25", 20.80, 20.85, "transcript (CFO prepared remarks)", SEC + "000079634325000102/adbeex991q325.htm", ""),
    "FY25_Q4": ("FY26", 23.30, 23.50, "transcript (CFO prepared remarks)", SEC + "000079634325000135/adbeex991q425.htm", ""),
    "FY26_Q1": ("FY26", 23.30, 23.50, "transcript: 'we are reaffirming our FY '26 targets'", SEC + "000079634326000048/adbeex991q126.htm", ""),
    "FY26_Q2": ("FY26", 24.35, 24.45, "press-release text bundled with transcript file ('Non-GAAP: $24.35 to $24.45') + WebSearch", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000109/adbeex991q226.htm", ""),
    "FY26_Q3": ("FY26", 24.45, 24.50, "WebSearch snippet of Q3 FY26 press release (8-K ex99.1); transcript not available", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm", "retrieved via WebSearch snippet; matches orchestrator anchor"),
}
HEADLINE = {  # revenue $bn, non-GAAP EPS $ (quarter), source
    "FY23_Q1": (4.66, 3.80, "transcript"), "FY23_Q2": (4.82, 3.91, "transcript"), "FY23_Q3": (4.89, 4.09, "transcript"), "FY23_Q4": (5.05, 4.27, "transcript"),
    "FY24_Q1": (5.18, 4.48, "transcript"), "FY24_Q2": (5.31, 4.48, "transcript"), "FY24_Q3": (5.41, 4.65, "transcript"), "FY24_Q4": (5.61, 4.81, "transcript"),
    "FY25_Q1": (5.71, 5.08, "transcript"), "FY25_Q2": (5.87, 5.06, "WebSearch (press release snippet)"), "FY25_Q3": (5.99, 5.31, "transcript"),
    "FY25_Q4": (6.19, 5.49, "transcript (revenue); EPS derived = FY25 20.94 - 9M 15.45"), "FY26_Q1": (6.40, 6.06, "transcript"),
    "FY26_Q2": (6.62, 5.96, "press-release text in transcript file (revenue) / WebSearch (EPS)"), "FY26_Q3": (6.76, 6.13, "WebSearch (press release snippet)"),
}


def main():
    qs = list(csv.DictReader(open(f"{OUT}/analyst_questions_auto.csv")))
    n_override = 0
    for q in qs:
        q["topic_final"] = q["topic_auto"]; q["hand_override"] = ""
        for call, pref, lab in HAND:
            if q["call"] == call and pref in q["question_text"][:400]:
                if lab != q["topic_auto"]:
                    n_override += 1; q["hand_override"] = f"{q['topic_auto']}->{lab}"
                q["topic_final"] = lab
        q["speaker"] = NAME_FIX.get(q["speaker"], q["speaker"])
        q["hand_reviewed"] = "yes (all full-text questions read; see methods.md)"
        q["coverage"] = "full transcript"
    agree = 1 - n_override / len(qs)
    print(f"full-text questions={len(qs)} hand overrides={n_override} keyword-vs-hand agreement={agree:.1%}")
    for d in DEGRADED:
        d.update(date=DATES[d["call"]], q_no="", topic_auto="", hits="", broad_arr_growth_flag=int("ARR" in d["question_text"] or "RPO" in d["question_text"]),
                 operator_intro="", hand_override="", hand_reviewed="n/a (topic from search summary)")
    cols = ["call", "date", "q_no", "speaker", "firm", "question_text", "topic_auto", "topic_final", "hand_override", "hand_reviewed",
            "broad_arr_growth_flag", "hits", "source", "coverage", "operator_intro"]
    allq = qs + DEGRADED
    allq.sort(key=lambda r: (r["date"], str(r["q_no"]).zfill(2)))
    with open(f"{OUT}/analyst_questions.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(allq)
    # ---- fear index ----
    fear = []
    for c in CALLS:
        rows = [r for r in allq if r["call"] == c]
        n = len(rows)
        strict = sum(1 for r in rows if r["topic_final"] in STRICT)
        broad = sum(1 for r in rows if r["topic_final"] in STRICT or int(r["broad_arr_growth_flag"]))
        auto_strict = sum(1 for r in rows if r.get("topic_auto") in STRICT)
        tc = {}
        for r in rows: tc[r["topic_final"]] = tc.get(r["topic_final"], 0) + 1
        partial = c in DEGRADED_PRESENT
        fear.append(dict(call=c, date=DATES[c], n_questions=n, typical_n="12-15" if partial else "",
                         fear_index_strict=round(strict / n, 3) if n else "", fear_index_broad=round(broad / n, 3) if n else "",
                         fear_index_keyword_only=round(auto_strict / n, 3) if (n and not partial) else "",
                         n_ai_disruption=tc.get("ai_disruption_competition", 0), n_seats_pricing=tc.get("seats_pricing_retention", 0),
                         n_ai_monetization=tc.get("ai_monetization", 0), n_dx=tc.get("digital_experience", 0), n_margins=tc.get("margins_ai_costs", 0),
                         n_leadership=tc.get("leadership", 0), n_macro_other=tc.get("macro_other", 0),
                         coverage=("partial coverage: " + DEGRADED_PRESENT[c]) if partial else "full transcript",
                         confidence="LOW (partial coverage; WebSearch reconstruction)" if partial else "medium (hand-labelled full transcript)"))
    pd.DataFrame(fear).to_csv(f"{OUT}/fear_index.csv", index=False)
    # ---- prices ----
    p = pd.read_csv(f"{RAW}/ADBE_prices_brownbear.csv", parse_dates=["Date"]).set_index("Date").sort_index()
    prices = []
    for c in CALLS:
        d = pd.Timestamp(DATES[c])
        if d in p.index:
            i = p.index.get_loc(d); nd = p.index[i + 1]
            prices.append(dict(call=c, call_date=DATES[c], close_call_date=round(float(p.loc[d, "Close"]), 2), next_trading_day=str(nd.date()),
                               close_next_day=round(float(p.loc[nd, "Close"]), 2), reaction_pct=round((p.loc[nd, "Close"] / p.loc[d, "Close"] - 1) * 100, 1),
                               source="GitHub raw: fja05680/brownbear symbol-cache/ADBE.csv (yfinance-derived daily OHLC; cross-checked vs rosidotidev/algo1 db/tickers/ADBE.csv, identical closes)",
                               url="https://raw.githubusercontent.com/fja05680/brownbear/master/symbol-cache/ADBE.csv", notes=""))
        else:
            prices.append(dict(call=c, call_date=DATES[c], close_call_date="", next_trading_day="2026-09-11", close_next_day=252.23, reaction_pct="",
                               source="WebSearch snippet: ad-hoc-news.de 'Adobe Inc. stock gains after record Q3 and raised 2026 guidance' (close USD 252.23 on 2026-09-11)",
                               url="https://www.ad-hoc-news.de/boerse/news/corporate-news/adobe-inc-stock-gains-after-record-q3-and-raised-2026-guidance/70110548",
                               notes="price CSV ends 2026-07-30; Sep-11-2026 close from news snippet (UNVERIFIED second source); call-date close UNAVAILABLE"))
    pdf = pd.DataFrame(prices); pdf.to_csv(f"{OUT}/prices_at_calls.csv", index=False)
    # ---- forward P/E ----
    fpe = []
    for r in prices:
        fy, lo, hi, basis, url, note = GUIDE[r["call"]]
        mid = (lo + hi) / 2
        rev, eps, hsrc = HEADLINE[r["call"]]
        fpe.append(dict(call=r["call"], call_date=r["call_date"], price_date=r["next_trading_day"], price_next_day_close=r["close_next_day"],
                        guidance_fy=fy, guide_eps_low=lo, guide_eps_high=hi, guide_eps_mid=mid, forward_pe=round(r["close_next_day"] / mid, 1),
                        guidance_basis=basis, guidance_url=url, guidance_note=note,
                        q_revenue_bn=rev, q_nongaap_eps=eps, headline_source=hsrc))
    fdf = pd.DataFrame(fpe); fdf.to_csv(f"{OUT}/forward_pe.csv", index=False)
    print(fdf[["call", "price_next_day_close", "guide_eps_mid", "forward_pe"]].to_string())
    fe = pd.DataFrame(fear); print(fe[["call", "n_questions", "fear_index_strict", "fear_index_broad", "fear_index_keyword_only"]].to_string())
    # ---- chart 1: fear index vs forward P/E ----
    fe["date"] = pd.to_datetime(fe["date"]); fdf["call_date"] = pd.to_datetime(fdf["call_date"])
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150); fig.patch.set_facecolor("white")
    full = fe[~fe["call"].isin(DEGRADED_PRESENT)]; part = fe[fe["call"].isin(DEGRADED_PRESENT)]
    ax.plot(full["date"], full["fear_index_strict"].astype(float), color=NAVY, lw=2, marker="o", label="AI-fear index, strict (share of analyst questions; full transcripts)")
    ax.plot(full["date"], full["fear_index_broad"].astype(float), color=TEAL, lw=1.2, ls="--", marker=".", label="AI-fear index, broad (+ net-new-ARR growth questions)")
    ax.scatter(part["date"], part["fear_index_strict"].astype(float), s=140, facecolors="white", edgecolors=RED, zorder=5, label="partial coverage, not connected (FY25 Q2 n=2, FY26 Q3 n=6; LOW confidence)")
    ax.set_ylim(0, 1.08); ax.set_ylabel("Fear index (share of analyst questions)")
    ax.set_xlabel("Earnings call date")
    ax2 = ax.twinx()
    ax2.plot(fdf["call_date"], fdf["forward_pe"], color=AMBER, lw=2, marker="s", label="Forward P/E (next-day close / midpoint of FY non-GAAP EPS guide)")
    ax2.set_ylabel("Forward P/E (x)"); ax2.set_ylim(0, 40)
    for a in (ax, ax2):
        a.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False); ax2.spines["left"].set_visible(False)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2, fontsize=7, frameon=False)
    ax.set_title("Adobe earnings calls: analyst AI-fear index vs forward P/E, FY23 Q1 to FY26 Q3", fontsize=11)
    fig.text(0.01, 0.01, "Source: 13 full transcripts (GitHub mirrors of CapIQ/Fool/Insider Monkey/LSEG); FY25 Q2 and FY26 Q3 via WebSearch (partial); prices: GitHub daily CSV + news; guidance: Adobe 8-K ex99.1. Hand-labelled topics.", fontsize=6.5, color=GREY)
    fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(f"{CH}/fear_index_vs_forward_pe.png"); plt.close(fig)
    # ---- chart 2: seat vs usage vocab ----
    v = pd.read_csv(f"{OUT}/vocab_counts.csv"); v["date"] = pd.to_datetime(v["date"])
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150); fig.patch.set_facecolor("white")
    ax.plot(v["date"], v["seat_per_10k"], color=NAVY, lw=2, marker="o", label="Seat vocabulary (seat/s, per user, license/s, subscriber/s)")
    ax.plot(v["date"], v["usage_per_10k"], color=TEAL, lw=2, marker="o", label="Usage vocabulary (credit/s, consumption, usage, generations, Firefly Services, API, outcome/s)")
    last = v.iloc[-1]; ax.annotate("FY26 Q2: Q&A-only source\n(no prepared remarks)", (last["date"], last["usage_per_10k"]), xytext=(-110, 25), textcoords="offset points", fontsize=7, color=GREY, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    ax.set_ylabel("Mentions per 10,000 management words"); ax.set_xlabel("Earnings call date")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.legend(fontsize=8, frameon=False, loc="upper left")
    ax.set_title("Management language on Adobe calls: seat vocabulary vs usage vocabulary", fontsize=11)
    fig.text(0.01, 0.01, "Source: management text (prepared remarks + answers) of 13 full transcripts from GitHub mirrors; FY25 Q2 and FY26 Q3 UNAVAILABLE (no transcript). Word-boundary regex counts.", fontsize=6.5, color=GREY)
    fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(f"{CH}/seat_vs_usage_vocab.png"); plt.close(fig)
    # ---- chart 3: usage-term introduction timeline ----
    fm = pd.read_csv(f"{OUT}/usage_term_first_mentions.csv"); fm["date"] = pd.to_datetime(fm["date"])
    fm = fm[~fm["term"].isin(["consumption (any sense)", "MAU", "freemium"])].sort_values("date").reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150); fig.patch.set_facecolor("white")
    for i, r in fm.iterrows():
        y = i % 6
        ax.scatter(r["date"], y, color=TEAL, s=40, zorder=3); ax.text(r["date"], y + 0.18, f"{r['term']} ({r['first_call']})", fontsize=7, color=NAVY, rotation=0, ha="left")
    ax.set_yticks([]); ax.set_xlabel("Earnings call date of first management mention"); ax.set_ylim(-0.6, 6.4)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.spines["left"].set_visible(False)
    ax.set_title("When usage-monetization terms first appeared in Adobe management remarks", fontsize=11)
    fig.text(0.01, 0.01, "Source: 13 full transcripts (FY23 Q1-FY26 Q2 excl. FY25 Q2); first call where management used each term. FY25 Q2 and FY26 Q3 not scanned (no transcript).", fontsize=6.5, color=GREY)
    fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(f"{CH}/usage_terms_timeline.png"); plt.close(fig)
    # correlation for findings
    m = fe.merge(fdf[["call", "forward_pe"]], on="call")
    m["fs"] = m["fear_index_strict"].astype(float)
    print("corr(fear_strict, fwd_pe) all 15:", round(m["fs"].corr(m["forward_pe"]), 2), " full-text only:", round(m[~m["call"].isin(DEGRADED_PRESENT)]["fs"].corr(m[~m["call"].isin(DEGRADED_PRESENT)]["forward_pe"]), 2))
    print("vocab means: seat FY23", v.iloc[:4]["seat_per_10k"].mean().round(2), "FY25-26", v.iloc[9:]["seat_per_10k"].mean().round(2), "| usage FY23", v.iloc[:4]["usage_per_10k"].mean().round(2), "FY25-26", v.iloc[9:]["usage_per_10k"].mean().round(2))
    print(v[["call", "mgmt_words", "seat_per_10k", "usage_per_10k"]].to_string())


if __name__ == "__main__":
    main()
