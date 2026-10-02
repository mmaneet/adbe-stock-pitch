# WS3 methods: task-level AI exposure by creative-workflow stage vs. Adobe monetization

Analyst: Claude (research subagent) for Maneet; date 2026-10-02; time box ~75 min. All work in `research/ws3_task_exposure/`.
Code: `code/classify_tasks.py` (rules + hand overrides), `code/compute_exposure.py` (tables), `code/chart_exposure.py` (charts).

## 1. Data sources and versions
| Item | Source | Version / date | Notes |
|---|---|---|---|
| O*NET task statements (6 occupations, 102 tasks) | `openai/GPTs-are-GPTs` `data/full_labelset.tsv` and `data/full_onet_data.tsv`, downloaded via raw.githubusercontent.com | Repo last commit 2025-10-04 (occ_level.csv added 2025-10-03); the file has 19,265 task rows, which matches the row count of the O*NET 27.2 `task_statements` table (onetcenter.org dictionary 27.2, seen via WebSearch snippet), so the vintage is O*NET 27.2 (Feb 2023) | onetcenter.org / onetonline.org are blocked here; strategy (a) in the brief succeeded, so (b)/(c) were not needed. Task Type core/supplemental preserved. |
| Eloundou et al. (2023) task-level exposure labels | same file: `gpt4_exposure` (GPT-4 rating, E0/E1/E2), `human_labels` (= `human_exposure_agg`, annotator rating), `alpha/beta/gamma` (derived from the GPT-4 label, verified 100% consistent), `gpt4_automation` (T-scale) | arXiv 2303.10130, March 2023 (v1); repo data June 2024 | Rubric: E0 none; E1 LLM alone cuts task time >=50%; E2 LLM plus additional software (explicitly incl. image generation) cuts time >=50%. |
| Eloundou occupation-level scores | `data/occ_level.csv`: `dv_rating_{alpha,beta,gamma}` (GPT-4) and `human_rating_{alpha,beta,gamma}`; 923 O*NET-SOC occupations | commit 2025-10-03 | alpha = share E1; beta = E1 + 0.5*E2; gamma = E1 + E2. Percentiles computed by me among the 923 occupations. |
| Felten-Raj-Seamans AIOE | `AIOE-Data/AIOE`: `AIOE_DataAppendix.xlsx` sheet "Appendix A" (AIOE, 774 SOC codes); `Image Generation AIOE and AIIE.xlsx` sheet "IG AIOE"; `Language Modeling AIOE and AIIE.xlsx` sheet "LM AIOE" | Repo last commit 2024-06-03; AIOE paper SMJ 2021; generative-AI extensions uploaded Mar-May 2023 | Matched on 6-digit SOC (O*NET code minus ".00"). Percentiles computed by me among 774 occupations. |
| Occupation employment weights | `openai/GPTs-are-GPTs` `data/national_May2021_dl.csv` (BLS OEWS May 2021 national file mirrored in the repo), `TOT_EMP` for the six 6-digit codes | May 2021 | bls.gov is blocked. WebSearch for May 2024 returned only secondary/OOH figures (noted in sources.csv as cross-checks), so the primary, consistent OEWS May 2021 file was used. Equal-occupation weights are reported as a sensitivity in `exposure_by_stage.csv` (schemes `*_equal_occ`). |
| Adobe product/monetization descriptions | helpx.adobe.com generative-credits pages, business.adobe.com Firefly Services and AEM Assets pricing pages, experienceleague.adobe.com Workfront/GenStudio docs, developer.adobe.com Firefly Services docs (all via WebSearch snippets; adobe.com is blocked for fetching) | accessed 2026-10-02 | See `sources.csv`. |

## 2. Steps
1. Downloaded raw files to `data/raw/` (requests, 1 s between calls, UA header per env notes).
2. Extracted the six occupations' tasks (`data/onet_tasks.csv`, 102 rows: 27-1024.00 n=16, 27-1011.00 n=16, 27-1014.00 n=14, 27-4032.00 n=23, 11-2021.00 n=20, 13-1161.00 n=13).
3. Classified each task into a stage with ordered keyword rules (Section 3), then hand-reviewed all 102 tasks (100% hand-checked) and recorded overrides with reasons (`override_reason` column). Agreement rule vs. final: 85.3% (87/102). Both labels saved in `data/task_stage_classification.csv`.
4. Defined exposure metrics (Section 4), computed task weights (Section 5), aggregated by stage (`data/exposure_by_stage.csv`, five weighting schemes), and built the occupation table (`data/exposure_occupations.csv`).
5. Mapped each stage to Adobe products and a primary monetization model (`data/stage_monetization.csv`, every row marked ESTIMATE) and drew `charts/exposure_by_stage.png` (4 creative occupations) and `charts/exposure_by_stage_all6.png` (all six).

## 3. Stage rubric (final labels; applied by hand after the rule pass)
Assign the stage of the task's primary verb/object; if a task spans stages, choose the one where most of the labour sits. Stages:
- **ideation/concepting**: developing concepts, approaches, storyboards, rough sketches, mood/trend research, studying scripts or briefs to plan a presentation.
- **asset generation**: creating new visual/audio material from scratch: illustrations, logos, images, 2D/3D animation, models, graphics, recording or sourcing sounds.
- **editing/retouching/compositing**: modifying existing material: cutting/trimming/sequencing footage, inserting sound/music, manipulating light/colour/texture, VFX, post-production decisions, familiarising with raw footage for the edit.
- **layout/design**: arranging copy, type and images into layouts, documents, brochures, presentations, web pages, interfaces; specifying type and material details.
- **versioning/resizing/localization**: producing final deliverable variants for channels or formats: resizing, adapting, translating, and (because O*NET 27.2 has no modern wording) legacy prepress/output production (camera-ready art, typesetting markup, printer instructions). ESTIMATE: including prepress here is a judgement call; the alternative was asset management/distribution.
- **brand compliance/review/approval**: reviewing proofs/layouts/edits against standards, approving staff work, screenings held for sign-off, attending shoots/press checks to ensure correct output, producing review prints.
- **client/stakeholder communication**: conferring with, presenting to, or briefing clients, directors, producers, department heads about requirements and approaches (where the communication itself is the task).
- **asset management/distribution**: archiving, libraries, configuration control, media logging (key numbers/time codes), distributing assets.
- **other/management**: outside the creative workflow: budgeting, hiring, scheduling, vendor negotiation, legal, physical SFX fabrication, and all marketing strategy/analytics tasks. Sub-split (column `final_substage`) into *marketing analytics & insight*, *marketing strategy & planning*, *management/admin/physical* so the monetization map can distinguish Experience Cloud analytics from unserved tasks.

Keyword rules (regex, case-insensitive, first match wins, in this order): other/management -> asset management -> client communication -> review/approval -> ideation -> versioning -> editing -> layout -> asset generation; unmatched -> other/management. Exact patterns are in `code/classify_tasks.py`. Rule misfires fixed by hand included "budget" catching a client-briefing task (289), "edited" catching hand-drawn source images (6889), and "sequence" catching animation simulation (6891).

## 4. Exposure definitions and thresholds
- **Highly exposed (primary)**: task label is E1 or E2, i.e. Eloundou gamma = 1 (E1 + E2). Reported separately for human annotators (`human_labels`) and GPT-4 (`gpt4_exposure`), plus their average. Threshold chosen because E2 explicitly includes image-generation tools, which is the relevant channel for creative work; alpha (E1 only) is also reported as `share_E1_direct_*` for the stricter "LLM alone" view.
- **Mean exposure**: weighted mean of beta (E1 = 1, E2 = 0.5, E0 = 0), reported as `mean_beta_human`, `mean_beta_gpt4`, `mean_beta_avg`.
- Caution: GPT-4 rated 95-100% of the creative occupations' tasks E2, so the GPT-4 gamma share is near 100% for every creative stage and does not discriminate between stages; the human labels (shown as bars) do. Both are reported.

## 5. Weights
- Eloundou's task file has no importance weight (only `coreweight` 2/1 for core/supplemental and `equalweight`). Primary: equal weight within occupation (`task_weight` = 1/n_tasks). Sensitivity: core=2/supplemental=1 (`task_weight_core_sensitivity`, scheme `all6_emp_coreweight`).
- Occupation weights: BLS OEWS May 2021 national employment (Graphic Designers 204,040; Art Directors 42,080; Special Effects Artists and Animators 20,430; Film and Video Editors 28,030; Marketing Managers 278,690; Market Research Analysts and Marketing Specialists 727,540). Sensitivity: equal occupation weights.
- Stage share of highly exposed weight = sum(w x exposed) / sum(w) within stage; stage weight share = sum(w in stage) / sum(w).
- Because the two marketing occupations hold 77% of the six-occupation employment, the all-six view is dominated by "other" marketing tasks; the main exhibit therefore uses the four creative occupations (69 tasks), with the all-six view as a second chart and in the CSV.

## 6. Monetization map
Primary model per stage from Adobe's public descriptions (sources.csv): per-seat = Creative Cloud apps, Express, Acrobat (generative credits are bundled into seats: CC Pro includes unlimited standard generations plus 4,000 premium credits; Express Premium 250 credits; credits do not roll over); usage = Firefly Services APIs (credits consumed per API call, enterprise contract, no public rate card), Adobe Stock per asset; enterprise platform = Workfront, Frame.io, AEM Assets/Content Hub, GenStudio for Performance Marketing (custom enterprise pricing), Adobe Analytics/CJA/Experience Platform; none/competitor = stages Adobe does not meaningfully serve. Every mapping row is a judgement and is marked ESTIMATE; secondary models are listed per stage.

## 7. Limitations
- Eloundou labels date from early 2023 (GPT-4 launch) and predate major image/video generation progress (Firefly Image 3/4, video models, Sora/Veo-class tools); E2 captured "image generation could help" but not current capability or quality. Treat exposure shares as upper-bound potential, not realised displacement.
- O*NET 27.2 task statements are US-occupation-based, partly dated (prepress, film negatives, videotape), and do not describe modern campaign-variation/localization work, so the usage-monetized stage is thin (4 tasks) and its human-rated exposure (9%) is not evidence that Adobe's API stage is unexposed.
- Occupations, not Adobe customers: O*NET tasks describe US workers in six occupations; Adobe's revenue mix (enterprise vs individual seats) is not observable from this data.
- Stage classification is single-analyst; rule/hand agreement 85%. A second reviewer (Maneet) should spot-check the 15 overrides and the prepress placement.
- GPT-4 labels are near-saturated at E2 for creative tasks; human labels drive the stage ranking.
- AIOE measures ability-level exposure (2021 construction) and is not a task-level measure; used only for occupation context.
- Employment weights are May 2021 (not May 2024) because bls.gov is blocked; weights affect stage weight shares, not within-stage exposure shares (except where stages mix occupations).
