"""Workstream tabs for ADBE_alt_data.xlsx. Each add_* function is guarded: missing files -> tab with a note."""
import os, glob
import pandas as pd
from openpyxl.styles import Font

def _num(v):
    try:
        if v is None or (isinstance(v, float) and pd.isna(v)): return None
        return float(v)
    except Exception:
        return None

def note(ws, r, text):
    ws.cell(row=r, column=1, value=text).font = Font(italic=True, color="7F8C8D")

def add_trends_competitors(wb, ctx):
    read_csv, write_df, hdr, autosize, BLUE, BLACK, BOLD, ROOT = ctx
    ws = wb.create_sheet("Trends_Competitors")
    ws["A1"] = "WS5: competitor growth vs Adobe (blue = sourced input; black = formula)"; ws["A1"].font = BOLD
    df = read_csv("ws5_trends_competitors/data/growth_comparison.csv")
    r = 3
    if df is None:
        note(ws, r, "UNAVAILABLE: growth_comparison.csv missing"); return
    note(ws, r, "Source: research/ws5_trends_competitors/data/growth_comparison.csv; each row's primary URL is in the Sources tab (WS5). Google Trends: UNAVAILABLE (host blocked); manual export kit in ws5 data/."); r += 1
    cols = ["entity","metric","period","period_end","value_musd","prior_value_musd","yoy_growth_calc","incremental_calc","annualized_incremental_calc","basis","note"]
    hdr(ws, r, cols); r += 1
    for _, rec in df.iterrows():
        ws.cell(row=r, column=1, value=rec["entity"]); ws.cell(row=r, column=2, value=rec["metric"])
        ws.cell(row=r, column=3, value=rec["period"]); ws.cell(row=r, column=4, value=rec["period_end"])
        v = _num(rec["value_musd"]); p = _num(rec["prior_value_musd"])
        c = ws.cell(row=r, column=5, value=v); c.font = BLUE
        c = ws.cell(row=r, column=6, value=p); c.font = BLUE
        if v is not None and p:
            ws.cell(row=r, column=7, value=f"=E{r}/F{r}-1").number_format = "0.0%"
            ws.cell(row=r, column=8, value=f"=E{r}-F{r}")
            mult = 4 if str(rec["period"]).startswith("Q") else 1
            ws.cell(row=r, column=9, value=f"=H{r}*{mult}")
        elif _num(rec["yoy_growth_pct"]) is not None:
            c = ws.cell(row=r, column=7, value=_num(rec["yoy_growth_pct"])/100); c.font = BLUE; c.number_format = "0.0%"
        ws.cell(row=r, column=10, value=rec["basis"]); ws.cell(row=r, column=11, value=rec["note"])
        r += 1
    # share-of-pool block
    r += 1
    ws.cell(row=r, column=1, value="Share-of-pool calc (latest annualized run-rates; formulas)").font = BOLD; r += 1
    hdr(ws, r, ["entity","run_rate_musd (latest quarter x4 / ARR)","annualized_increment_musd","share_of_stock","share_of_increment"]); r += 1
    rows = {"Adobe C&MP (Q3 FY26 x4)": (4651*4, 2136), "Figma (Q2'26 x4)": (370.1*4, 482.0), "Canva (Q2'26 revenue x4)": (921.9*4, 742.4)}
    first = r
    for k, (rr, inc) in rows.items():
        ws.cell(row=r, column=1, value=k)
        ws.cell(row=r, column=2, value=rr).font = BLUE
        ws.cell(row=r, column=3, value=inc).font = BLUE
        r += 1
    last = r - 1
    for rr_ in range(first, last + 1):
        ws.cell(row=rr_, column=4, value=f"=B{rr_}/SUM($B${first}:$B${last})").number_format = "0.0%"
        ws.cell(row=rr_, column=5, value=f"=C{rr_}/SUM($C${first}:$C${last})").number_format = "0.0%"
    ws.cell(row=r, column=1, value="Pool total"); ws.cell(row=r, column=2, value=f"=SUM(B{first}:B{last})"); ws.cell(row=r, column=3, value=f"=SUM(C{first}:C{last})")
    ws.cell(row=r+1, column=1, value="Pool growth (increment / (stock - increment))"); ws.cell(row=r+1, column=2, value=f"=C{r}/(B{r}-C{r})").number_format = "0.0%"
    autosize(ws)

def add_sources(wb, ctx):
    read_csv, write_df, hdr, autosize, BLUE, BLACK, BOLD, ROOT = ctx
    ws = wb.create_sheet("Sources")
    ws["A1"] = "All workstream sources (concatenated from each ws*/sources.csv)"; ws["A1"].font = BOLD
    hdr(ws, 3, ["workstream","claim","value","url","date_accessed","notes"])
    r = 4
    for p in sorted(glob.glob(os.path.join(ROOT, "ws*_*", "sources.csv"))):
        wsname = os.path.basename(os.path.dirname(p))
        try:
            df = pd.read_csv(p)
        except Exception as e:
            ws.cell(row=r, column=1, value=wsname); ws.cell(row=r, column=2, value=f"ERROR reading sources.csv: {e}"); r += 1; continue
        for _, rec in df.iterrows():
            ws.cell(row=r, column=1, value=wsname)
            for j, col in enumerate(["claim","value","url","date_accessed","notes"]):
                v = rec.get(col)
                ws.cell(row=r, column=2 + j, value=None if (isinstance(v, float) and pd.isna(v)) else (str(v) if v is not None else None))
            r += 1
    autosize(ws, maxw=80)

# placeholders, filled in as workstreams complete
def add_price_volume(wb, ctx):
    read_csv, write_df, hdr, autosize, BLUE, BLACK, BOLD, ROOT = ctx
    ws = wb.create_sheet("PriceVolume")
    ws["A1"] = "WS1: price vs volume decomposition (blue = sourced/modelled input; black = formula)"; ws["A1"].font = BOLD
    dec = read_csv("ws1_price_volume/data/decomposition.csv")
    r = 3
    if dec is None:
        note(ws, r, "UNAVAILABLE: decomposition.csv missing"); return
    note(ws, r, "Method (ws1 methods.md): cc growth = reported - FX gap; organic = cc - Semrush pts; implied volume/mix = (1+organic)/(1+price) - 1. Price contribution pts come from ws1 data/price_model.csv (list uplift x share repriced x renewal phase-in). Semrush Q3 FY26 revenue is an ESTIMATE."); r += 1
    cols = ["fiscal_quarter","group","scenario","share_repriced","sub_rev_m","prior_year_sub_rev_m","reported_growth_pct","fx_adj_pts","cc_growth_pct","semrush_rev_m","semrush_pts","organic_cc_growth_pct","price_contrib_pts","implied_volume_mix_pct","price_contrib_m2m_pts","implied_volume_m2m_pct","fx_note"]
    hdr(ws, r, cols); r += 1
    for _, rec in dec.iterrows():
        ws.cell(row=r, column=1, value=rec["fiscal_quarter"]); ws.cell(row=r, column=2, value=rec["group"]); ws.cell(row=r, column=3, value=rec["scenario"])
        ws.cell(row=r, column=4, value=_num(rec["scenario_share_repriced"])).font = BLUE
        ws.cell(row=r, column=5, value=_num(rec["sub_rev_m"])).font = BLUE
        ws.cell(row=r, column=6, value=_num(rec["prior_year_sub_rev_m"])).font = BLUE
        ws.cell(row=r, column=7, value=f"=(E{r}/F{r}-1)*100").number_format = "0.00"
        ws.cell(row=r, column=8, value=_num(rec["fx_adj_pts"])).font = BLUE
        ws.cell(row=r, column=9, value=f"=G{r}-H{r}").number_format = "0.00"
        ws.cell(row=r, column=10, value=_num(rec["semrush_rev_m"])).font = BLUE
        ws.cell(row=r, column=11, value=f"=J{r}/F{r}*100").number_format = "0.00"
        ws.cell(row=r, column=12, value=f"=I{r}-K{r}").number_format = "0.00"
        ws.cell(row=r, column=13, value=_num(rec["price_contrib_pts"])).font = BLUE
        ws.cell(row=r, column=14, value=f"=((1+L{r}/100)/(1+M{r}/100)-1)*100").number_format = "0.00"
        ws.cell(row=r, column=15, value=_num(rec["price_contrib_m2m_sensitivity_pts"])).font = BLUE
        ws.cell(row=r, column=16, value=f"=((1+L{r}/100)/(1+O{r}/100)-1)*100").number_format = "0.00"
        ws.cell(row=r, column=17, value=rec["fx_note"])
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Price-change log (ws1 data/price_log.csv; list prices, US unless noted)").font = BOLD; r += 1
    pl = read_csv("ws1_price_volume/data/price_log.csv")
    if pl is not None:
        hdr(ws, r, list(pl.columns)); r += 1
        for _, rec in pl.iterrows():
            for j, col in enumerate(pl.columns):
                v = rec[col]
                if col in ("old_price","new_price"):
                    c = ws.cell(row=r, column=1+j, value=_num(v)); c.font = BLUE
                elif col == "pct_change":
                    oc = 1 + list(pl.columns).index("old_price"); nc = 1 + list(pl.columns).index("new_price")
                    if _num(rec["old_price"]) and _num(rec["new_price"]) is not None:
                        from openpyxl.utils import get_column_letter as gcl
                        ws.cell(row=r, column=1+j, value=f"=({gcl(nc)}{r}/{gcl(oc)}{r}-1)*100").number_format = "0.0"
                    else:
                        ws.cell(row=r, column=1+j, value=_num(v)).font = BLUE
                else:
                    ws.cell(row=r, column=1+j, value=None if (isinstance(v, float) and pd.isna(v)) else v)
            r += 1
    autosize(ws, maxw=50)
def add_seat_compression(wb, ctx):
    read_csv, write_df, hdr, autosize, BLUE, BLACK, BOLD, ROOT = ctx
    from openpyxl.utils import get_column_letter as gcl
    ws = wb.create_sheet("SeatCompression")
    ws["A1"] = "WS2: revenue per creative worker / seat compression (blue = sourced input; black = formula)"; ws["A1"].font = BOLD
    note(ws, 2, "MISMATCH: Adobe revenue is GLOBAL (fiscal year ending Nov/Dec); employment is US-only BLS OEWS wage-and-salary (May reference). Indices only, not per-seat dollars.")
    emp = read_csv("ws2_seat_compression/data/bls_oews_employment_wide.csv")
    rev = read_csv("ws2_seat_compression/data/adobe_revenue.csv")
    r = 4
    if emp is None or rev is None:
        note(ws, r, "UNAVAILABLE: ws2 data files missing"); return
    # Block A: employment + revenue by year
    ws.cell(row=r, column=1, value="A. BLS OEWS national employment (May) and Adobe revenue (USD bn), 2019-2025").font = BOLD; r += 1
    soc = ["27-1024","27-1011","27-1014","27-4032","27-4021","11-2021","13-1161"]
    cols = ["year"] + soc + ["creative5_sum (f)","marketing2_sum (f)","DM_rev_bn","creative_rev_bn","total_rev_bn","creative5_idx (f)","DM_rev_idx (f)","DM_rev_per_worker_idx (f)","creative_rev_per_worker_idx (f)"]
    hdr(ws, r, cols); r += 1
    first = r
    rev_by_year = {int(x["fiscal_year"]): x for _, x in rev.iterrows()}
    for _, rec in emp.iterrows():
        y = int(rec["year"])
        ws.cell(row=r, column=1, value=y)
        for j, s in enumerate(soc):
            ws.cell(row=r, column=2 + j, value=_num(rec[s])).font = BLUE
        c5 = 2 + len(soc); m2 = c5 + 1
        ws.cell(row=r, column=c5, value=f"=SUM(B{r}:F{r})")
        ws.cell(row=r, column=m2, value=f"=G{r}+H{r}")
        rr = rev_by_year.get(y, {})
        for k, col in enumerate(["digital_media_revenue_usd_bn","creative_revenue_usd_bn","total_revenue_usd_bn"]):
            v = _num(rr.get(col)) if rr is not None and len(rr) else None
            ws.cell(row=r, column=m2 + 1 + k, value=v).font = BLUE
        dm = gcl(m2 + 1); cr = gcl(m2 + 2); c5l = gcl(c5)
        ws.cell(row=r, column=m2 + 4, value=f"={c5l}{r}/{c5l}${first}*100").number_format = "0.0"
        ws.cell(row=r, column=m2 + 5, value=f"={dm}{r}/{dm}${first}*100").number_format = "0.0"
        ws.cell(row=r, column=m2 + 6, value=f"=({dm}{r}/{c5l}{r})/({dm}${first}/{c5l}${first})*100").number_format = "0.0"
        ws.cell(row=r, column=m2 + 7, value=f'=IF({cr}{r}="","",({cr}{r}/{c5l}{r})/({cr}${first}/{c5l}${first})*100)').number_format = "0.0"
        r += 1
    last = r - 1
    dm = gcl(m2 + 1); cr = gcl(m2 + 2); c5l = gcl(c5)
    r += 1
    # Block B: achieved CAGRs
    ws.cell(row=r, column=1, value="B. Achieved revenue-per-US-creative-worker growth (formulas)").font = BOLD; r += 1
    ws.cell(row=r, column=1, value="DM rev per creative worker CAGR FY19-FY25"); ws.cell(row=r, column=2, value=f"=(({dm}{last}/{c5l}{last})/({dm}{first}/{c5l}{first}))^(1/({last}-{first}))-1").number_format = "0.0%"; cagr_dm = r; r += 1
    ws.cell(row=r, column=1, value="Creative rev per creative worker CAGR FY19-FY24"); ws.cell(row=r, column=2, value=f"=(({cr}{last-1}/{c5l}{last-1})/({cr}{first}/{c5l}{first}))^(1/({last-1}-{first}))-1").number_format = "0.0%"; r += 1
    ws.cell(row=r, column=1, value="DM rev per creative worker growth FY24->FY25"); ws.cell(row=r, column=2, value=f"=({dm}{last}/{c5l}{last})/({dm}{last-1}/{c5l}{last-1})-1").number_format = "0.0%"; r += 1
    ws.cell(row=r, column=1, value="Creative5 employment change May-24 -> May-25"); ws.cell(row=r, column=2, value=f"={c5l}{last}/{c5l}{last-1}-1").number_format = "0.0%"; r += 1
    ws.cell(row=r, column=1, value="Graphic designers change May-24 -> May-25"); ws.cell(row=r, column=2, value=f"=B{last}/B{last-1}-1").number_format = "0.0%"; r += 2
    # Block C: scenarios
    ws.cell(row=r, column=1, value="C. Required per-worker growth to sustain target ARR growth under headcount scenarios (formulas)").font = BOLD; r += 1
    ws.cell(row=r, column=1, value="Target ARR growth"); ws.cell(row=r, column=2, value=0.10).font = BLUE; ws.cell(row=r, column=2).number_format = "0.0%"; tgt = r; r += 1
    ws.cell(row=r, column=1, value="Creative5 employment base (May 2025)"); ws.cell(row=r, column=2, value=f"={c5l}{last}"); base = r; r += 1
    hdr(ws, r, ["scenario","annual headcount growth","emp 2026 (f)","emp 2027 (f)","emp 2028 (f)","required per-worker growth (f)","achieved FY19-25 CAGR","gap (achieved - required)"]); r += 1
    sc = read_csv("ws2_seat_compression/data/scenarios.csv")
    rows = [("Flat headcount", 0.0), ("-3%/yr headcount", -0.03), ("-7%/yr headcount", -0.07)]
    if sc is not None:
        for _, rec in sc.iterrows():
            g = _num(rec["annual_emp_growth"])
            if g is not None and not str(rec["scenario"]).startswith("Required"):
                rows.append((str(rec["scenario"]), g))
    for name, g in rows:
        ws.cell(row=r, column=1, value=name)
        ws.cell(row=r, column=2, value=g).font = BLUE; ws.cell(row=r, column=2).number_format = "0.00%"
        for k in range(3):
            ws.cell(row=r, column=3 + k, value=f"=$B${base}*(1+B{r})^{k+1}").number_format = "#,##0"
        ws.cell(row=r, column=6, value=f"=(1+$B${tgt})/(1+B{r})-1").number_format = "0.0%"
        ws.cell(row=r, column=7, value=f"=$B${cagr_dm}").number_format = "0.0%"
        ws.cell(row=r, column=8, value=f"=G{r}-F{r}").number_format = "0.0%"
        r += 1
    r += 1
    # Block D: agency headcount
    ag = read_csv("ws2_seat_compression/data/agency_headcount.csv")
    if ag is not None:
        ws.cell(row=r, column=1, value="D. Advertising holding-company year-end headcount (blue) with 2019=100 index (formula)").font = BOLD; r += 1
        piv = ag.pivot_table(index="year", columns="company", values="employees_year_end", aggfunc="first")
        comps = list(piv.columns)
        hdr(ws, r, ["year"] + comps + [f"{c} idx (f)" for c in comps]); r += 1
        f0 = r
        for y, rec in piv.iterrows():
            ws.cell(row=r, column=1, value=int(y))
            for j, cmp in enumerate(comps):
                ws.cell(row=r, column=2 + j, value=_num(rec[cmp])).font = BLUE
                col = gcl(2 + j)
                ws.cell(row=r, column=2 + len(comps) + j, value=f'=IF({col}{r}="","",{col}{r}/{col}${f0}*100)').number_format = "0.0"
            r += 1
        r += 1
    # Block E: Indeed annual averages
    ind = read_csv("ws2_seat_compression/data/indeed_postings_monthly.csv")
    if ind is not None:
        ws.cell(row=r, column=1, value="E. Indeed Hiring Lab US job postings index (Feb-2020 = 100), monthly (blue); latest month and YoY (formula)").font = BOLD; r += 1
        cols = list(ind.columns)
        hdr(ws, r, cols); r += 1
        f0 = r
        for _, rec in ind.iterrows():
            ws.cell(row=r, column=1, value=str(rec[cols[0]]))
            for j, col in enumerate(cols[1:]):
                ws.cell(row=r, column=2 + j, value=_num(rec[col])).font = BLUE
            r += 1
        l0 = r - 1
        ws.cell(row=r, column=1, value="Latest YoY % (f)")
        for j, col in enumerate(cols[1:]):
            cl = gcl(2 + j)
            ws.cell(row=r, column=2 + j, value=f"={cl}{l0}/{cl}{l0-12}-1").number_format = "0.0%"
        r += 1
    autosize(ws, maxw=40)
def add_task_exposure(wb, ctx):
    read_csv, write_df, hdr, autosize, BLUE, BLACK, BOLD, ROOT = ctx
    ws = wb.create_sheet("TaskExposure")
    ws["A1"] = "WS3: AI task exposure by creative-workflow stage (blue = computed from O*NET + Eloundou labels; black = formula)"; ws["A1"].font = BOLD
    df = read_csv("ws3_task_exposure/data/exposure_by_stage.csv")
    r = 3
    if df is None:
        note(ws, r, "UNAVAILABLE: exposure_by_stage.csv missing"); return
    note(ws, r, "Highly exposed = Eloundou E1 or E2 (gamma). Weights: equal within occupation; occupations by BLS OEWS May 2021 employment. Monetization = analyst ESTIMATE (ws3 data/stage_monetization.csv)."); r += 1
    for scheme, label in [("creative4_emp_weighted", "4 creative occupations (27-1024, 27-1011, 27-1014, 27-4032)"), ("all6_emp_weighted", "All 6 occupations incl. 11-2021 and 13-1161")]:
        sub = df[df["scheme"] == scheme]
        if sub.empty: continue
        ws.cell(row=r, column=1, value=f"Scheme: {label}").font = BOLD; r += 1
        hdr(ws, r, ["stage","monetization","n_tasks","stage_weight_share","share_highly_exposed_human","share_highly_exposed_gpt4","mean_beta_human","exposed_weight_human (formula)","exposed_weight_gpt4 (formula)"]); r += 1
        first = r
        for _, rec in sub.iterrows():
            ws.cell(row=r, column=1, value=rec["stage"]); ws.cell(row=r, column=2, value=rec["monetization_primary"])
            ws.cell(row=r, column=3, value=_num(rec["n_tasks"])).font = BLUE
            ws.cell(row=r, column=4, value=_num(rec["stage_weight_share"])).font = BLUE
            ws.cell(row=r, column=5, value=_num(rec["share_highly_exposed_human"])).font = BLUE
            ws.cell(row=r, column=6, value=_num(rec["share_highly_exposed_gpt4"])).font = BLUE
            ws.cell(row=r, column=7, value=_num(rec["mean_beta_human"])).font = BLUE
            ws.cell(row=r, column=8, value=f"=D{r}*E{r}"); ws.cell(row=r, column=9, value=f"=D{r}*F{r}")
            for c in (4,5,6,8,9): ws.cell(row=r, column=c).number_format = "0.0%"
            r += 1
        last = r - 1
        r += 1
        ws.cell(row=r, column=1, value="Share of highly exposed task weight by monetization model (formulas)").font = BOLD; r += 1
        hdr(ws, r, ["monetization","human-rated share","GPT-4-rated share"]); r += 1
        for m in ["seat","usage","enterprise platform","none/competitor"]:
            ws.cell(row=r, column=1, value=m)
            ws.cell(row=r, column=2, value=f'=SUMIF($B${first}:$B${last},A{r},$H${first}:$H${last})/SUM($H${first}:$H${last})').number_format = "0.0%"
            ws.cell(row=r, column=3, value=f'=SUMIF($B${first}:$B${last},A{r},$I${first}:$I${last})/SUM($I${first}:$I${last})').number_format = "0.0%"
            r += 1
        r += 1
    occ = read_csv("ws3_task_exposure/data/exposure_occupations.csv")
    if occ is not None:
        ws.cell(row=r, column=1, value="Occupation-level exposure scores (Eloundou human/GPT-4 alpha-beta-gamma with percentiles; AIOE overall / image generation / language modeling)").font = BOLD; r += 1
        keep = [c for c in occ.columns if c not in ("source",) and not c.startswith("Unnamed")]
        hdr(ws, r, keep); r += 1
        for _, rec in occ.iterrows():
            for j, col in enumerate(keep):
                v = rec[col]; n = _num(v)
                c = ws.cell(row=r, column=1+j, value=(n if n is not None else (None if (isinstance(v, float) and pd.isna(v)) else v)))
                if n is not None: c.font = BLUE
            r += 1
    autosize(ws, maxw=45)
def add_call_nlp(wb, ctx):
    read_csv, write_df, hdr, autosize, BLUE, BLACK, BOLD, ROOT = ctx
    ws = wb.create_sheet("CallNLP")
    ws["A1"] = "WS4: earnings-call analyst-question analysis and forward P/E (blue = counted/sourced input; black = formula)"; ws["A1"].font = BOLD
    note(ws, 2, "13 of 15 calls from full transcripts (GitHub mirrors); FY25 Q2 and FY26 Q3 reconstructed from search snippets (partial coverage, LOW confidence). Topic labels hand-reviewed (72% agreement with keyword rules).")
    fi = read_csv("ws4_call_nlp/data/fear_index.csv"); pe = read_csv("ws4_call_nlp/data/forward_pe.csv"); vc = read_csv("ws4_call_nlp/data/vocab_counts.csv")
    r = 4
    if fi is None or pe is None:
        note(ws, r, "UNAVAILABLE: ws4 data files missing"); return
    ws.cell(row=r, column=1, value="A. Analyst question counts by topic, fear index (formula) and forward P/E (formula)").font = BOLD; r += 1
    cols = ["call","call_date","n_questions","n_ai_disruption","n_seats_pricing","n_ai_monetization","n_dx","n_margins","n_leadership","n_macro_other","fear_index_strict (f)","fear_index_broad_src","coverage","price_next_day_close","guidance_fy","guide_eps_low","guide_eps_high","guide_eps_mid (f)","forward_pe (f)","guidance_basis","guidance_url"]
    hdr(ws, r, cols); r += 1
    pe_by = {x["call"]: x for _, x in pe.iterrows()}
    first = r
    for _, rec in fi.iterrows():
        p = pe_by.get(rec["call"], {})
        ws.cell(row=r, column=1, value=rec["call"]); ws.cell(row=r, column=2, value=rec["date"])
        for j, col in enumerate(["n_questions","n_ai_disruption","n_seats_pricing","n_ai_monetization","n_dx","n_margins","n_leadership","n_macro_other"]):
            ws.cell(row=r, column=3 + j, value=_num(rec[col])).font = BLUE
        ws.cell(row=r, column=11, value=f"=(D{r}+E{r})/C{r}").number_format = "0.00"
        ws.cell(row=r, column=12, value=_num(rec["fear_index_broad"])).font = BLUE
        ws.cell(row=r, column=13, value=str(rec["coverage"])[:60])
        ws.cell(row=r, column=14, value=_num(p.get("price_next_day_close")) if len(p) else None).font = BLUE
        ws.cell(row=r, column=15, value=p.get("guidance_fy") if len(p) else None)
        ws.cell(row=r, column=16, value=_num(p.get("guide_eps_low")) if len(p) else None).font = BLUE
        ws.cell(row=r, column=17, value=_num(p.get("guide_eps_high")) if len(p) else None).font = BLUE
        ws.cell(row=r, column=18, value=f"=AVERAGE(P{r}:Q{r})").number_format = "0.000"
        ws.cell(row=r, column=19, value=f"=N{r}/R{r}").number_format = "0.0"
        ws.cell(row=r, column=20, value=p.get("guidance_basis") if len(p) else None)
        ws.cell(row=r, column=21, value=p.get("guidance_url") if len(p) else None)
        r += 1
    last = r - 1
    r += 1
    ws.cell(row=r, column=1, value="Correlation(fear index strict, forward P/E), all 15 calls (formula)"); ws.cell(row=r, column=2, value=f"=CORREL(K{first}:K{last},S{first}:S{last})").number_format = "0.00"; r += 1
    ws.cell(row=r, column=1, value="Mean fear index FY23 calls (formula)"); ws.cell(row=r, column=2, value=f"=AVERAGE(K{first}:K{first+3})").number_format = "0.00"; r += 1
    ws.cell(row=r, column=1, value="Mean fear index FY26 calls (formula)"); ws.cell(row=r, column=2, value=f"=AVERAGE(K{last-2}:K{last})").number_format = "0.00"; r += 1
    ws.cell(row=r, column=1, value="Forward P/E change, first to last call (formula)"); ws.cell(row=r, column=2, value=f"=S{last}/S{first}-1").number_format = "0.0%"; r += 2
    if vc is not None:
        ws.cell(row=r, column=1, value="B. Management vocabulary per 10k words: seat vs usage terms (hits in blue; rates and ratio are formulas)").font = BOLD; r += 1
        hdr(ws, r, ["call","date","mgmt_words","seat_hits","usage_hits","seat_per_10k (f)","usage_per_10k (f)","usage_minus_seat (f)","usage_to_seat_ratio (f)","detail"]); r += 1
        for _, rec in vc.iterrows():
            ws.cell(row=r, column=1, value=rec["call"]); ws.cell(row=r, column=2, value=rec["date"])
            ws.cell(row=r, column=3, value=_num(rec["mgmt_words"])).font = BLUE
            ws.cell(row=r, column=4, value=_num(rec["seat_hits"])).font = BLUE
            ws.cell(row=r, column=5, value=_num(rec["usage_hits"])).font = BLUE
            ws.cell(row=r, column=6, value=f"=D{r}/C{r}*10000").number_format = "0.0"
            ws.cell(row=r, column=7, value=f"=E{r}/C{r}*10000").number_format = "0.0"
            ws.cell(row=r, column=8, value=f"=G{r}-F{r}").number_format = "0.0"
            ws.cell(row=r, column=9, value=f'=IF(D{r}=0,"n/a",E{r}/D{r})').number_format = "0.0"
            ws.cell(row=r, column=10, value=str(rec["detail"])[:200])
            r += 1
    autosize(ws, maxw=45)
def add_tabs(wb, name_row, read_csv, write_df, hdr, autosize, BLUE, BLACK, BOLD, ROOT):
    ctx = (read_csv, write_df, hdr, autosize, BLUE, BLACK, BOLD, ROOT)
    for fn in (add_price_volume, add_seat_compression, add_task_exposure, add_call_nlp, add_trends_competitors, add_sources):
        try:
            fn(wb, ctx)
        except Exception as e:
            ws = wb.create_sheet(fn.__name__.replace("add_", "ERR_")[:28])
            ws["A1"] = f"ERROR building tab: {e}"
            print("TAB ERROR", fn.__name__, e)
