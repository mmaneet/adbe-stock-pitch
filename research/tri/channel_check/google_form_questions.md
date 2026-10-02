# Google Form text: both surveys

Folder: research/tri/channel_check. Status: KIT ONLY, forms not built or distributed as of 2026-10-02.
Build two separate forms. Settings for both: do not collect email addresses; one response per device off; show progress bar; confirmation message "Thank you. Results are reported only in aggregate." Export responses to Sheets, then paste into the matching CSV template (column order below matches data/responses_*.csv).

---

## Form A: Creative teams, seats and AI (10 questions, about 3 minutes)

**Form title:** How creative teams' work has changed since 2024 (3-minute student survey)

**Form description:** This survey is for a student investment pitch competition on Adobe. It asks five yes/no questions and two rough numbers about your team's creative output, software seats, and AI tools. Nothing confidential is requested: no contract pricing, no client names, no internal financials. Responses are anonymous and reported only in aggregate.

### Section 1: Screener

**S1. I understand this is an anonymous survey for a student investment pitch, that nothing confidential is requested, and that I can stop at any time.** (Required; Multiple choice)
- I agree, continue
- I do not agree (go to: Submit form)

**S2. Which best describes your role?** (Required; Multiple choice; CSV column `role`)
- In-house creative or design lead
- Marketing-ops, creative-ops, or content-operations lead
- Agency producer or project manager
- Agency creative director or art director
- Other (please specify) [short answer]
- None of these; I do not work with a creative team (go to: Submit form)

**S3. Which best describes your organization?** (Required; Multiple choice; CSV column `company_type`)
- Enterprise brand
- Mid-market brand
- Small business or startup
- Agency or studio
- Public sector or non-profit

**S4. How many employees does your organization have?** (Required; Multiple choice; CSV column `size_band`)
- Under 100
- 100 to 999
- 1,000 to 9,999
- 10,000 or more

**S5. Does your team use Adobe Creative Cloud?** (Required; Multiple choice)
- Yes
- No (go to: Submit form)

### Section 2: Questions

**Q1. Has your team's Creative Cloud seat count fallen in the last 2 years?** (Required; Multiple choice; CSV `q1`)
- Yes
- No

**Q1a. If yes, what drove it? (optional)** (Checkboxes)
- Headcount fell
- Downgraded some users to a cheaper plan
- Audit removed unused seats
- Moved some users to Adobe Express or free tools
- Other (please specify) [short answer]

**Q2. Has the number of creative assets your team produces per campaign increased since 2024?** (Required; Multiple choice; CSV `q2`)
- Yes
- No

**Q2a. Approximately what percent change in assets per campaign since 2024? Use a minus sign for a decrease (for example, 40 or -10).** (Short answer; response validation: number; CSV `q2_pct_change`)

**Q3. Do you pay for Adobe AI beyond what is bundled with seats (Firefly credit packs, Firefly Services, GenStudio, an enterprise AI line item)?** (Required; Multiple choice; CSV `q3`)
- Yes
- No
- Not sure (record as blank)

**Q4. Have you replaced any Adobe product with an AI-native tool (Canva, Figma, ChatGPT, Midjourney, or similar), meaning the Adobe product was dropped or its seats cut?** (Required; Multiple choice; CSV `q4`)
- Yes
- No, we use them alongside Adobe
- No, we do not use them

(Both "No" options code as No in `q4`; record the alongside/not-used distinction in `notes`.)

**Q4a. If yes, which Adobe product, and for which task? (optional)** (Short answer; goes to `notes`)

**Q5. Does your organization require commercially safe or indemnified AI for production content?** (Required; Multiple choice; CSV `q5`)
- Yes, written policy
- Yes, in practice
- No
- Not sure (record as blank)

(Both "Yes" options code as Yes in `q5`; record which in `notes`.)

**Q6. Approximately what percent has your team's headcount changed since 2024? Use a minus sign for a decrease (for example, 10 or -15; 0 for no change).** (Required; Short answer; response validation: number; CSV `q6_headcount_pct`)

**Q7. Anything Adobe or a competitor shipped in the last year that changed how your team works? (optional, 25 words or fewer)** (Paragraph; CSV `verbatim`)

---

## Form B: Freelancers and students, Creative Cloud and AI (8 questions, about 2 minutes)

**Form title:** Creative software you pay for and use (2-minute student survey)

**Form description:** This survey is for a student investment pitch competition on Adobe. Five yes/no questions about the creative software you pay for and the AI tools you use. Nothing confidential: no rates, no client names. Responses are anonymous and reported only in aggregate.

### Section 1: Screener

**S1. I understand this is an anonymous survey for a student investment pitch, that nothing confidential is requested, and that I can stop at any time.** (Required; Multiple choice)
- I agree, continue
- I do not agree (go to: Submit form)

**S2. Which best describes you?** (Required; Multiple choice; CSV column `role`)
- Freelance graphic or brand designer
- Freelance illustrator
- Freelance video, motion, or photo
- Design, art, film, or media student (please give your year) [short answer]
- Side-hustle creative alongside a day job
- Other (please specify) [short answer]
- None of these (go to: Submit form)

**S3. Work setup** (Required; Multiple choice; CSV columns `company_type` and `size_band`)
- Solo freelancer (company_type freelance, size_band 1)
- Small studio or collective of 2 to 5 (company_type freelance, size_band 2-5)
- Student (company_type student, size_band 1)
- Side-hustle alongside employment (company_type side-hustle, size_band 1)

**S4. Have you paid for Adobe Creative Cloud at any point in the last 2 years (including a student plan)?** (Required; Multiple choice)
- Yes
- No (go to: Submit form)

### Section 2: Questions

**Q1. Have you cancelled or downgraded Creative Cloud in the last 2 years (for example, All Apps to a single app or Photography plan, or to the free tier)?** (Required; Multiple choice; CSV `q1`)
- Yes
- No

**Q1a. If yes, what prompted it? (optional)** (Checkboxes; goes to `notes`)
- Price
- I was not using it enough
- Another tool covers the work
- Student discount ended
- Other (please specify) [short answer]

**Q2. Do you use Firefly (generative fill, text-to-image, generative credits) in any Adobe app or the Firefly website?** (Required; Multiple choice; CSV `q2`)
- Yes, regularly (weekly or more)
- Yes, occasionally
- No

(Both "Yes" options code as Yes in `q2`; record frequency in `notes`.)

**Q3. Have you moved any paid client work to ChatGPT, Canva, or Midjourney instead of an Adobe app?** (Required; Multiple choice; CSV `q3`)
- Yes
- No

**Q3a. If yes, which task? (optional)** (Short answer; goes to `notes`)

**Q4. Do clients require Adobe file formats (PSD, AI, INDD, or print PDF from InDesign)?** (Required; Multiple choice; CSV `q4`)
- Yes
- No
- I do not have clients yet (record as blank)

**Q5. Do you expect to keep (or re-subscribe to) Creative Cloud next year?** (Required; Multiple choice; CSV `q5`)
- Yes
- No
- Undecided (record as blank)

**Q6. In 25 words or fewer, what would make you drop or keep Creative Cloud? (optional)** (Paragraph; CSV `verbatim`)

---

## Transfer rules (Sheets to CSV)

- `respondent_id`: A001, A002... / B001, B002... in submission order. Delete the EXAMPLE_ rows from the template before pasting.
- `date`: form timestamp, as YYYY-MM-DD.
- `interviewer`: "form" for form responses; the interviewer's name for calls.
- Code "Not sure", "Undecided", and "no clients yet" as blank, never as No; tally_chart.py reports them as n/a.
