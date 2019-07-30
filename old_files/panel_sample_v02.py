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

def get_panel_sample():

    columns = ['Y','D','X','L','M','E','groupID']
    index = list()
    for i in range(100):
        for j in range(1999,2013):
            index.append((i, j))
    index = pd.MultiIndex.from_tuples(index, names=('indivID', 'year'))
    df = pd.DataFrame(columns=columns, index=index)
    eps= np.random.normal(size=1400)
    # randomly assign a treatment year, 
    # while only about 60 percent of indiviuals get treatment
    for j in range(60):
        cut=np.random.randint(low=2002,high=2010)
        for i in range(1999, cut):
            df.loc[(j, i), 'M'] = 0
        for i in range(cut,2013):
            df.loc[(j, i), 'M'] = 1
    # create controls in this case all regressors will be already standardized
    vars=['X','L','E']
    for var in vars:
        df[var]=np.random.normal(size=1400)
    # let's create the first stage (D is biased due to eps)
    df.loc[pd.isnull(df['M']), 'M'] = 0
    df['D']= 0.6*df['M'] + 0.3*df.X + 0.1*df.E + eps
    indiveff=np.random.normal(0.4,0.3,1400)
    df.Y= 1 + indiveff + 0.8*df.D + 0.5*df.X + 0.3*df.E + 0.2*df.L + eps
    return df

df=get_panel_sample()
df.to_csv('panel_sample.csv')