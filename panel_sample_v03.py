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
    columns = ['Y','D','X','L','M','E','groupID']
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
    gr1=np.repeat(1,1400)
    gr2=np.repeat(2,1400)
    gr3=np.repeat(3,1400)
    gr4=np.repeat(4,1400)
    df['groupID']=np.concatenate((gr1,gr2,gr3,gr4), axis=0)
    #df['indivID']=df.index
    df.loc[pd.isnull(df['M']), 'M'] = 0
    indiveff=np.random.normal(0.4,0.3,5600)
    groupeff1=np.random.normal(1,0.3,1400)
    groupeff2=np.random.normal(2,0.3,1400)
    groupeff3=np.random.normal(3,0.3,1400)
    groupeff4=np.random.normal(4,0.3,1400)
    groupeff=np.concatenate((groupeff1,groupeff2,groupeff3,groupeff4), axis=0)
    # let's create the first stage (D is biased due to eps)
    df['D']= 0.6*df['M'] + 0.3*df.X + 0.1*df.E + groupeff + indiveff + eps
    df.Y= 1 + indiveff + 0.8*df.D + 0.5*df.X + 0.3*df.E + 0.2*df.L + groupeff + eps
    return df

df=panel_sample()
df.to_csv('panel_sample.csv')

#model = 'Y ~ M + X + E + L + C(indivID) + C(groupID)'
model = 'Y ~ M + X + E + L'
reg = sm.OLS(model, df).fit()
print(reg.summary)