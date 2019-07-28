# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 19:52:15 2019

@author: fabia
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
from patsy import dmatrices
import matplotlib.pyplot as plt
from scipy import stats
import warnings
from linearmodels import PanelOLS

np.random.seed(123)

#df.assign(cntyID = df.sort_values(['state_fps', 'cnty_fps']))
filter_cols = 'poptot|popdensity|pminority|pcollege|pincome|medincome|pmortgage|cont_totalbranches|cont_brgrowth|cont_total_origin|cont_NumSBL_Rev1|Obs'
df = pd.read_stata('data/mergersample_controls.dta')
index = ['popdensity','poptot','medincome','pminority','pcollege','pmortgage','pincome','cont_totalbranches', 'cont_brgrowth','cont_NumSBL_Rev1','cont_total_origin','Obs']
df_t = pd.DataFrame(columns=['Variable', 'Exposed', 'Allother', 'pvalue01', 'Control', 'pvalue02'], index=index)
std = pd.DataFrame(columns=['a','b','c'], index=index)
df.drop_duplicates(keep='first', inplace=True)
df_exposed = df.loc[df.overlap==1]
df_exposed=df_exposed.assign(Obs=lambda df_exposed:len(df_exposed))
df_exposed = df_exposed.filter(regex=filter_cols).T
std['a']=np.std(df_exposed, axis=1)
df = pd.read_stata('data/mergersample_controls.dta')
df.drop_duplicates(keep='first', inplace=True)
df_all     = df.loc[df.overlap==0]
df_all=df_all.assign(Obs=lambda df_all:len(df_all))
df_all     = df_all.filter(regex=filter_cols).T
std['b']=np.std(df_all, axis=1)
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
std['c']=np.std(df_control, axis=1)
df = df.filter(regex=filter_cols)
df_t['Variable']  = index
#df_t              = df_t.append({'Variable':'Obs'}, ignore_index=True)
df_t['Exposed']   = np.round(np.nanmean(df_exposed, axis=1), decimals=3)
df_t['Allother'] = np.round(np.nanmean(df_all, axis=1), decimals=3)
ptemp = stats.ttest_ind(df_exposed, df_all, axis=1, equal_var=True, nan_policy='omit')
df_t['pvalue01']   = np.round(np.ma.getdata(ptemp[1]), decimals=3)
df_t['Control']   = np.round(np.nanmean(df_control, axis=1), decimals=3)
ptemp = stats.ttest_ind(df_exposed, df_control, axis=1, equal_var=True, nan_policy='omit')
df_t['pvalue02']   = np.round(np.ma.getdata(ptemp[1]), decimals=3)
filter_cols = ['poptot','popdensity','pminority','pcollege','pincome','medincome','pmortgage','cont_totalbranches','cont_brgrowth','cont_total_origin','cont_NumSBL_Rev1']
index.remove('Obs')

print('{:<20s}{:>20s}{:>20s}{:>20s}{:>20s}{:>20s}'.format('Variable','Exposed','All other','p-value','Control','p-value'))
for i in index:
     print('{:<20s}{:>20.2f}{:>20.2f}{:>20.2f}{:>20.2f}{:>20.2f}'.format(i, df_t.Exposed[i], df_t.Allother[i], df_t.pvalue01[i], df_t.Control[i], df_t.pvalue02[i]))
     print('{:<20s}{:>20.2f}{:>20.2f}{:>20s}{:>20.2f}{:>20s}'.format(' ',std.a[i], std.b[i], ' ',std.c[i], ' '))
print('{:<20s}{:>20.0f}{:>20.0f}{:>20.0f}{:>20.2f}{:>20.2f}'.format('Obs',df_t.Exposed['Obs'], df_t.Allother['Obs'], df_t.pvalue01['Obs'], df_t.Control['Obs'], df_t.pvalue02['Obs']))