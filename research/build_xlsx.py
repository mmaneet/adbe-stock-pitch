"""Build research/ADBE_alt_data.xlsx from workstream outputs.
Conventions: hardcoded sourced inputs in BLUE font; formulas in BLACK; every input row carries a source note.
Run:  . .venv/bin/activate && python research/build_xlsx.py
"""
import os, csv, glob
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.abspath(__file__))
BLUE = Font(color="0000FF")
BLACK = Font(color="000000")
BOLD = Font(bold=True)
HDR_FILL = PatternFill("solid", fgColor="DDE4EE")
TODAY = "2026-10-02"

def hdr(ws, row, labels, col=1):
    for i, l in enumerate(labels):
        c = ws.cell(row=row, column=col + i, value=l)
        c.font = BOLD; c.fill = HDR_FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")

def autosize(ws, maxw=60):
    widths = {}
    for row in ws.iter_rows():
        for c in row:
            if c.value is None: continue
            l = len(str(c.value))
            widths[c.column] = min(maxw, max(widths.get(c.column, 10), l + 2))
    for col, w in widths.items():
        ws.column_dimensions[get_column_letter(col)].width = w

def write_df(ws, df, start_row, start_col=1, blue=True, note=None, title=None):
    """Write a dataframe as a block. Returns (first_data_row, last_data_row, col_map)."""
    r = start_row
    if title:
        ws.cell(row=r, column=start_col, value=title).font = BOLD; r += 1
    if note:
        ws.cell(row=r, column=start_col, value=note).font = Font(italic=True, color="7F8C8D"); r += 1
    hdr(ws, r, list(df.columns), start_col); r += 1
    first = r
    for _, rec in df.iterrows():
        for j, col in enumerate(df.columns):
            v = rec[col]
            if pd.isna(v): v = None
            elif hasattr(v, "item"): v = v.item()
            c = ws.cell(row=r, column=start_col + j, value=v)
            if blue and isinstance(v, (int, float)): c.font = BLUE
        r += 1
    colmap = {col: get_column_letter(start_col + j) for j, col in enumerate(df.columns)}
    return first, r - 1, colmap

def read_csv(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        print("MISSING", rel); return None
    try:
        return pd.read_csv(p)
    except Exception as e:
        print("ERR", rel, e); return None

# ---------------------------------------------------------------- Inputs
INPUTS = [
    # label, value, unit, source, url
    ("Share price (close 2026-10-01)", 241.28, "USD", "Market data via web search (confirmed 2026-10-02)", "https://www.google.com/finance/quote/ADBE:NASDAQ"),
    ("Shares outstanding (10-Q cover, 2026-09-18)", 389.2, "M", "Adobe 10-Q Q3 FY26 cover page", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000156/adbe-20260828.htm"),
    ("Q3 FY26 total revenue", 6760, "USD M", "Adobe Q3 FY26 press release (8-K Ex.99.1), 2026-09-10", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm"),
    ("Q3 FY26 C&MP subscription revenue", 4651, "USD M", "Adobe Q3 FY26 press release / 10-Q", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm"),
    ("Q3 FY25 C&MP subscription revenue (recast)", 4117, "USD M", "Adobe Q3 FY26 10-Q", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000156/adbe-20260828.htm"),
    ("Q3 FY26 BP&C subscription revenue", 1905, "USD M", "Adobe Q3 FY26 press release / 10-Q", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm"),
    ("Q3 FY25 BP&C subscription revenue (recast)", 1648, "USD M", "Adobe Q3 FY26 10-Q", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000156/adbe-20260828.htm"),
    ("9M FY26 C&MP subscription revenue", 13577, "USD M", "Adobe Q3 FY26 10-Q", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000156/adbe-20260828.htm"),
    ("9M FY25 C&MP subscription revenue (recast)", 12058, "USD M", "Adobe Q3 FY26 10-Q", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000156/adbe-20260828.htm"),
    ("9M FY26 BP&C subscription revenue", 5540, "USD M", "Adobe Q3 FY26 10-Q", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000156/adbe-20260828.htm"),
    ("9M FY25 BP&C subscription revenue (recast)", 4777, "USD M", "Adobe Q3 FY26 10-Q", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000156/adbe-20260828.htm"),
    ("FY26 revenue guidance low", 26576, "USD M", "Adobe Q3 FY26 press release targets", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm"),
    ("FY26 revenue guidance high", 26626, "USD M", "Adobe Q3 FY26 press release targets", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm"),
    ("FY26 C&MP guidance low", 18242, "USD M", "Adobe Q3 FY26 press release targets", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm"),
    ("FY26 C&MP guidance high", 18272, "USD M", "Adobe Q3 FY26 press release targets", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm"),
    ("FY26 BP&C guidance low", 7470, "USD M", "Adobe Q3 FY26 press release targets", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm"),
    ("FY26 BP&C guidance high", 7490, "USD M", "Adobe Q3 FY26 press release targets", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm"),
    ("FY26 non-GAAP EPS guidance low", 24.45, "USD", "Adobe Q3 FY26 press release targets", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm"),
    ("FY26 non-GAAP EPS guidance high", 24.50, "USD", "Adobe Q3 FY26 press release targets", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm"),
    ("FY26 ending ARR growth guidance", 0.102, "ratio", "Adobe Q3 FY26 press release targets", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm"),
    ("Beginning FY26 ARR book", 25660, "USD M", "Adobe Q4 FY25 press release / FY26 targets", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm"),
    ("Q3 FY26 ending ARR", 27500, "USD M", "Adobe Q3 FY26 press release", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm"),
    ("Q3 FY26 ending ARR YoY growth", 0.112, "ratio", "Adobe Q3 FY26 press release", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm"),
    ("AI-first ARR (Q3 FY26, >$650M)", 650, "USD M", "Adobe Q3 FY26 press release (floor)", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000147/adbeex991q326.htm"),
    ("FY25 Digital Experience subscription revenue", 5410, "USD M", "Adobe 2026 proxy statement", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000796343&type=DEF+14A"),
    ("Semrush acquisition price", 1870, "USD M", "Adobe 10-Q Q3 FY26 (closed 2026-04-28)", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000156/adbe-20260828.htm"),
    ("9M FY26 operating cash flow", 7646, "USD M", "Adobe 10-Q Q3 FY26 cash flow statement", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000156/adbe-20260828.htm"),
    ("9M FY26 capex", 180, "USD M", "Adobe 10-Q Q3 FY26 cash flow statement", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000156/adbe-20260828.htm"),
    ("9M FY26 stock-based compensation", 1582, "USD M", "Adobe 10-Q Q3 FY26 cash flow statement", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000156/adbe-20260828.htm"),
    ("9M FY26 buybacks", 6880, "USD M", "Adobe 10-Q Q3 FY26 cash flow statement", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000156/adbe-20260828.htm"),
    ("Total debt (current + long-term)", 6363, "USD M", "Adobe 10-Q Q3 FY26 balance sheet", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000156/adbe-20260828.htm"),
    ("Cash + short-term investments", 5639, "USD M", "Adobe 10-Q Q3 FY26 balance sheet", "https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000156/adbe-20260828.htm"),
    ("CC All Apps -> CC Pro NA monthly price, old", 59.99, "USD/mo", "Adobe help: Creative Cloud Pro pricing update (effective 2025-06-17)", "https://helpx.adobe.com/creative-cloud/kb/creative-cloud-pro-plan-pricing-update.html"),
    ("CC All Apps -> CC Pro NA monthly price, new", 69.99, "USD/mo", "Adobe help: Creative Cloud Pro pricing update (effective 2025-06-17)", "https://helpx.adobe.com/creative-cloud/kb/creative-cloud-pro-plan-pricing-update.html"),
    ("Last disclosed CC subscribers (FY2018)", 17, "M", "Adobe FY2018 disclosure", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000796343&type=10-K"),
]

def build():
    wb = Workbook()
    ws = wb.active; ws.title = "Inputs"
    ws["A1"] = "ADBE alt-data workbook - Inputs (blue = hardcoded sourced input; black = formula)"; ws["A1"].font = BOLD
    ws["A2"] = f"Built {TODAY}. All inputs trace to Sources tab. Numbers retrieved via web-search snippets where the primary page was not fetchable; see notes."
    ws["A2"].font = Font(italic=True, color="7F8C8D")
    hdr(ws, 4, ["Input", "Value", "Unit", "Source", "URL"])
    name_row = {}
    r = 5
    for label, val, unit, src, url in INPUTS:
        ws.cell(row=r, column=1, value=label)
        c = ws.cell(row=r, column=2, value=val); c.font = BLUE
        ws.cell(row=r, column=3, value=unit); ws.cell(row=r, column=4, value=src); ws.cell(row=r, column=5, value=url)
        name_row[label] = r; r += 1
    def ref(label): return f"Inputs!$B${name_row[label]}"
    # derived block (formulas, black)
    r += 1
    ws.cell(row=r, column=1, value="Derived (formulas)").font = BOLD; r += 1
    derived = [
        ("Market cap (USD M)", f"={ref('Share price (close 2026-10-01)')}*{ref('Shares outstanding (10-Q cover, 2026-09-18)')}"),
        ("Net debt (USD M)", f"={ref('Total debt (current + long-term)')}-{ref('Cash + short-term investments')}"),
        ("Enterprise value (USD M)", "=B{mc}+B{nd}"),
        ("FY26 non-GAAP EPS midpoint", f"=AVERAGE({ref('FY26 non-GAAP EPS guidance low')},{ref('FY26 non-GAAP EPS guidance high')})"),
        ("P/E on FY26 non-GAAP EPS guide", "=B{px}/B{eps}"),
        ("9M FY26 FCF (OCF - capex, USD M)", f"={ref('9M FY26 operating cash flow')}-{ref('9M FY26 capex')}"),
        ("9M FY26 FCF after SBC (USD M)", "=B{fcf}-" + ref('9M FY26 stock-based compensation')),
        ("Annualized FCF (9M x 4/3, USD M)", "=B{fcf}*4/3"),
        ("EV / annualized FCF", "=B{ev}/B{afcf}"),
        ("FCF yield on market cap (annualized)", "=B{afcf}/B{mc}"),
        ("Q3 FY26 C&MP YoY growth", f"={ref('Q3 FY26 C&MP subscription revenue')}/{ref('Q3 FY25 C&MP subscription revenue (recast)')}-1"),
        ("Q3 FY26 BP&C YoY growth", f"={ref('Q3 FY26 BP&C subscription revenue')}/{ref('Q3 FY25 BP&C subscription revenue (recast)')}-1"),
        ("9M FY26 C&MP YoY growth", f"={ref('9M FY26 C&MP subscription revenue')}/{ref('9M FY25 C&MP subscription revenue (recast)')}-1"),
        ("9M FY26 BP&C YoY growth", f"={ref('9M FY26 BP&C subscription revenue')}/{ref('9M FY25 BP&C subscription revenue (recast)')}-1"),
        ("Implied Q4 FY26 C&MP revenue (guide mid - 9M)", f"=AVERAGE({ref('FY26 C&MP guidance low')},{ref('FY26 C&MP guidance high')})-{ref('9M FY26 C&MP subscription revenue')}"),
        ("Implied FY26 ending ARR (USD M)", f"={ref('Beginning FY26 ARR book')}*(1+{ref('FY26 ending ARR growth guidance')})"),
        ("AI-first ARR as % of Q3 ending ARR", f"={ref('AI-first ARR (Q3 FY26, >$650M)')}/{ref('Q3 FY26 ending ARR')}"),
    ]
    drow = {}
    for label, f in derived:
        drow[label] = r
        ws.cell(row=r, column=1, value=label); r += 1
    fmt = dict(mc=drow["Market cap (USD M)"], nd=drow["Net debt (USD M)"], ev=drow["Enterprise value (USD M)"],
               px=name_row['Share price (close 2026-10-01)'], eps=drow["FY26 non-GAAP EPS midpoint"],
               fcf=drow["9M FY26 FCF (OCF - capex, USD M)"], afcf=drow["Annualized FCF (9M x 4/3, USD M)"])
    for label, f in derived:
        c = ws.cell(row=drow[label], column=2, value=f.format(**fmt)); c.font = BLACK
    autosize(ws)
    return wb, ws, name_row

if __name__ == "__main__":
    wb, ws, name_row = build()
    # workstream tabs are added by integrate() once outputs exist (see bottom of file after subagents finish)
    try:
        from build_xlsx_tabs import add_tabs  # noqa
        add_tabs(wb, name_row, read_csv, write_df, hdr, autosize, BLUE, BLACK, BOLD, ROOT)
    except ImportError:
        print("build_xlsx_tabs not present yet; writing Inputs only")
    out = os.path.join(ROOT, "ADBE_alt_data.xlsx")
    wb.save(out); print("wrote", out)
