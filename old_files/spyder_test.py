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

filter_cols = 'poptot|popdensity|pminority|pcollege|pincome|medincome|pmortgage|cont_totalbranches|cont_brgrowth|cont_total_origin|cont_NumSBL_Rev1|Obs'
df = pd.read_stata('data/alltract_controls.dta')
#index = ['popdensity','poptot','medincome','pminority','pcollege','pmortgage','pincome','cont_totalbranches', 'cont_brgrowth','cont_NumSBL_Rev1','cont_total_origin']
index = ['popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'pmortgage', 'totalbranches', 'brgrowth', 'NumSBL_Rev1', 'total_origin', 'pincome', 'Obs']
df_t = pd.DataFrame(columns=['Variable', 'All', 'Closings', 'Merger'], index=index)
std = pd.DataFrame(columns=['a', 'b', 'c'], index=index)
df.drop_duplicates(keep='first', inplace=True)
temp=df.loc[df['year']==2001].copy()
df_all = df.loc[(df['year']>=2002)&(df['year']<=2007)].copy()
df_all = df_all.groupby(['state_fps', 'cnty_fps', 'tractstring'])
df_all = df_all.agg(np.nanmax)
df_all = df_all.loc[df_all['totalbranches']>0]
df_all = df_all['totalbranches']
df_all=pd.merge(temp, df_all, on=['state_fps', 'cnty_fps', 'tractstring'],how='inner', suffixes=('', '_y'))
df_all = df_all.loc[df_all['totalbranches_y']>0]
df_all = df_all.groupby(['state_fps', 'cnty_fps', 'tractstring'])
df_all = df_all.agg(np.nanmean)
df_all['Obs'] = len(df_all)
std['a'] = np.std(df_all)
df_all = df_all.agg(np.nanmean)
alltract_index = 'popdensity|poptot|medincome|pminority|pcollege|pmortgage|totalbranches|brgrowth|NumSBL_Rev1|total_origin|pincome|Obs'
df_all = df_all.filter(regex=alltract_index)
df_all = np.round(df_all, decimals=3)
df_closing = df.loc[df['year']>=2002]
df_closing = df_closing.loc[df_closing['year']<=2007]
df_closing = df_closing.groupby(['state_fps', 'cnty_fps', 'tractstring'])
df_closing = df_closing.agg(np.nanmax)
df_closing = df_closing['num_closings']
df_closing=pd.merge(temp, df_closing, on=['state_fps', 'cnty_fps', 'tractstring'],how='inner', suffixes=('', '_y'))
df_closing = df_closing.loc[df_closing['num_closings_y']>0]
df_closing = df_closing.groupby(['state_fps', 'cnty_fps', 'tractstring'])
df_closing = df_closing.agg(np.nanmean)
df_closing['Obs'] = len(df_closing)
std['b'] = np.std(df_closing)
df_closing = df_closing.agg(np.nanmean)
df_closing = df_closing.filter(regex=alltract_index).T
df_closing = np.round(df_closing, decimals=3)
df = pd.read_stata('data/replication_input.dta')
#df_merger      = df.loc[df['year']==2001]
df_merger = df.loc[df['year']>=2002]
df_merger = df_merger.loc[df_merger['year']<=2007]
df01 = pd.read_stata('data/alltract_controls.dta')
df01.drop_duplicates(keep='first', inplace=True)
df_merger = pd.merge(df_merger,df01,  on=['state_fps','cnty_fps','tractstring'], how='inner', suffixes=('', '_y'))
df_merger = pd.merge(temp, df_merger, on=['state_fps','cnty_fps','tractstring'], suffixes=('', '_y'))
df_merger = df_merger.groupby(['state_fps', 'cnty_fps', 'tractstring'])
df_merger = df_merger.agg(np.nanmean)
df_merger['Obs'] =len(df_merger) 
num=len(df_merger)
std['c'] = np.std(df_merger[index])
df_merger = df_merger.agg(np.nanmean)
#df_merger.rename(index= {'cont_totalbranches': 'totalbranches', 'cont_brgrowth':'brgrowth', 'cont_NumSBL_Rev1':'NumSBL_Rev1','cont_total_origin':'total_origin'},  inplace = True)
df_merger = df_merger.filter(regex=alltract_index).T
df_merger = df_merger.iloc[:12]
df_merger['Obs'] = num
df_merger=np.round(df_merger, decimals=3)
df_t['Variable']  = list(index)
df_t['All']       = np.round(df_all, decimals=3)
df_t['Closings']  = np.round(df_closing, decimals=3)
df_t['Merger']    = np.round(df_merger, decimals=3)
index.remove('Obs')
print('{:<15s}{:>20s}{:>25s}{:>20s}'.format('Variable','All branched tracts','Tracts with closings','Merger sample'))
for i in index:
     print('{:<15s}{:>20.2f}{:>25.2f}{:>20.2f}'.format(i, df_t.All[i], df_t.Closings[i], df_t.Merger[i]))
     print('{:<15s}{:>20.2f}{:>25.2f}{:>20.2f}'.format(' ',std.a[i], std.b[i], std.c[i]))
print('{:<15s}{:>20.0f}{:>25.0f}{:>20.0f}'.format('Obs',df_t.All['Obs'], df_t.Closings['Obs'], df_t.Merger['Obs']))