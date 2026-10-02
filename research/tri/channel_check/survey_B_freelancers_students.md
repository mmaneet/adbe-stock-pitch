# Survey B: freelancers and students

Folder: research/tri/channel_check. Status: KIT ONLY, no responses collected as of 2026-10-02.
Format: 3-minute Google Form (see google_form_questions.md) or a 5-minute conversation; five yes/no items, one neutral probe each.
Target: 20+ responses. Record in data/responses_B_template.csv (copy it to data/responses_B.csv first).

## 30-second intro script (read verbatim, or use as the form description)

"Thanks for helping. I'm a student preparing an investment pitch on Adobe for a university competition. This is five yes-or-no questions about the creative software you pay for and use; it takes under five minutes. Nothing confidential: no rates, no client names. Answers are anonymous and only reported in aggregate, coded as, for example, 'a freelance illustrator' or 'a second-year design student.' OK to take notes and quote you anonymously?"

## Before the questions: record role, company type, size band

- `role`: freelance designer / freelance illustrator / freelance video or motion / photographer / design or media student (year) / other (specify)
- `company_type`: freelance / student / side-hustle alongside employment
- `size_band`: 1 (solo) / 2-5 (small studio or collective); students record 1

## Questions

**Q1 (Y/N). Have you cancelled or downgraded Creative Cloud in the last 2 years?**
Maps to: concession, individual-subscriber weakness. Downgrade includes moving from All Apps to a single app or the Photography plan, or dropping a paid plan for the free tier.
Probe (neutral): "What prompted that?" (Listen for: price, usage, a substitute tool, student discount ending. Do not lead.)

**Q2 (Y/N). Do you use Firefly (generative fill, text-to-image, generative credits)?**
Maps to: C3 / C4 (Adobe's AI is reaching users and they engage with it). Count Yes for any regular use inside Photoshop, Illustrator, Express, or the Firefly web app.
Probe (neutral): "Roughly how often, and have you ever run out of credits or bought more?"

**Q3 (Y/N). Have you moved any paid work to ChatGPT, Canva, or Midjourney?**
Maps to: C4 falsifier. "Moved" means a task a client pays for is now done in that tool instead of an Adobe app.
Probe (neutral): "Which task, and does the file still pass through an Adobe app before delivery?"

**Q4 (Y/N). Do clients require Adobe file formats (PSD, AI, INDD, PDF from InDesign)?**
Maps to: C1 (revenue sits where Adobe is hard to replace; format lock-in in the professional workflow).
Probe (neutral): "Which formats, and has any client asked for a non-Adobe deliverable such as a Canva or Figma file?"

**Q5 (Y/N). Do you expect to keep Creative Cloud next year?**
Maps to: C4 / concession (retention intent). Students: answer for the year after graduation if that is within 12 months.
Probe (neutral): "What would change that answer?"

Close: one short quote (<25 words) in `verbatim` if permitted.

## Coding note: what SUPPORTS vs WEAKENS the long

| Item | SUPPORTS the long | WEAKENS the long | Neutral / note |
|---|---|---|---|
| Q1 cancelled or downgraded | No | Yes for price or because a substitute covers the work | Yes because the student discount ended, with intent to resubscribe, is neutral |
| Q2 uses Firefly | Yes, regular use; credits exhausted or topped up | No, and generation is done elsewhere | Occasional use is weak support |
| Q3 moved paid work | No; other tools used only for unpaid or exploratory work | Yes, a billed task now lives in ChatGPT/Canva/Midjourney | Falsifier for C4; count strictly |
| Q4 clients require Adobe formats | Yes | No, and clients accept or ask for Canva/Figma deliverables | Students with no clients: leave blank (n/a) |
| Q5 keep Creative Cloud | Yes | No or undecided leaning no | Report undecided as n/a, not No |

Reporting rule: this is the weakest segment for Adobe by design (the concession says individual subscribers are soft), so a poor Q1/Q5 tally confirms the concession rather than breaking the thesis; the thesis-relevant signal is Q3 (work actually leaving) against Q4 (formats keeping it). Report as "x/n", small non-random sample.
