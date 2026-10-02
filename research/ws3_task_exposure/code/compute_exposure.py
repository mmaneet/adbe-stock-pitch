"""Occupation-level exposure table, stage-level exposure aggregation, and chart."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
WS="/home/user/adbe-stock-pitch/research/ws3_task_exposure/"
RAW=WS+"data/raw/"
socs=["27-1024.00","27-1011.00","27-1014.00","27-4032.00","11-2021.00","13-1161.00"]

# ---------- 1. occupation-level exposure with percentile ranks ----------
occ=pd.read_csv(RAW+"gpts_occ_level.csv")
for c in ['dv_rating_alpha','dv_rating_beta','dv_rating_gamma','human_rating_alpha','human_rating_beta','human_rating_gamma']:
    occ[c+'_pctile']=occ[c].rank(pct=True)*100
occ['soc6']=occ['O*NET-SOC Code'].str[:7]
aioe=pd.read_excel(RAW+"aioe_AIOE_DataAppendix.xlsx",sheet_name="Appendix A")
ig=pd.read_excel(RAW+"aioe_Image_Generation_AIOE_and_AIIE.xlsx",sheet_name="IG AIOE")
lm=pd.read_excel(RAW+"aioe_Language_Modeling_AIOE_and_AIIE.xlsx",sheet_name="LM AIOE")
aioe.columns=['soc6','aioe_title','AIOE']; ig.columns=['soc6','ig_title','AIOE_image_generation']; lm.columns=['soc6','lm_title','AIOE_language_modeling']
A=aioe.merge(ig[['soc6','AIOE_image_generation']],on='soc6',how='outer').merge(lm[['soc6','AIOE_language_modeling']],on='soc6',how='outer')
for c in ['AIOE','AIOE_image_generation','AIOE_language_modeling']: A[c+'_pctile']=A[c].rank(pct=True)*100
print("AIOE n occupations:",len(A),"| Eloundou n:",len(occ))
E=occ[occ['O*NET-SOC Code'].isin(socs)].merge(A,on='soc6',how='left')
E=E.rename(columns={'O*NET-SOC Code':'onet_soc','Title':'title'})
E['eloundou_source']="openai/GPTs-are-GPTs data/occ_level.csv (commit 2025-10-03/04); percentile among 923 O*NET-SOC occupations"
E['aioe_source']="AIOE-Data/AIOE (last commit 2024-06-03; AIOE 2021 SMJ; IG/LM extensions added 2023); percentile among 774 SOC occupations"
cols=['onet_soc','title','dv_rating_alpha','dv_rating_alpha_pctile','dv_rating_beta','dv_rating_beta_pctile','dv_rating_gamma','dv_rating_gamma_pctile',
      'human_rating_alpha','human_rating_alpha_pctile','human_rating_beta','human_rating_beta_pctile','human_rating_gamma','human_rating_gamma_pctile',
      'AIOE','AIOE_pctile','AIOE_image_generation','AIOE_image_generation_pctile','AIOE_language_modeling','AIOE_language_modeling_pctile','eloundou_source','aioe_source']
E=E[cols].round(3)
E.to_csv(WS+"data/exposure_occupations.csv",index=False)
pd.set_option('display.width',250); pd.set_option('display.max_columns',40)
print(E.drop(columns=['eloundou_source','aioe_source']).to_string())

# ---------- 2. occupation weights: OEWS May 2021 national (repo mirror) ----------
nat=pd.read_csv(RAW+"gpts_national_May2021_dl.csv")
nat=nat[nat.O_GROUP=='detailed'][['OCC_CODE','OCC_TITLE','TOT_EMP']]
nat['TOT_EMP']=nat['TOT_EMP'].astype(str).str.replace(',','').astype(float)
emp=nat.set_index('OCC_CODE')['TOT_EMP']
T=pd.read_csv(WS+"data/task_stage_classification.csv")
T['soc6']=T.onet_soc.str[:7]
T['emp_may2021']=T.soc6.map(emp)
print(T.groupby(['onet_soc','title'])['emp_may2021'].first())
# task weight schemes
T['w_equal_occ']=T['task_weight']                      # equal within occ, occupations equal
T['w_emp']=T['task_weight']*T['emp_may2021']           # equal within occ, occupations by employment
T['w_emp']=T['w_emp']/T['w_emp'].sum()
T['w_emp_core']=T['task_weight_core_sensitivity']*T['emp_may2021']; T['w_emp_core']/=T['w_emp_core'].sum()
T['w_equal_occ']=T['w_equal_occ']/T['w_equal_occ'].sum()
T['alpha_gpt4']=(T.gpt4_exposure=='E1').astype(int); T['alpha_human']=(T.human_labels=='E1').astype(int)

def agg(df,w,stage_col):
    g=df.groupby(stage_col)
    out=pd.DataFrame({
      'n_tasks':g.size(),
      'stage_weight_share':g[w].sum(),
      'share_highly_exposed_human':g.apply(lambda d:(d[w]*d.highly_exposed_human).sum()/d[w].sum()),
      'share_highly_exposed_gpt4':g.apply(lambda d:(d[w]*d.highly_exposed_gpt4).sum()/d[w].sum()),
      'share_E1_direct_human':g.apply(lambda d:(d[w]*d.alpha_human).sum()/d[w].sum()),
      'share_E1_direct_gpt4':g.apply(lambda d:(d[w]*d.alpha_gpt4).sum()/d[w].sum()),
      'mean_beta_human':g.apply(lambda d:(d[w]*d.beta_human).sum()/d[w].sum()),
      'mean_beta_gpt4':g.apply(lambda d:(d[w]*d.beta_gpt4).sum()/d[w].sum()),
    })
    out['share_highly_exposed_avg']=(out.share_highly_exposed_human+out.share_highly_exposed_gpt4)/2
    out['mean_beta_avg']=(out.mean_beta_human+out.mean_beta_gpt4)/2
    return out

MON={  # primary monetization model per stage (see data/stage_monetization.csv)
 'ideation/concepting':'seat','asset generation':'seat','editing/retouching/compositing':'seat','layout/design':'seat',
 'versioning/resizing/localization':'usage','brand compliance/review/approval':'enterprise platform',
 'client/stakeholder communication':'none/competitor','asset management/distribution':'enterprise platform',
 'other: marketing analytics & insight':'enterprise platform','other: marketing strategy & planning':'none/competitor',
 'other: management/admin/physical':'none/competitor'}
ORDER=['ideation/concepting','asset generation','editing/retouching/compositing','layout/design','versioning/resizing/localization',
       'brand compliance/review/approval','client/stakeholder communication','asset management/distribution',
       'other: marketing analytics & insight','other: marketing strategy & planning','other: management/admin/physical']

res=[]
for name,w,df in [("all6_emp_weighted",'w_emp',T),("all6_equal_occ",'w_equal_occ',T),("all6_emp_coreweight",'w_emp_core',T),
                  ("creative4_emp_weighted",'w_emp',T[T.onet_soc.str.startswith('27')]),("creative4_equal_occ",'w_equal_occ',T[T.onet_soc.str.startswith('27')])]:
    d=df.copy(); d[w]=d[w]/d[w].sum()
    a=agg(d,w,'final_substage'); a['scheme']=name; a['monetization_primary']=a.index.map(MON); a.index.name='stage'; res.append(a.reset_index())
R=pd.concat(res); R=R.round(4)
R['stage']=pd.Categorical(R.stage,ORDER,ordered=True); R=R.sort_values(['scheme','stage'])
R.to_csv(WS+"data/exposure_by_stage.csv",index=False)
print(R[R.scheme=='all6_emp_weighted'].to_string()); print(R[R.scheme=='creative4_emp_weighted'].to_string())
# overall by occupation
O=T.groupby(['onet_soc','title']).agg(n=('task_id','size'),human_hi=('highly_exposed_human','mean'),gpt4_hi=('highly_exposed_gpt4','mean'),
    human_E1=('alpha_human','mean'),gpt4_E1=('alpha_gpt4','mean'),beta_h=('beta_human','mean'),beta_g=('beta_gpt4','mean')).round(3)
print(O)
# monetization summary: weight-share of highly-exposed task weight by monetization model (all6, creative4)
for name in ["all6_emp_weighted","creative4_emp_weighted"]:
    r=R[R.scheme==name].copy()
    r['hi_h']=r.stage_weight_share*r.share_highly_exposed_human; r['hi_g']=r.stage_weight_share*r.share_highly_exposed_gpt4
    m=r.groupby('monetization_primary')[['stage_weight_share','hi_h','hi_g']].sum()
    m['share_of_highly_exposed_weight_human']=m.hi_h/m.hi_h.sum(); m['share_of_highly_exposed_weight_gpt4']=m.hi_g/m.hi_g.sum()
    print("\n",name); print(m.round(3))

# ---------- 3. chart ----------
COL={'seat':'#C0392B','usage':'#2A9D8F','enterprise platform':'#1F3A5F','none/competitor':'#7F8C8D'}
r=R[R.scheme=='all6_emp_weighted'].set_index('stage').loc[ORDER]
fig,ax=plt.subplots(figsize=(9,5.6))
y=np.arange(len(ORDER))[::-1]
ax.barh(y,r.share_highly_exposed_human*100,color=[COL[m] for m in r.monetization_primary],height=0.62,label='_nolegend_')
ax.scatter(r.share_highly_exposed_gpt4*100,y,marker='D',s=28,color='black',zorder=3,label='GPT-4-rated share (E1 or E2)')
for yi,(st,row) in zip(y,r.iterrows()):
    ax.text(row.share_highly_exposed_human*100+1 if row.share_highly_exposed_human<0.9 else row.share_highly_exposed_human*100-1,
            yi, f"{row.share_highly_exposed_human*100:.0f}%  (w={row.stage_weight_share*100:.0f}%, n={int(row.n_tasks)})",
            va='center',ha='left' if row.share_highly_exposed_human<0.9 else 'right',fontsize=8,
            color='black' if row.share_highly_exposed_human<0.9 else 'white')
ax.set_yticks(y); ax.set_yticklabels(ORDER,fontsize=9)
ax.set_xlabel("Share of task weight rated highly exposed by human annotators, E1 or E2 (%)")
ax.set_xlim(0,105)
ax.set_title("AI exposure by creative-workflow stage, colored by Adobe monetization model",fontsize=11,loc='left')
for s in ['top','right']: ax.spines[s].set_visible(False)
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
h=[Patch(color=COL[k],label=k) for k in ['seat','usage','enterprise platform','none/competitor']]+[Line2D([0],[0],marker='D',color='black',lw=0,markersize=5,label='GPT-4-rated share (E1 or E2)')]
ax.legend(handles=h,fontsize=8,frameon=False,loc='lower right',title='Bar color = primary Adobe monetization',title_fontsize=8)
fig.text(0.01,0.01,"Source: O*NET 27.2 tasks and Eloundou et al. (2023) labels via openai/GPTs-are-GPTs; 102 tasks, 6 occupations, weighted by BLS OEWS May 2021 employment; stage and monetization mapping = analyst ESTIMATE (ws3).",fontsize=7,color='#7F8C8D')
plt.tight_layout(rect=(0,0.03,1,1)); fig.savefig(WS+"charts/exposure_by_stage.png",dpi=150); print("chart saved")
