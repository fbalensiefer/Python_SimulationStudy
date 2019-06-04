# -*- coding: utf-8 -*-
###############################################################################
#       Preface
###############################################################################
#%load_ext autoreload
#%reset

# preface loading packages required for Python Data Science
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
filter_cols = 'poptot|popdensity|pminority|pcollege|pincome|medincome|pmortgage|cont_totalbranches|cont_brgrowth|cont_total_origin|cont_NumSBL_Rev1'
df = pd.read_stata('data/mergersample_controls.dta')
index = ['popdensity','poptot','medincome','pminority','pcollege','pmortgage','pincome','cont_totalbranches', 'cont_brgrowth','cont_NumSBL_Rev1','cont_total_origin']
df_t = pd.DataFrame(columns=['Variable', 'Exposed', 'All other', 'p-value 01', 'Control', 'p-value 02'], index=index)
df.drop_duplicates(keep='first', inplace=True)
df_exposed = df.loc[df.overlap==1] 
df_exposed = df_exposed.filter(regex=filter_cols).T
df = pd.read_stata('data/mergersample_controls.dta')
df.drop_duplicates(keep='first', inplace=True)
df_all     = df.loc[df.overlap==0] 
df_all     = df_all.filter(regex=filter_cols).T
df01 = pd.read_stata('data/replication_input.dta')
df01 = df01.filter(regex='state_fps|cnty_fps|tractstring|overlap|mergerID')
df01.drop_duplicates(keep='first', inplace=True)
df02 = pd.read_stata('data/mergersample_controls.dta')
df02.drop_duplicates(keep='first', inplace=True)
df = pd.merge(df01,df02,  on=['state_fps','cnty_fps','tractstring','mergerID'])
df = df.loc[df.overlap_y==0]
#f_control = df.groupby(['state_fps','cnty_fps'], as_index=True)
df_control = df.groupby('state_fps')
df_control = df_control.agg(np.mean)
df_control = df_control.filter(regex=filter_cols).T
df = df.filter(regex=filter_cols)
df_t['Variable']  = list(df)
df_t['Exposed']   = np.round(np.nanmean(df_exposed, axis=1), 3) 
df_t['All other'] = np.round(np.nanmean(df_all, axis=1), 3) 
ptemp = stats.ttest_ind(df_exposed, df_all, axis=1, equal_var=True, nan_policy='omit')
df_t['p-value 01']   = np.round(np.ma.getdata(ptemp[1]), 3)
df_t['Control']   = np.round(np.nanmean(df_control, axis=1), 3)
ptemp = stats.ttest_ind(df_exposed, df_control, axis=1, equal_var=True, nan_policy='omit')
df_t['p-value 02']   = np.round(np.ma.getdata(ptemp[1]), 3)
filter_cols = ['poptot','popdensity','pminority','pcollege','pincome','medincome','pmortgage','cont_totalbranches','cont_brgrowth','cont_total_origin','cont_NumSBL_Rev1']
print(df_t.to_string(index=False))
#print(df_control)
#np.shape(ptemp)

###############################################################################

# todo add standard devidations in brackets
# todo why are there missing values for some variables
# Table 4: Representativeness of the Merger Sample
filter_cols = 'poptot|popdensity|pminority|pcollege|pincome|medincome|pmortgage|cont_totalbranches|cont_brgrowth|cont_total_origin|cont_NumSBL_Rev1'
df = pd.read_stata('data/alltract_controls.dta')
#index = ['popdensity','poptot','medincome','pminority','pcollege','pmortgage','pincome','cont_totalbranches', 'cont_brgrowth','cont_NumSBL_Rev1','cont_total_origin']
index = ['popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'pmortgage', 'totalbranches', 'brgrowth', 'NumSBL_Rev1', 'total_origin', 'pincome', 'num_closings']
df_t = pd.DataFrame(columns=['Variable', 'All', 'Closings', 'Merger'], index=index)
df.drop_duplicates(keep='first', inplace=True)

df_all = df.loc[df['year']>=2002]
df_all = df_all.loc[df_all['year']<=2007]
df_all = df_all.groupby(['state_fps', 'cnty_fps', 'tractstring'])
df_all = df_all.agg(np.max)
df_all = df_all.loc[df_all['totalbranches']>0]
df_all = df_all.agg(np.mean)
alltract_index = 'popdensity|poptot|medincome|pminority|pcollege|pmortgage|totalbranches|brgrowth|NumSBL_Rev1|total_origin|pincome|num_closings'
df_all = df_all.filter(regex=alltract_index)

df_closing = df.loc[df['year']>=2002]
df_closing = df_closing.loc[df_closing['year']<=2007]
df_closing = df_closing.groupby(['state_fps', 'cnty_fps', 'tractstring'])
df_closing = df_closing.agg(np.nanmax)
df_closing = df_closing.loc[df_closing['num_closings']>0]
df_closing = df_closing.agg(np.nanmean)
df_closing = df_closing.filter(regex=alltract_index).T

df = pd.read_stata('data/replication_input.dta')
#df_merger      = df.loc[df['year']==2001]
df_merger = df.loc[df['year']>=2002]
df_merger = df_merger.loc[df_merger['year']<=2007]
df01 = pd.read_stata('data/alltract_controls.dta')
df01.drop_duplicates(keep='first', inplace=True)
df_merger = pd.merge(df_merger,df01,  on=['state_fps','cnty_fps','tractstring'])
df_merger = df_merger.groupby(['state_fps', 'cnty_fps', 'tractstring'])
df_merger = df_merger.agg(np.nanmax)
df_merger = df_merger.agg(np.nanmean)
s = pd.Series(filter_cols)
snew = pd.Series([...])
df_merger.set_index([s, snew])
df_merger = df_merger.filter(regex=filter_cols).T


df_t['Variable']  = list(index)
df_t['All']       = np.round(df_all, 3)
df_t['Closings']  = np.round(df_closing, 3)
df_t['Merger']    = np.round(df_merger, 3)

print(df_t.to_string(index=False))


###############################################################################