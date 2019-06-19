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
import statsmodels.formula.api as smf
import statsmodels.api as sm
from patsy import dmatrices
import matplotlib.pyplot as plt
from scipy import stats
from linearmodels import PanelOLS
import econtools.metrics as mt
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

df = pd.read_stata('data/replication_input.dta')
df.drop_duplicates(keep='first', inplace=True)
df=df.assign(event_year=lambda df:df.year-df.yr_approve)
index=list(df)
dfmean = pd.DataFrame(columns=range(-8, 10), index=index)
dfstd = pd.DataFrame(columns=range(-8, 10), index=index)
#df['num_closings']=(df['num_closings']-df['num_closings'].mean())/df['num_closings'].std()
df['num_closings']=(df['num_closings']-df['num_closings'].min())/(df['num_closings'].max()-df['num_closings'].min())
for i in range(-8, 11):
    dfmean[i]=df.loc[(df['event_year']==i) & df['overlap']==1].mean()
    dfstd[i]=df.loc[(df['event_year']==i) & df['overlap']==1].std()
dfmean=dfmean.T
dfstd=dfstd.T
mean=dfmean['num_closings']
std=dfstd['num_closings']
plt.errorbar(mean.index, mean, xerr=0.5, yerr=2*std, linestyle='')
plt.show()  

###############################################################################

# Table 6: First-Stage and Reduced-Form estimates 
df = pd.read_stata('data/replication_input.dta')
df.drop_duplicates(keep='first', inplace=True)
df=df.assign(event_year=lambda df:df.year-df.yr_approve)
index=list(df)
df['group_timeID']= df.groupby(['state_fps', 'cnty_fps', 'year']).grouper.group_info[0]
df['indivID']= df.groupby(['state_fps', 'cnty_fps', 'tractstring']).grouper.group_info[0]
df['clustID']= df.groupby(['state_fps', 'cnty_fps']).grouper.group_info[0] 
df.set_index(['indivID', 'group_timeID'], inplace=True)

## estimates of column 1 (number of closings)
est_numclose= pd.DataFrame(columns=['beta', 'SE'], index=range(-8, 10))
beta=pd.DataFrame(index=range(-8, 10))
std=pd.DataFrame(index=range(-8, 10))
for i in range(-8, 11):
    df['D'] = 0
    df.loc[df['event_year'] >= i , 'D'] = 1
    temp=df.loc[(df['event_year']==i) & df['overlap']==1]
    #temp=df.loc[df['overlap']==1]
    y, x = dmatrices('num_closings ~ D + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=temp)
    model_spec = sm.OLS(y, x)
    #model_spec = mt.reg(temp, temp.num_closings, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], fe_name='indivID', cluster='clustID')
    results = model_spec.fit()
    #results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    #print(results.summary())
    beta[i]=results.params[2]
    std[i]=results.HC0_se[2]
#pd.options.display.float_format = '{:.3f}'.format
est_numclose['beta']=beta.T
est_numclose['SE']=std.T

## estimates of column 2 (total branches)
est_totalbranches= pd.DataFrame(columns=['beta', 'SE'], index=range(-8, 10))
for i in range(-8, 11):
    df['D'] = 0
    df.loc[df['event_year'] >= i , 'D'] = 1
    temp=df.loc[(df['event_year']==i) & df['overlap']==1]
    y, x = dmatrices('totalbranches ~ D + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=temp)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit()
    #results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.totalbranches, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    beta[i]=results.params[2]
    std[i]=results.HC0_se[2]
#pd.options.display.float_format = '{:.3f}'.format
est_totalbranches['beta']=beta.T
est_totalbranches['SE']=std.T

## estimates of column 3 (SBL origin)
est_SBLorigin= pd.DataFrame(columns=['beta', 'SE'], index=range(-8, 10))
for i in range(-8, 11):
    df['D'] = 0
    df.loc[df['event_year'] >= i , 'D'] = 1
    temp=df.loc[(df['event_year']==i) & df['overlap']==1]
    y, x = dmatrices('NumSBL_Rev1 ~ D + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=temp)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit()
    #results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.NumSBL_Rev1, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    beta[i]=results.params[2]
    std[i]=results.HC0_se[2]
#pd.options.display.float_format = '{:.3f}'.format
est_SBLorigin['beta']=beta.T
est_SBLorigin['SE']=std.T

## estimates of column 4 (Mortgage origin)
est_Morigin= pd.DataFrame(columns=['beta', 'SE'], index=range(-8, 10))
for i in range(-8, 11):
    df['D'] = 0
    df.loc[df['event_year'] >= i , 'D'] = 1
    temp=df.loc[(df['event_year']==i) & df['overlap']==1]
    y, x = dmatrices('total_origin ~ D + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=temp)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit()
    #results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    beta[i]=results.params[2]
    std[i]=results.HC0_se[2]
#pd.options.display.float_format = '{:.3f}'.format
est_Morigin['beta']=beta.T
est_Morigin['SE']=std.T

## finish table 6 by producing a df containing all estimates
df_t= pd.DataFrame(columns=['Num_closings', 'Total_branches', 'SBL_origin', 'Mortgage_origin'], index=range(-8, 10))
df_t['Num_closings']      = est_totalbranches['beta']
df_t['Total_branches']    = est_totalbranches['beta']
df_t['SBL_origin']        = est_SBLorigin['beta']
df_t['Mortgage_origin']   = est_Morigin['beta']

###############################################################################

# Figure 3: Exposure to consolidation and local branch levels

df = pd.read_stata('data/replication_input.dta')
df.drop_duplicates(keep='first', inplace=True)
df=df.assign(event_year=lambda df:df.year-df.yr_approve)
index=list(df)
dfmean = pd.DataFrame(columns=range(-8, 10), index=index)
dfstd = pd.DataFrame(columns=range(-8, 10), index=index)
#df['cont_totalbranches']=(df['cont_totalbranches']-df['cont_totalbranches'].mean())/df['cont_totalbranches'].std()
df['cont_totalbranches']=(df['cont_totalbranches']-df['cont_totalbranches'].min())/(df['cont_totalbranches'].max()-df['cont_totalbranches'].min())
for i in range(-8, 11):
    dfmean[i]=df.loc[(df['event_year']==i) & df['overlap']==1].mean()
    dfstd[i]=df.loc[(df['event_year']==i) & df['overlap']==1].std()
dfmean=dfmean.T
dfstd=dfstd.T
mean=dfmean['cont_totalbranches']
std=dfstd['cont_totalbranches']
plt.errorbar(mean.index, mean, xerr=0.5, yerr=2*std, linestyle='')
plt.show()  

###############################################################################

# Figure 4: Exposure to consolidation and the volume of new lending

## Small Business Lending
df = pd.read_stata('data/replication_input.dta')
df.drop_duplicates(keep='first', inplace=True)
df=df.assign(event_year=lambda df:df.year-df.yr_approve)
index=list(df)
dfmean = pd.DataFrame(columns=range(-8, 10), index=index)
dfstd = pd.DataFrame(columns=range(-8, 10), index=index)
#df['NumSBL_Rev1']=(df['NumSBL_Rev1']-df['NumSBL_Rev1'].mean())/df['NumSBL_Rev1'].std()
df['NumSBL_Rev1']=(df['NumSBL_Rev1']-df['NumSBL_Rev1'].min())/(df['NumSBL_Rev1'].max()-df['NumSBL_Rev1'].min())
for i in range(-8, 11):
    dfmean[i]=df.loc[(df['event_year']==i) & df['overlap']==1].mean()
    dfstd[i]=df.loc[(df['event_year']==i) & df['overlap']==1].std()
dfmean=dfmean.T
dfstd=dfstd.T
mean=dfmean['NumSBL_Rev1']
std=dfstd['NumSBL_Rev1']
plt.errorbar(mean.index, mean, xerr=0.5, yerr=2*std, linestyle='')
plt.show() 

## Mortgages
df = pd.read_stata('data/replication_input.dta')
df.drop_duplicates(keep='first', inplace=True)
df=df.assign(event_year=lambda df:df.year-df.yr_approve)
index=list(df)
dfmean = pd.DataFrame(columns=range(-8, 10), index=index)
dfstd = pd.DataFrame(columns=range(-8, 10), index=index)
#df['total_origin']=(df['total_origin']-df['total_origin'].mean())/df['total_origin'].std()
df['total_origin']=(df['total_origin']-df['total_origin'].min())/(df['total_origin'].max()-df['total_origin'].min())
for i in range(-8, 11):
    dfmean[i]=df.loc[(df['event_year']==i) & df['overlap']==1].mean()
    dfstd[i]=df.loc[(df['event_year']==i) & df['overlap']==1].std()
dfmean=dfmean.T
dfstd=dfstd.T
mean=dfmean['total_origin']
std=dfstd['total_origin']
plt.errorbar(mean.index, mean, xerr=0.5, yerr=2*std, linestyle='')
plt.show() 

###############################################################################

# Figure 5: The effect of subsequent bank entry on local credit supply
plt.figure()

## Small Business Lending
df = pd.read_stata('data/replication_input.dta')
df.drop_duplicates(keep='first', inplace=True)
df=df.assign(event_year=lambda df:df.year-df.yr_approve)
index=list(df)
dfmean = pd.DataFrame(columns=range(-8, 10), index=index)
#df['NumSBL_Rev1']=(df['NumSBL_Rev1']-df['NumSBL_Rev1'].mean())/df['NumSBL_Rev1'].std()
df['NumSBL_Rev1']=(df['NumSBL_Rev1']-df['NumSBL_Rev1'].min())/(df['NumSBL_Rev1'].max()-df['NumSBL_Rev1'].min())
df['totalbranches']=(df['totalbranches']-df['totalbranches'].min())/(df['totalbranches'].max()-df['totalbranches'].min())
for i in range(-8, 11):
    dfmean[i]=df.loc[(df['event_year']==i) & df['overlap']==1].mean()
dfmean=dfmean.T
mean=dfmean['NumSBL_Rev1']
plt.subplot(2,2,1)
plt.scatter(mean.index, mean)
plt.subplot(2,2,1)
plt.scatter(mean.index, dfmean['totalbranches'])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15))
plt.title('New Small Business loans')
#plt.show() 

## Mortgages
df = pd.read_stata('data/replication_input.dta')
df.drop_duplicates(keep='first', inplace=True)
df=df.assign(event_year=lambda df:df.year-df.yr_approve)
index=list(df)
dfmean = pd.DataFrame(columns=range(-8, 10), index=index)
#df['total_origin']=(df['total_origin']-df['total_origin'].mean())/df['total_origin'].std()
df['total_origin']=(df['total_origin']-df['total_origin'].min())/(df['total_origin'].max()-df['total_origin'].min())
df['totalbranches']=(df['totalbranches']-df['totalbranches'].min())/(df['totalbranches'].max()-df['totalbranches'].min())
for i in range(-8, 11):
    dfmean[i]=df.loc[(df['event_year']==i) & df['overlap']==1].mean()
dfmean=dfmean.T
mean=dfmean['total_origin']
plt.subplot(2,2,2)
plt.scatter(mean.index, mean)
plt.subplot(2,2,2)
plt.scatter(mean.index, dfmean['totalbranches'])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15))
plt.title('New Mortgages')
#plt.show() 

###############################################################################

# Table 7: IV-Estimates of the effect of closings an local credit supply
df = pd.read_stata('data/replication_input.dta')
df.drop_duplicates(keep='first', inplace=True)
df=df.assign(event_year=lambda df:df.year-df.yr_approve)
index=list(df)
df['close_2yr']=0
df['close_2yr']=df['closed_branch'].loc[(df.event_year==0) | (df.event_year==1)]
df['close_2yr'].fillna(0, inplace=True)
df['POST']=df['event_year'].loc[df.event_year>0]
df['POST_close']=df.POST * df.close_2yr
df['POST_expose']= df.POST * df.overlap 

df['group_timeID']= df.groupby(['state_fps', 'cnty_fps', 'year']).grouper.group_info[0]
df['indivID']= df.groupby(['state_fps', 'cnty_fps', 'tractstring']).grouper.group_info[0]
df['clustID']= df.groupby(['state_fps', 'cnty_fps']).grouper.group_info[0] 
df.set_index(['indivID', 'group_timeID'], inplace=True)

#################################################################################

## OLS
# NumSBL_Rev1
y, x = dmatrices('NumSBL_Rev1 ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
mod = PanelOLS(y, x, entity_effects=True)
results = mod.fit(cov_type='clustered', other_effects=['indivID', 'group_timeID'])
print(results.summary())

#################################################################################

## OLS
    # NumSBL_Rev1
    y, x = dmatrices('NumSBL_Rev1 ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
    model_spec = sm.OLS(mod)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = mt.reg(temp, temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], fe_name=['indivID', 'group_timeID'], cluster='clustID')
    #results = model_spec.fit()
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # AmtSBL_Rev1
    y, x = dmatrices('AmtSBL_Rev1 ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # total_origin
    y, x = dmatrices('total_origin ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # loan_amount
    y, x = dmatrices('loan_amount ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())    
    
## Reduced Form
    # NumSBL_Rev1
    y, x = dmatrices('total_origin ~ POST_expose + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # AmtSBL_Rev1
    y, x = dmatrices('AmtSBL_Rev1 ~ POST_expose + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # total_origin
    y, x = dmatrices('total_origin ~ POST_expose + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # loan_amount
    y, x = dmatrices('loan_amount ~ POST_expose + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())
    
## IV ESTIMATION
    # NumSBL_Rev1 - IV2SLS.from_formula()
    y, x = dmatrices('NumSBL_Rev1 ~ popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + [POST_close ~ POST_expose]', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # AmtSBL_Rev1
    y, x = dmatrices('AmtSBL_Rev1 ~ popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + [POST_close ~ POST_expose]', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # total_origin
    y, x = dmatrices('total_origin ~ popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + [POST_close ~ POST_expose]', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # loan_amount
    y, x = dmatrices('loan_amount ~ popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + [POST_close ~ POST_expose]', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())


###############################################################################
### Remaining Part is not relevant for further analysis
###############################################################################

# Resampling to control for overrepresentation in the sample
# (Idea: banks concentrade their closings in areas deemed to be "over-branched")
# Resample tracts across counties and states to test for robustness of the results

# Table 7 - Resampled: IV-Estimates of the effect of closings an local credit supply
df = pd.read_stata('data/replication_input.dta')
df.drop_duplicates(keep='first', inplace=True)
df=df.assign(event_year=lambda df:df.year-df.yr_approve)
index=list(df)
df['close_2yr']=0
df['close_2yr']=df['closed_branch'].loc[(df.event_year==0) | (df.event_year==1)]
df['close_2yr'].fillna(0, inplace=True)
df['POST']=df['event_year'].loc[df.event_year>0]
df['POST_close']=df.POST * df.close_2yr
df['POST_expose']= df.POST * df.overlap 

df['group_timeID']= df.groupby(['state_fps', 'cnty_fps', 'year']).grouper.group_info[0]
df['indivID']= df.groupby(['state_fps', 'cnty_fps', 'tractstring']).grouper.group_info[0]
df['clustID']= df.groupby(['state_fps', 'cnty_fps']).grouper.group_info[0] 
df.set_index(['indivID', 'group_timeID'], inplace=True)

#df = (df.set_index('indivID').reindex(range(df.indivID.min(), df.indivID.max())).interpolate().reset_index())

## OLS
    # NumSBL_Rev1
    y, x = dmatrices('NumSBL_Rev1 ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = mt.reg(temp, temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], fe_name=['indivID', 'group_timeID'], cluster='clustID')
    #results = model_spec.fit()
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # AmtSBL_Rev1
    y, x = dmatrices('AmtSBL_Rev1 ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # total_origin
    y, x = dmatrices('total_origin ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # loan_amount
    y, x = dmatrices('loan_amount ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())    
    
## Reduced Form
    # NumSBL_Rev1
    y, x = dmatrices('total_origin ~ POST_expose + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # AmtSBL_Rev1
    y, x = dmatrices('AmtSBL_Rev1 ~ POST_expose + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # total_origin
    y, x = dmatrices('total_origin ~ POST_expose + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # loan_amount
    y, x = dmatrices('loan_amount ~ POST_expose + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())
    
## IV ESTIMATION
    # NumSBL_Rev1 - IV2SLS.from_formula()
    y, x = dmatrices('NumSBL_Rev1 ~ popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + [POST_close ~ POST_expose]', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # AmtSBL_Rev1
    y, x = dmatrices('AmtSBL_Rev1 ~ popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + [POST_close ~ POST_expose]', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # total_origin
    y, x = dmatrices('total_origin ~ popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + [POST_close ~ POST_expose]', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())

    # loan_amount
    y, x = dmatrices('loan_amount ~ popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + [POST_close ~ POST_expose]', data=df)
    model_spec = sm.OLS(y, x)
    results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
    #model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
    #results = model_spec.fit(cov_type='clustered', cluster_entity=True)
    print(results.summary())
