import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Patch; from matplotlib.lines import Line2D
WS="/home/user/adbe-stock-pitch/research/ws3_task_exposure/"
R=pd.read_csv(WS+"data/exposure_by_stage.csv")
COL={'seat':'#C0392B','usage':'#2A9D8F','enterprise platform':'#1F3A5F','none/competitor':'#7F8C8D'}
def draw(scheme,fname,title,note):
    r=R[R.scheme==scheme].copy()
    order=[s for s in ['ideation/concepting','asset generation','editing/retouching/compositing','layout/design','versioning/resizing/localization',
       'brand compliance/review/approval','client/stakeholder communication','asset management/distribution',
       'other: marketing analytics & insight','other: marketing strategy & planning','other: management/admin/physical'] if s in set(r.stage)]
    r=r.set_index('stage').loc[order]
    fig,ax=plt.subplots(figsize=(9,6.0))
    y=np.arange(len(order))[::-1]
    ax.barh(y,r.share_highly_exposed_human*100,color=[COL[m] for m in r.monetization_primary],height=0.6)
    ax.scatter(r.share_highly_exposed_gpt4*100,y,marker='|',s=260,color='black',linewidths=2,zorder=3)
    for yi,(st,row) in zip(y,r.iterrows()):
        v=row.share_highly_exposed_human*100
        lab=f"{v:.0f}%  (weight {row.stage_weight_share*100:.0f}%, {int(row.n_tasks)} tasks)"
        if v>=60: ax.text(1.5,yi,lab,va='center',ha='left',fontsize=8,color='white')
        else: ax.text(v+1.5,yi,lab,va='center',ha='left',fontsize=8,color='black')
    ax.set_yticks(y); ax.set_yticklabels(order,fontsize=9)
    ax.set_xlabel("Share of task weight rated highly exposed (E1 or E2) by human annotators, %")
    ax.set_xlim(0,104); ax.set_ylim(-0.7,len(order)-0.3)
    ax.set_title(title,fontsize=11,loc='left')
    for s in ['top','right']: ax.spines[s].set_visible(False)
    h=[Patch(color=COL[k],label=k) for k in ['seat','usage','enterprise platform','none/competitor']]+[Line2D([0],[0],marker='|',color='black',lw=0,markersize=10,markeredgewidth=2,label='GPT-4-rated share (E1 or E2)')]
    ax.legend(handles=h,fontsize=8,frameon=False,loc='upper center',bbox_to_anchor=(0.5,-0.13),ncol=3,title='Bar color = primary Adobe monetization model (analyst ESTIMATE)',title_fontsize=8)
    fig.text(0.01,0.01,"Source: O*NET 27.2 task statements and Eloundou et al. (2023) exposure labels via openai/GPTs-are-GPTs (accessed 2026-10-02).\n"+note+"\nTask weights: equal within occupation, occupations weighted by BLS OEWS May 2021 employment. Stage rubric and monetization map: ws3 methods.md.",fontsize=7,color='#7F8C8D')
    plt.tight_layout(rect=(0,0.10,1,1)); fig.savefig(WS+fname,dpi=150); plt.close(fig); print("saved",fname)
draw("creative4_emp_weighted","charts/exposure_by_stage.png","AI exposure by creative-workflow stage, 4 creative occupations","69 tasks: Graphic Designers, Art Directors, SFX Artists/Animators, Film/Video Editors.")
draw("all6_emp_weighted","charts/exposure_by_stage_all6.png","AI exposure by stage, 4 creative + 2 marketing occupations","102 tasks: 4 creative occupations + Marketing Managers + Market Research Analysts.")
