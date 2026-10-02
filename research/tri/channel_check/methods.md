# channel_check: methods

Date: 2026-10-02. Host probes: none needed (offline kit; no network used). No git.

## What is here

| File | Purpose |
|---|---|
| survey_A_inhouse_agency.md | 5 Y/N + 2 numeric items, intro script, probes, coding table (in-house / agency leads) |
| survey_B_freelancers_students.md | 5 Y/N items, intro script, probes, coding table (freelancers / students) |
| google_form_questions.md | Exact Google Form text for both (screener, items, types, options, CSV transfer rules) |
| outreach_message.md | Email subject + 2-sentence body, 1-sentence DM, form-link message |
| data/responses_A_template.csv, data/responses_B_template.csv | Headers + two EXAMPLE_ rows each |
| tally_chart.py | Tally + Lennox-style chart |
| charts/channel_check_A_EXAMPLE.png, charts/channel_check_B_EXAMPLE.png | Rendered from the EXAMPLE_ rows only, to prove the pipeline |

## How to run

```
. /home/user/adbe-stock-pitch/.venv/bin/activate
cd /home/user/adbe-stock-pitch/research/tri/channel_check
cp data/responses_A_template.csv data/responses_A.csv   # fill; delete EXAMPLE_ rows or leave them (they are dropped)
python tally_chart.py data/responses_A.csv --survey A \
    --title "Table 1. Creative-ops channel check, October 2026" --out charts/channel_check_A.png
python tally_chart.py data/responses_B.csv --survey B \
    --title "Table 2. Freelancer and student channel check, October 2026" --out charts/channel_check_B.png
```

Flags: `--include-examples` keeps EXAMPLE_ rows and suffixes the title "(EXAMPLE DATA)"; `--month "October 2026"` overrides the source-line month (default: latest `date` in the file); `--wrap 42` sets label wrap width; `--survey` is inferred from `_A`/`_B` in the filename if omitted.
Output: a markdown tally table on stdout ("17/20" style, with n/a counts and what a Yes means), medians of `q2_pct_change` and `q6_headcount_pct` (A), and the PNG.

## Chart conventions (replicating inputs/Maneet_Mehta_YSIG2026Pitch.pdf p. 4, Table 1)

Horizontal stacked bars, one row per question, first question on top, question text wrapped on the left; blue #2F6DB5 = Yes with the count in white inside the segment, grey #BFBFBF = No with the count inside; x-axis 0..n integer ticks labelled "Respondents (n = N)"; legend Yes/No at the bottom, no frame; title at the top; thin figure border; source line "Author's channel check, <month>; small, non-random sample." in small grey text; no top/right spines; white background; 150 dpi. The grey is deliberately neutral (a "No" is absence, not a category), so the dataviz validator flags its chroma; blue vs grey CVD separation passes (Delta E 27) and the counts printed inside segments cover the low-contrast grey.

## Coding and data rules

- Y/N columns accept Yes/No/Y/N (case-insensitive); anything else (Not sure, Undecided, blank) is reported as n/a and excluded from that row's bar, while n in the axis label is the respondent count.
- Numeric columns are signed integers in percent; midpoints for ranges, with the range in `notes`.
- `verbatim` under 25 words, only with consent; no names, no company names, no pricing.
- Survey B has no numeric items, so its CSV omits `q2_pct_change` and `q6_headcount_pct`; the script tolerates either layout.

## Limitations

Small, non-random, self-selected samples reached through the author's network; Yes/No framing loses magnitude (hence the two numeric items in A); respondents may conflate Firefly bundled with seats and paid Adobe AI (Q3 wording and the form's "beyond what is bundled" guard address this). Nothing here is evidence until responses exist.
