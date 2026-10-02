"""Stage classification of O*NET tasks for six occupations.
Step 1: transparent keyword rules (ordered; first matching rule wins).
Step 2: 100% hand review; overrides listed explicitly with reasons.
Outputs data/task_stage_classification.csv and prints agreement rate.
"""
import re, pandas as pd
WS="/home/user/adbe-stock-pitch/research/ws3_task_exposure/"
tasks=pd.read_csv(WS+"data/onet_tasks.csv")
L=pd.read_csv(WS+"data/raw/gpts_full_labelset.tsv",sep="\t",low_memory=False)
L['Task ID']=L['Task ID'].astype(int)
lab=L.set_index('Task ID')[['gpt4_exposure','human_labels','alpha','beta','gamma','gpt4_automation']]
tasks=tasks.join(lab,on='task_id')

# ---------- Ordered keyword rules (regex, case-insensitive). First match wins. ----------
RULES=[
 ("other/management", r"hire|hiring|train|budget|schedul|pricing|negotiat|contract|legal|copyright|trade show|forecast|survey|sales|profit|financial|economic|environment|sustainab|demand|market research|statistics|\bdata\b|competitor|satisfaction|strateg|policies|business case|supervise|coordinate activities|chemicals|fabricat|buying personnel|products or services|product development|product specifications|interviewers|advertising needs|marketplace|promotional"),
 ("asset management/distribution", r"archive|librar|configuration control|catalog|key numbers|time codes|distribut"),
 ("client/stakeholder communication", r"confer|present .*to clients|consult|discuss|collaborate|attend .*conferences|provide management|advise|work with creative directors|screenings"),
 ("brand compliance/review/approval", r"review|approv|proof|conform|standards|specifications|verify|corrections|suggest improvements|ensure"),
 ("ideation/concepting", r"concept|storyboard|sketch|study scripts|plan presentation|research|design solutions|conceptualize|script, plan|story development|approach"),
 ("versioning/resizing/localization", r"resiz|version|adapt|localiz|translat|\bformat|printer|printing|camera-ready|typeset|film negatives"),
 ("editing/retouching/compositing", r"\bedit|\bcut|trim|manipulat|effects|insert|combine|piece sounds|soundtrack|sequence|footage|post-production|music|frames|scenes|composit|retouch|editing"),
 ("layout/design", r"layout|size and arrangement|\btype\b|typography|brochure|presentations|web pages|interfaces"),
 ("asset generation", r"create|generat|draw|produce|illustrat|images|graphics|animat|three-dimensional|record|photograph|modeling|design"),
]
def rule_stage(t):
    for s,rx in RULES:
        if re.search(rx,t,flags=re.I): return s
    return "other/management"
tasks['rule_stage']=tasks['task'].map(rule_stage)

# ---------- Hand review (100% of 102 tasks). Overrides: task_id -> (final_stage, reason) ----------
OVR={
 308:("ideation/concepting","primary action is preparing rough sketches; discussion is secondary"),
 291:("ideation/concepting","developing design solutions with creative director = concepting"),
 284:("layout/design","formulating layout and specifying type/photo/graphic details = layout spec"),
 6887:("asset generation","creating animated sequences with software/hand drawing = generation; script/plan secondary"),
 6890:("layout/design","brochures, presentations, web pages, technical illustrations = document/layout design"),
 312:("brand compliance/review/approval","layout prints are made for supervisor/client review (obsolete prepress task)"),
 310:("versioning/resizing/localization","instructions for final print production = output production stage (ESTIMATE)"),
 4060:("editing/retouching/compositing","reviewing raw footage before assembly is part of the edit, not approval"),
 4070:("editing/retouching/compositing","selecting music passages/developing score = sound editing, collaboration secondary"),
 4055:("editing/retouching/compositing","determining effects/music needed = post-production design decision"),
 4067:("editing/retouching/compositing","post-production models = editing workflow"),
 4072:("editing/retouching/compositing","pacing scenes = editing judgement"),
 4059:("editing/retouching/compositing","programming graphic effects = VFX/compositing"),
 4062:("asset generation","recording/obtaining sounds = sourcing/generating audio assets"),
 962:("other/management","marketing advisory to business groups, outside creative workflow"),
 964:("other/management","consulting buying personnel on product demand, outside creative workflow"),
 19502:("other/management","consulting buying personnel on sustainable products, outside creative workflow"),
 5440:("other/management","analyst presenting research/proposals to management = marketing insight reporting, not creative stakeholder comms"),
 293:("brand compliance/review/approval","attending shoots/press checks to ensure correct output = quality review"),
 15229:("ideation/concepting","researching new software/design concepts = concept research (rule agrees via 'research')"),
 957:("other/management","compiling product/service lists = marketing content ops, outside creative workflow"),
 6893:("other/management","campaign production coordination, budgeting, scheduling = management"),
 299:("ideation/concepting","designs, concepts and sample layouts = concepting (rule agrees)"),
 306:("asset generation","graphics/logos/web graphics creation (rule agrees)"),
 302:("versioning/resizing/localization","prepress assembly of final layouts = output production (ESTIMATE)"),
 295:("versioning/resizing/localization","prepress markup/typesetting instructions = output production (ESTIMATE)"),
 6885:("versioning/resizing/localization","camera-ready art, film negatives, printer's proofs = output production (ESTIMATE)"),
 4061:("editing/retouching/compositing","operating editing/titling/DVE systems to produce final product = editing"),
 4069:("brand compliance/review/approval","screenings for directors/production staff = review/approval session"),
 4056:("asset management/distribution","verifying key numbers/time codes = media logging/asset management"),
 5445:("other/management","directing survey interviewers = research operations"),
 5434:("other/management","research reports = marketing insight, outside creative workflow"),
 289:("client/stakeholder communication","client briefing on objectives/approach = client communication; 'budget' keyword misfired"),
 6889:("asset generation","hand-drawn images for later digitisation = creating source assets"),
 6891:("asset generation","simulating animated object behaviour = animation production, not editing"),
}
# substage for other/management (used to split monetization: analytics vs strategy vs admin)
SUB_ANALYTICS={963,965,958,5433,5435,5436,5437,5438,5439,5441,5442,5443,5444,5445,5434,5440}
SUB_STRATEGY={950,951,20709,962,964,19502,19503,19504,19505,956,957,961,959}
SUB_ADMIN={952,954,955,960,286,290,296,6893,4065,6892}

def final(row):
    if row.task_id in OVR: return OVR[row.task_id][0]
    return row.rule_stage
tasks['final_stage']=tasks.apply(final,axis=1)
tasks['override_reason']=tasks['task_id'].map(lambda i: OVR.get(i,("",""))[1])
def sub(row):
    if row.final_stage!="other/management": return row.final_stage
    if row.task_id in SUB_ANALYTICS: return "other: marketing analytics & insight"
    if row.task_id in SUB_STRATEGY: return "other: marketing strategy & planning"
    if row.task_id in SUB_ADMIN: return "other: management/admin/physical"
    return "other: UNASSIGNED"
tasks['final_substage']=tasks.apply(sub,axis=1)
tasks['hand_reviewed']=True
agree=(tasks.rule_stage==tasks.final_stage).mean()
print(f"Rule vs final agreement: {agree:.1%} ({(tasks.rule_stage==tasks.final_stage).sum()}/{len(tasks)}); hand-checked 100%")
print(tasks.final_substage.value_counts())
print("UNASSIGNED other:", (tasks.final_substage=="other: UNASSIGNED").sum())
# weights: equal within occupation (primary); core/supplemental weight as sensitivity
tasks['task_weight_equal']=1/tasks.groupby('onet_soc')['task_id'].transform('count')
tasks['task_weight_core']=tasks['task_type'].map({'core':2,'supplemental':1}).astype(float)
tasks['task_weight_core']=tasks['task_weight_core']/tasks.groupby('onet_soc')['task_weight_core'].transform('sum')
tasks['highly_exposed_gpt4']=(tasks['gpt4_exposure'].isin(['E1','E2'])).astype(int)
tasks['highly_exposed_human']=(tasks['human_labels'].isin(['E1','E2'])).astype(int)
tasks['beta_gpt4']=tasks['gpt4_exposure'].map({'E0':0,'E1':1,'E2':0.5,'E3':0})
tasks['beta_human']=tasks['human_labels'].map({'E0':0,'E1':1,'E2':0.5,'E3':0})
cols=['onet_soc','title','task_id','task','task_type','rule_stage','final_stage','final_substage','override_reason','hand_reviewed',
      'gpt4_exposure','human_labels','highly_exposed_gpt4','highly_exposed_human','beta_gpt4','beta_human','gpt4_automation','task_weight_equal','task_weight_core']
tasks=tasks.rename(columns={})
tasks[cols].rename(columns={'task_weight_equal':'task_weight'}).assign(task_weight_core_sensitivity=tasks['task_weight_core']).to_csv(WS+"data/task_stage_classification.csv",index=False)
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',110)
print(tasks[['onet_soc','task_id','rule_stage','final_stage','gpt4_exposure','human_labels','task']].to_string())
