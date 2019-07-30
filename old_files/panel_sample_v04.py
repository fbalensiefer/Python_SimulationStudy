# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 13:49:04 2019

@author: fabian balensiefer

algorithm to produce a panel data sample
"""
###############################################################################
#       Preface
###############################################################################

# preface loading packages required for Python Data Science
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from linearmodels import PanelOLS

np.random.seed(123)

def panel_sample():
    columns = ['Y','D','X','M','Exp','E','groupID','timeeff']
    index = list()
    for i in range(400):
        for j in range(1999,2013):
            index.append((i, j))
    index = pd.MultiIndex.from_tuples(index, names=('indivID', 'year'))
    df = pd.DataFrame(columns=columns, index=index)
    eps= np.random.normal(0,0.5,size=5600)
    # randomly assign a treatment year, 
    # while only about 60 percent of indiviuals get treatment
    for j in range(120):
        cut=np.random.randint(low=2002,high=2010)
        for i in range(1999, cut):
            df.loc[(j, i), 'M'] = 0
        for i in range(cut,2013):
            df.loc[(j, i), 'M'] = 1
    for j in range(200,320):
        cut=np.random.randint(low=2002,high=2010)
        for i in range(1999, cut):
            df.loc[(j, i), 'M'] = 0
        for i in range(cut,2013):
            df.loc[(j, i), 'M'] = 1
    # create controls in this case all regressors will be already standardized
    for j in range(400):
        mu=int(np.random.uniform(1,10,1))
        for i in range(1999,2013):        
            df.loc[(j,i), 'X']=np.random.normal(mu,mu/3)
    for i in range(1999,2013):
        df.loc[(slice(None),i), 't'] = i
    for i in range(400):
        df.loc[(i,slice(None)), 'iID'] = i
    for i in range(400):
        df.loc[(i,slice(None)), 'iFE'] = np.random.normal()
    gr1=np.repeat(1,1400)
    gr2=np.repeat(2,1400)
    gr3=np.repeat(3,1400)
    gr4=np.repeat(4,1400)
    df['groupID']=np.concatenate((gr1,gr2,gr3,gr4), axis=0)
    for j in range(1,5):
        mu=int(np.random.uniform(1,10,1))
        for i in range(1999,2013):        
            df.loc[(df['groupID']==j)&(df['t']==i), 'E']=np.random.normal(mu,mu/3)
    df['group_timeID']= df.groupby(['groupID', 't']).grouper.group_info[0]
    df.loc[pd.isnull(df['M']), 'Exp'] = 0
    df.loc[pd.isnull(df['Exp']), 'Exp'] = 1
    df.loc[pd.isnull(df['M']), 'M'] = 0
    for i in range(1,5):
        #mu=int(np.random.uniform(1,10,1))
        df.loc[df['groupID']==i, 'gFE'] = np.random.normal()
    for i in range(1999,2013):
        trend=i/2000
        df.loc[(slice(None),i), 'timeeff'] =np.random.normal(trend,0.3)
    df['gtFE']=df.gFE*df.timeeff
    # let's create the first stage (D is biased due to eps)
    df['D']= 0.5*df['M'] + eps
    df.Y= 0.99*df.D + df.gtFE + df.iFE + eps
    return df

df=panel_sample()
df.to_csv('panel_sample.csv')

df['DD']=df.M*df.Exp
df['indivID']=df['iID'].copy()
df['gtID']=df['group_timeID'].copy()
df.set_index(['indivID', 'group_timeID'], inplace=True)

mod = PanelOLS(df.Y, df['D'], entity_effects=True, time_effects=True)
res = mod.fit(cov_type='clustered', cluster_entity=True)
print('The naiv approach, which should be biased \n %2.4f \n (%2.4f)' %(res.params,res.std_errors))

#mod1 = smf.ols('D ~ M + X', df)
mod1 = smf.ols('D ~ M', df)
res1 = mod1.fit()
df['predicted']=res1.predict()
mod2 = PanelOLS(df.Y, df.predicted, entity_effects=True, time_effects=True)
res2 = mod2.fit()
print('The naiv IV approach, which identifies the DGP \n First stage: \n %2.4f \n (%2.4f) \n Second stage: \n %2.4f \n (%2.4f)' %(res1.params['M'],res1.bse['M'],res2.params,res2.std_errors))

mod = PanelOLS(df.Y, df['DD'], entity_effects=True, time_effects=True)
res = mod.fit(cov_type='clustered', cluster_entity=True)
print('The reduced form (DD) with Exposure to merger as instrument \n %2.4f \n (%2.4f)' %(res.params,res.std_errors))

mod = PanelOLS(df.Y, df[['DD','X']], entity_effects=True, time_effects=True)
res = mod.fit(cov_type='clustered', cluster_entity=True)
print('The reduced form (DD) with Exposure to merger as instrument and control variables \n %2.4f \n (%2.4f)' %(res.params[0],res.std_errors[0]))
print('Note: the true effect is 0.5 thus the authors framework should yield reliable results')



##############################################################################
df['indivID']=df['iID'].copy()
df['year']=df['t'].copy()
df.set_index(['indivID', 'year'], inplace=True)
mod1 = PanelOLS(df.D, df[['M','X']],entity_effects=True, time_effects=True)
res1 = mod1.fit()
df['predicted']=res1.predict()
df['indivID']=df['iID'].copy()
df['group_timeID']=df['gtID'].copy()
df.set_index(['indivID', 'group_timeID'], inplace=True)
mod2 = PanelOLS(df.Y, df.predicted, entity_effects=True, time_effects=True)
res2 = mod2.fit()
print('The authors IV approach, which includes time-varying tract controls \n First stage: \n %2.4f \n (%2.4f) \n Second stage: \n %2.4f \n (%2.4f)' %(res1.params['M'],res1.std_errors['M'],res2.params,res2.std_errors))