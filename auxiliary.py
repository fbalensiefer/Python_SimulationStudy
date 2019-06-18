import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
from patsy import dmatrices
import matplotlib.pyplot as plt
from scipy import stats
from linearmodels import PanelOLS

# Table 1: Merger Sample
def table1_fun():
    df = pd.read_stata('data/replication_input.dta')
    df = df[['acq_instname', 'out_instname', 'yr_approve', 'approved']]
    df.drop_duplicates(keep='first', inplace=True)
    df = df.sort_values(by='approved')
    df = df[['acq_instname', 'out_instname', 'yr_approve']]
    pd.options.display.float_format = '{:.0f}'.format
    df = df.rename(index=str , columns={'acq_instname':'Buyer', 'out_instname':'Target', 'yr_approve':'Year approved'})
    print(df.to_string(index=False))
    
