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
import statsmodels.api as sm

def panel_sample():
    columns = ['Y','D','X','L','M','Exp','E','groupID','timeeff']
    index = list()
    for i in range(400):
        for j in range(1999,2013):
            index.append((i, j))
    index = pd.MultiIndex.from_tuples(index, names=('indivID', 'year'))
    df = pd.DataFrame(columns=columns, index=index)
    eps= np.random.normal(size=5600)
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
    vars=['X','L','E']
    for var in vars:
        df[var]=np.random.normal(size=5600)
    for i in range(1999,2013):
        df.loc[(slice(None),i), 't'] = i
    for i in range(400):
        df.loc[i,(slice(None)), 'iFE'] = np.random.normal(size=13)
    gr1=np.repeat(1,1400)
    gr2=np.repeat(2,1400)
    gr3=np.repeat(3,1400)
    gr4=np.repeat(4,1400)
    df['groupID']=np.concatenate((gr1,gr2,gr3,gr4), axis=0)
    df['group_timeID']= df.groupby(['groupID', 't']).grouper.group_info[0]
    #df['indivID']=df.index
    df.loc[pd.isnull(df['M']), 'Exp'] = 0
    df.loc[pd.isnull(df['Exp']), 'Exp'] = 1
    df.loc[pd.isnull(df['M']), 'M'] = 0
    #indiveff=np.random.normal(1.5,0.5,5600)
    #for i in range(1,5):
    #    df.loc['groupID'==i, 'gFE'] = np.random.normal()
    groupeff1=np.random.normal(1,0.3,1400)
    groupeff2=np.random.normal(2,0.3,1400)
    groupeff3=np.random.normal(3,0.3,1400)
    groupeff4=np.random.normal(4,0.3,1400)
    groupeff=np.concatenate((groupeff1,groupeff2,groupeff3,groupeff4), axis=0)
    for i in range(1999,2013):
        trend=i/2000
        df.loc[(slice(None),i), 'timeeff'] =np.random.normal(trend,0.3)
    timeeff=df.timeeff
    group_timeFE=groupeff*timeeff
    # let's create the first stage (D is biased due to eps)
    df['D']= 0.6*df['M'] + 0.3*df.X + 0.1*df.E + groupeff + df.iFE + eps
    df.Y= 1 + df.iFE + 0.8*df.D + 0.5*df.X + 0.3*df.E + 0.2*df.L + group_timeFE + eps
    return df

df=panel_sample()
#df.to_csv('panel_sample.csv')

#model = 'Y ~ M + X + E + L + C(indivID) + C(groupID)'
#model = 'Y ~ M*Exp + X + E + L'
#reg = sm.OLS(model, df).fit()
#print(reg.summary)