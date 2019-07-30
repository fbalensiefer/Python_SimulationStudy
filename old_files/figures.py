# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 14:09:30 2019

@author: fabia
"""
#wdir='C:/Users/fabia/Google Drive/UniBonn/X_Microeconometrics/student-project-fbalensiefer'

# preface loading packages required for Python Data Science
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from linearmodels import PanelOLS

def fig2():
    df = pd.read_stata('data/replication_input.dta')
    df.drop_duplicates(keep='first', inplace=True)
    df=df.assign(event_year=lambda df:df.year-df.yr_approve)
    df['group_timeID']= df.groupby(['state_fps', 'cnty_fps', 'year']).grouper.group_info[0]
    df['indivID']= df.groupby(['state_fps', 'cnty_fps', 'tractstring']).grouper.group_info[0]
    df['clustID']= df.groupby(['state_fps', 'cnty_fps']).grouper.group_info[0] 
    index=list(df)
    dfmean = pd.DataFrame(columns=range(-8, 8), index=index)
    dfstd = pd.DataFrame(columns=range(-8, 8), index=index)
    df['num_closings']=(df['num_closings']-df['num_closings'].mean())/df['num_closings'].std()
    #df['num_closings']=(df['num_closings']-df['num_closings'].min())/(df['num_closings'].max()-df['num_closings'].min())
    #for i in range(-8, 11):
    #    dfmean[i]=df.loc[(df['event_year']==i) & df['overlap']==1].mean()
    #    dfstd[i]=df.loc[(df['event_year']==i) & df['overlap']==1].std()
    df = df.set_index(['indivID', 'group_timeID'])
    for i in range(-8, 8):
        df['D'] = 0
        df.loc[(df['event_year'] >= i) & df['overlap']==1, 'D'] = 1
        exog = ['D', 'poptot', 'popdensity', 'pminority', 'pcollege', 'medincome', 'pincome', 'cont_totalbranches', 'cont_brgrowth'] 
        mod = PanelOLS(df.num_closings, df[exog], entity_effects=False, time_effects=True)
        reg = mod.fit(cov_type='clustered', cluster_entity=False)
        dfmean[i]=reg.params['D']
        dfstd[i]=reg.std_errors['D']
    dfmean=dfmean.T
    dfstd=dfstd.T
    mean=dfmean['num_closings']
    std=dfstd['num_closings']
    return [mean, std]

mean=fig2()[0]
std=fig2()[1]
plt.errorbar(mean.index, mean, xerr=0.5, yerr=2*std, linestyle='')
plt.title('Number of branch closings')
plt.show() 


###############################################################################
###############################################################################

def fig3():
    df = pd.read_stata('data/replication_input.dta')
    df.drop_duplicates(keep='first', inplace=True)
    df=df.assign(event_year=lambda df:df.year-df.yr_approve)
    df['group_timeID']= df.groupby(['state_fps', 'cnty_fps', 'year']).grouper.group_info[0]
    df['indivID']= df.groupby(['state_fps', 'cnty_fps', 'tractstring']).grouper.group_info[0]
    df['clustID']= df.groupby(['state_fps', 'cnty_fps']).grouper.group_info[0] 
    index=list(df)
    dfmean = pd.DataFrame(columns=range(-8, 8), index=index)
    dfstd = pd.DataFrame(columns=range(-8, 8), index=index)
    df['cont_totalbranches']=(df['cont_totalbranches']-df['cont_totalbranches'].mean())/df['cont_totalbranches'].std()
    #df['totalbranches']=(df['totalbranches']-df['totalbranches'].min())/(df['totalbranches'].max()-df['totalbranches'].min())
    #for i in range(-8, 11):
    #    dfmean[i]=df.loc[(df['event_year']==i) & df['overlap']==1].mean()
    #    dfstd[i]=df.loc[(df['event_year']==i) & df['overlap']==1].std()
    df = df.set_index(['indivID', 'group_timeID'])
    for i in range(-8, 8):
        df['D'] = 0
        df.loc[(df['event_year'] >= i) & df['overlap']==1, 'D'] = 1
        exog = ['D', 'poptot', 'popdensity', 'pminority', 'pcollege', 'medincome', 'pincome', 'cont_totalbranches', 'cont_brgrowth'] 
        mod = PanelOLS(df.totalbranches, df[exog], entity_effects=False, time_effects=True)
        reg = mod.fit(cov_type='clustered', cluster_entity=False)
        dfmean[i]=reg.params['D']
        dfstd[i]=reg.std_errors['D']
    dfmean=dfmean.T
    dfstd=dfstd.T
    mean=dfmean['totalbranches']
    std=dfstd['totalbranches']
    return [mean, std]

mean=fig3()[0]
std=fig3()[1]
plt.errorbar(mean.index, mean, xerr=0.5, yerr=2*std, linestyle='')
plt.title('Total branches')
plt.show()  