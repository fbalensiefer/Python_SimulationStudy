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

def get_covariates():

    o = np.random.normal()
    e = np.random.normal()
    
    x = o + np.random.normal()
    u = o + np.random.normal()
    
    return o, u, x, e


def get_panel_sample(num_agents):

    columns = ['popdensity','poptot','medincome','pminority','pcollege','pmortgage','pincome','cont_totalbranches', 'cont_brgrowth','cont_NumSBL_Rev1','cont_total_origin']
    index = list()
    for i in range(num_agents):
        for j in [1,2,3]:
            index.append((i, j))
    index = pd.MultiIndex.from_tuples(index, names=('group_timeID', 'indivID'))
    df = pd.DataFrame(columns=columns, index=index)

    df.loc[(slice(None), 1), 'D'] = 0

    for i in range(num_agents):

        o, u, x, e = get_covariates()

        # We first sample the outcomes in the control state.
        y0 = list()
        for level in [98, 99, 100]:
            rslt = level + o + u + x + e + np.random.normal(scale=np.sqrt(10))
            y0.append(rslt)

        # Sampling the effects of treatment
        baseline_effect = np.random.normal(loc=2, scale=1)
        additional_effect = np.random.normal(loc=0, scale=1)

        # The propensity score governs the attributes of selection. This is where the selection
        # on gains or the pretreatment variable is taking place.
        p = get_propensity_score(selection, o, u, additional_effect, y0)
        d = np.random.choice([1, 0], p=[p, 1 - p])
        
        # If the trajectories are diverging, we need to determine the shift here. This is a
        # violation of the common trend assumption.
        if trajectory == 'divergent' and d == 1:
            y0[-1] += 0.5
        elif trajectory == 'divergent' and d == 0:
            y0[-1] -= 0.5

        # We are not ready to compute the treatment outcomes.
        y1 = list()

        rslt = np.nan
        y1.append(rslt)

        rslt = y0[1] + baseline_effect + additional_effect
        y1.append(rslt)

        rslt = y0[2] + (1 + baseline_effect) + additional_effect
        y1.append(rslt)

        # Housekeeping and the creation of the data set.
        df.loc[(i, slice(None)), 'Y_8'] = y0[0]
        
        df.loc[(i, slice(None)), 'D_ever'] = d
        df.loc[(i, [2, 3]), 'D'] = d
        df.loc[(i, 1), 'D'] = 0

        df.loc[(i, slice(None)), 'Y_1'] = y1
        df.loc[(i, slice(None)), 'Y_0'] = y0

        df.loc[(i, slice(None)), ['O', 'E', 'X', 'U']] = [o, e, x, u]

        # Determining the observed outcome based on the choice and potential outcomes.
        df['Y'] = df['D'] * df['Y_1'] + (1 - df['D']) * df['Y_0']

    # Finally some type definitions for pretty output.
    df = df.astype(np.float)
    df = df.astype({'D': np.int, 'D_ever': np.int})

    return df