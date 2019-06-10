# -*- coding: utf-8 -*-
###############################################################################
#       Preface
###############################################################################
#%load_ext autoreload
#%reset

# preface loading packages required for Python Data Science
%reset -f
%clear
import numpy as np
import pandas as pd
import statsmodels.api as sm
from patsy import dmatrices
import matplotlib.pyplot as plt
from scipy import stats
#%matplotlib inline

###############################################################################
###         Summary Stats
###############################################################################
# Table 1: Merger Sample
df = pd.read_stata('data/replication_input.dta')
df = df[['acq_instname', 'out_instname', 'yr_approve', 'approved']]
df.drop_duplicates(keep='first', inplace=True)
df = df.sort_values(by='approved')
df = df[['acq_instname', 'out_instname', 'yr_approve']]
pd.options.display.float_format = '{:.0f}'.format
df = df.rename(index=str , columns={'acq_instname':'Buyer', 'out_instname':'Target', 'yr_approve':'Year approved'})
print(df.to_string(index=False))

###############################################################################

# Table 2: Merger Sammary Statistics
df = pd.read_stata('data/replication_input.dta')
df = df.filter(regex='mergerID|premerger_acq|premerger_out')
df.drop_duplicates(keep='first', inplace=True)
df_t = pd.DataFrame(columns=['Variable', 'Median', 'Min', 'Max'])
df = df.filter(regex='premerger_acq|premerger_out')
df_t['Variable'] = ['Total assets', 'Branches', 'States of operation', 'Countries of operation', 'Total assets', 'Branches', 'States of operation', 'Countries of operation']
df_t['Median']   = np.round(np.median(df, axis=0))
df_t['Min']      = np.round(np.nanmin(df, axis=0))
df_t['Max']      = np.round(np.nanmax(df, axis=0))
print(df_t.to_string(index=False))
#np.round(df.describe(percentiles=[.5]), 1).T # we only need min, 50% (median), max


###############################################################################

# todo check why df_control differs
# todo add standard devidations in brackets
# Table 3: Summary Statistics for Exposed and Control Tracts
#df.assign(cntyID = df.sort_values(['state_fps', 'cnty_fps']))
filter_cols = 'poptot|popdensity|pminority|pcollege|pincome|medincome|pmortgage|cont_totalbranches|cont_brgrowth|cont_total_origin|cont_NumSBL_Rev1|Obs'
df = pd.read_stata('data/mergersample_controls.dta')
index = ['popdensity','poptot','medincome','pminority','pcollege','pmortgage','pincome','cont_totalbranches', 'cont_brgrowth','cont_NumSBL_Rev1','cont_total_origin']
df_t = pd.DataFrame(columns=['Variable', 'Exposed', 'All other', 'p-value 01', 'Control', 'p-value 02'], index=index)
df.drop_duplicates(keep='first', inplace=True)
df_exposed = df.loc[df.overlap==1]
df_exposed=df_exposed.assign(Obs=lambda df_exposed:len(df_exposed))
df_exposed = df_exposed.filter(regex=filter_cols).T
df = pd.read_stata('data/mergersample_controls.dta')
df.drop_duplicates(keep='first', inplace=True)
df_all     = df.loc[df.overlap==0]
df_all=df_all.assign(Obs=lambda df_all:len(df_all))
df_all     = df_all.filter(regex=filter_cols).T
df01 = pd.read_stata('data/replication_input.dta')
df01 = df01.filter(regex='state_fps|cnty_fps|tractstring|overlap|mergerID')
df01.drop_duplicates(keep='first', inplace=True)
df02 = pd.read_stata('data/mergersample_controls.dta')
df02.drop_duplicates(keep='first', inplace=True)
#df = pd.merge(df01,df02,  on=['state_fps','cnty_fps','tractstring','mergerID'], how='inner', suffixes=('', '_y'))
df = pd.merge(df01,df02,  on=['state_fps','cnty_fps','tractstring','mergerID'], how='inner')
df = df.loc[df.overlap_y==0]
df_control = df.groupby(['state_fps','cnty_fps'], as_index=True)
#df_control = df.groupby('state_fps')
df_control = df_control.agg(np.mean)
df_control = df.assign(Obs=lambda df:len(df))
df_control = df_control.filter(regex=filter_cols).T
df = df.filter(regex=filter_cols)
df_t['Variable']  = list(df)
df_t              = df_t.append({'Variable':'Obs'}, ignore_index=True)
df_t['Exposed']   = np.round(np.nanmean(df_exposed, axis=1), 3)
df_t['All other'] = np.round(np.nanmean(df_all, axis=1), 3)
ptemp = stats.ttest_ind(df_exposed, df_all, axis=1, equal_var=True, nan_policy='omit')
df_t['p-value 01']   = np.round(np.ma.getdata(ptemp[1]), 3)
df_t['Control']   = np.round(np.nanmean(df_control, axis=1), 3)
ptemp = stats.ttest_ind(df_exposed, df_control, axis=1, equal_var=True, nan_policy='omit')
df_t['p-value 02']   = np.round(np.ma.getdata(ptemp[1]), 3)
filter_cols = ['poptot','popdensity','pminority','pcollege','pincome','medincome','pmortgage','cont_totalbranches','cont_brgrowth','cont_total_origin','cont_NumSBL_Rev1']
pd.options.display.float_format = '{:.3f}'.format
print(df_t.to_string(index=False))
#print(df_control)
#np.shape(ptemp)

###############################################################################

# todo add standard devidations in brackets
# Table 4: Representativeness of the Merger Sample
filter_cols = 'poptot|popdensity|pminority|pcollege|pincome|medincome|pmortgage|cont_totalbranches|cont_brgrowth|cont_total_origin|cont_NumSBL_Rev1|Obs'
df = pd.read_stata('data/alltract_controls.dta')
#index = ['popdensity','poptot','medincome','pminority','pcollege','pmortgage','pincome','cont_totalbranches', 'cont_brgrowth','cont_NumSBL_Rev1','cont_total_origin']
index = ['popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'pmortgage', 'totalbranches', 'brgrowth', 'NumSBL_Rev1', 'total_origin', 'pincome', 'Obs']
df_t = pd.DataFrame(columns=['Variable', 'All', 'Closings', 'Merger'], index=index)
df.drop_duplicates(keep='first', inplace=True)

df_all = df.loc[df['year']>=2002]
df_all = df_all.loc[df_all['year']<=2007]
df_all = df_all.groupby(['state_fps', 'cnty_fps', 'tractstring'])
df_all = df_all.agg(np.nanmax)
#df_all = df_all.agg(np.nanmean)
df_all = df_all.loc[df_all['totalbranches']>0]
df_all['Obs'] = len(df_all)
df_all = df_all.agg(np.nanmean)
alltract_index = 'popdensity|poptot|medincome|pminority|pcollege|pmortgage|totalbranches|brgrowth|NumSBL_Rev1|total_origin|pincome|Obs'
df_all = df_all.filter(regex=alltract_index)

df_closing = df.loc[df['year']>=2002]
df_closing = df_closing.loc[df_closing['year']<=2007]
df_closing = df_closing.groupby(['state_fps', 'cnty_fps', 'tractstring'])
df_closing = df_closing.agg(np.nanmax)
df_closing = df_closing.loc[df_closing['num_closings']>0]
df_closing['Obs'] = len(df_closing)
df_closing = df_closing.agg(np.nanmean)
df_closing = df_closing.filter(regex=alltract_index).T

df = pd.read_stata('data/replication_input.dta')
#df_merger      = df.loc[df['year']==2001]
df_merger = df.loc[df['year']>=2002]
df_merger = df_merger.loc[df_merger['year']<=2007]
df01 = pd.read_stata('data/alltract_controls.dta')
df01.drop_duplicates(keep='first', inplace=True)
df_merger = pd.merge(df_merger,df01,  on=['state_fps','cnty_fps','tractstring'], how='inner', suffixes=('', '_y'))
df_merger = df_merger.groupby(['state_fps', 'cnty_fps', 'tractstring'])
df_merger = df_merger.agg(np.nanmax)
num= len(df_merger)
df_merger = df_merger.agg(np.nanmean)
df_merger.rename(index= {'cont_totalbranches': 'totalbranches', 'cont_brgrowth':'brgrowth', 'cont_NumSBL_Rev1':'NumSBL_Rev1','cont_total_origin':'total_origin'},  inplace = True)
df_merger = df_merger.filter(regex=alltract_index).T
df_merger = df_merger.iloc[4:15]
df_merger['Obs'] = num

df_t['Variable']  = list(index)
df_t['All']       = np.round(df_all, 3)
df_t['Closings']  = np.round(df_closing, 3)
df_t['Merger']    = np.round(df_merger, 3)

pd.options.display.float_format = '{:.3f}'.format
print(df_t.to_string(index=False))

###############################################################################

# Table 5: Complier Characteristics

## calculating MEDIAN values
df = pd.read_stata('data/replication_input.dta')
index = ['popdensity','poptot','medincome','pminority','pcollege','pmortgage','pincome','cont_totalbranches', 'cont_brgrowth','cont_NumSBL_Rev1','cont_total_origin']
df.drop_duplicates(keep='first', inplace=True)
df=df.assign(event_year=lambda df:df.year-df.yr_approve)
df=df.loc[df['event_year']==1]
p50=df[index].median()

## estimate the proportion of ALWAYS TAKERS, NEVER TAKERS and COMPLIERS
df_at = df.loc[df['overlap']==0]
p_always = np.nanmean(df_at.closed_branch)
df_nt = df.assign(temp=lambda df:1-df.closed_branch)
df_nt = df_nt.loc[df_nt['overlap']==1]
p_never = np.nanmean(df_nt.temp)
p_comp=1-p_always-p_never

## ESTIMATE AVERAGE CHARACTERISTICS OVER SET OF ALWAYS TAKERS AND COMPLIERS COMBINED (i.e.,Treatment tracts who had closings)
df_t1 = pd.DataFrame(index=index)
df_atcomp = df.loc[df['overlap']==1]
df_atcomp = df_atcomp.loc[df_atcomp['closed_branch']==1]
n=len(df_atcomp)
for i in index:
    temp=df_atcomp[df_atcomp[i]>p50[i]].count()
    df_t1[i]=temp/n
df_t1=df_t1.T
df_atcomp=df_t1['poptot']

## ESTIMATE AVERAGE CHARACTERISTICS OVER ALWAYS TAKERS ONLY (i.e., Control tracts who had closings)
df_t2 = pd.DataFrame(index=index)
df_at = df.loc[df['overlap']==0]
df_at = df_at.loc[df_at['closed_branch']==1]
n=len(df_at)
for i in index:
    temp=df_at[df_at[i]>p50[i]].count()
    df_t2[i]=temp/n
df_t2=df_t2.T
df_at=df_t2['poptot']

##  ESTIMATE AVERAGE CHARACTERISTICS FOR COMPLIERS
ecomp=((p_always+p_comp)/p_comp)*(df_atcomp-((p_always/(p_always+p_comp))*df_at))
## CALCULATE RATIO
ratio=ecomp/0.5
## PRINT to Table
df_tab = pd.DataFrame(columns=['Variables','ecomp','ratio'], index=index)
df_tab['Variables']=list(df[index])
df_tab['ecomp']=ecomp*100
df_tab['ratio']=ratio
pd.options.display.float_format = '{:.3f}'.format
print(df_tab.to_string(index=False))

###############################################################################
###         Main Results
###############################################################################

# Figure 2: Exposure to consolidation and the incidence of branch closings

###############################################################################

# Table 6: First-Stage and Reduced-Form estimates 

###############################################################################

# Figure 3: Exposure to consolidation and local branch levels

###############################################################################

# Figure 4: Exposure to consolidation and the volume of new lending

###############################################################################

# (maybe skip Figure 5)

###############################################################################

# Table 7: IV-Estimates of the effect of closings an local credit supply

###############################################################################
### Remaining Part is not relevant for further analysis
###############################################################################