# Survey A: in-house creative / marketing-ops leads and agency producers

Folder: research/tri/channel_check. Status: KIT ONLY, no interviews conducted as of 2026-10-02.
Format: 10-minute call or video; five yes/no items, two numeric items, one neutral probe each.
Target: 10-15 completed interviews. Record every answer in data/responses_A_template.csv (copy it to data/responses_A.csv first).

## 30-second intro script (read verbatim)

"Thanks for making time. I'm a student preparing an investment pitch on Adobe for a university competition. This takes about ten minutes: five yes-or-no questions and two rough numbers about how your team's creative work has changed since 2024. I'm not asking for anything confidential: no contract pricing, no client names, no internal financials. I won't use your name or your company's; you'd be coded as, for example, 'a creative-ops lead at a mid-sized retailer.' Is it OK if I take notes and quote you anonymously?"

If they decline anonymous quotes, leave `verbatim` blank and record only coded answers.

## Before the questions: record role, company type, size band

Say: "First, three quick labels so I can group answers." Record in the CSV:
- `role`: in-house creative lead / marketing-ops or creative-ops lead / agency producer / agency creative director / other (specify)
- `company_type`: enterprise brand / mid-market brand / small business / agency or studio / public sector or non-profit
- `size_band`: employees: <100 / 100-999 / 1,000-9,999 / 10,000+

## Questions (ask in this order; record Yes/No exactly as said, then the probe)

**Q1 (Y/N). Has your team's Creative Cloud seat count fallen in the last 2 years?**
Maps to: concession, seat compression.
Probe (neutral): "What drove that?" (Listen for: headcount, tier downgrade Pro to Standard, seat audit, moving non-designers to Express, shared logins. Do not suggest any of these.)

**Q2 (Y/N). Has the number of creative assets your team produces per campaign increased since 2024?**
Maps to: C2 (AI multiplies content demand).
Numeric follow-up (`q2_pct_change`): "Roughly what percent change, up or down?" Record a signed integer (e.g., 40, -10). If they give a range, record the midpoint and put the range in `notes`.
Probe (neutral): "Where is the extra volume coming from, if any?" (Listen for: channel formats, personalization, AI variants, client asks. Do not lead.)

**Q3 (Y/N). Do you pay for Adobe AI (Firefly credits, Firefly Services, GenStudio)?**
Maps to: C3 (Adobe can charge for AI). Count a Yes only if money changes hands beyond the bundled seat: credit packs, Firefly Services, GenStudio, or an enterprise AI line item.
Probe (neutral): "Who pays for it, and is that line growing, flat, or shrinking?"

**Q4 (Y/N). Have you replaced any Adobe product with an AI-native tool (Canva, Figma, ChatGPT, Midjourney)?**
Maps to: C4 falsifier (users are coming to Adobe). "Replaced" means an Adobe product was dropped or its seats cut because the other tool now does that job; using both is a No, with the complement noted.
Probe (neutral): "Which product, for which task, and is Adobe still used anywhere in that workflow?"

**Q5 (Y/N). Does your organization require commercially safe / indemnified AI for production content?**
Maps to: C3 (indemnified, commercially safe AI is what Adobe sells).
Probe (neutral): "Is that a written policy, legal's preference, or just practice? Does it name any vendor?"

**Q6 (numeric). What is your team's headcount change since 2024, in percent?** (`q6_headcount_pct`)
Record a signed integer. Probe (neutral): "Was any of that linked to AI, budget, or reorganization?" Record the reason in `notes`.

Close: "Anything Adobe or a competitor shipped in the last year that changed your workflow?" Capture one short quote (<25 words) in `verbatim` if permitted. Thank them; offer to share the aggregate tally.

## Coding note: what SUPPORTS vs WEAKENS the long

| Item | SUPPORTS the long | WEAKENS the long | Neutral / note |
|---|---|---|---|
| Q1 seats fell | No; or Yes explained by headcount only (seats track Q6) | Yes with seats falling faster than headcount (audit, downgrade, Express migration) | Compare with Q6 before coding |
| Q2 assets per campaign up | Yes, especially with Q6 flat or down (more output per person) | No, or assets down | Record the % |
| Q3 pays for Adobe AI | Yes, any paid line beyond the seat | No, and AI generation is done in Midjourney/ChatGPT then pasted into Adobe | No with no AI budget anywhere is neutral |
| Q4 replaced Adobe product | No; complements only (Canva for sales decks, Figma for UI Adobe never owned) | Yes: an Adobe product dropped or seats cut for a named tool | This is the C4 falsifier; count strictly |
| Q5 requires indemnified AI | Yes, especially if it names Adobe or excludes consumer tools | No, and consumer AI output ships in production | Yes without any Adobe AI spend (Q3 No) is a lead, not a sale |
| Q6 headcount | Flat or up with Q2 up | Down, attributed to AI productivity, with further cuts planned | Down for budget or reorganization reasons is neutral on the thesis |

Reporting rule: report tallies as "x/n" with n stated, label the sample "small, non-random", and never extrapolate a percentage to Adobe's base. Treat a single strong WEAKENS answer on Q4 as colour, not a finding, unless it repeats across 3+ respondents.
