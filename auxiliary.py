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

def tab1():
    df = pd.read_stata('data/replication_input.dta')
    df = df[['acq_instname', 'out_instname', 'yr_approve', 'approved']]
    df.drop_duplicates(keep='first', inplace=True)
    df = df.sort_values(by='approved')
    df = df[['acq_instname', 'out_instname', 'yr_approve']]
    pd.options.display.float_format = '{:.0f}'.format
    df = df.rename(index=str , columns={'acq_instname':'Buyer', 'out_instname':'Target', 'yr_approve':'Year approved'})
    return df

def tab2():
    df = pd.read_stata('data/replication_input.dta')
    df = df.filter(regex='mergerID|premerger_acq|premerger_out')
    df.drop_duplicates(keep='first', inplace=True)
    df_t = pd.DataFrame(columns=['Variable', 'Median', 'Min', 'Max'])
    df = df.filter(regex='premerger_acq|premerger_out')
    df_t['Variable'] = ['Total assets', 'Branches', 'States of operation', 'Countries of operation', 'Total assets', 'Branches', 'States of operation', 'Countries of operation']
    df_t['Median']   = np.round(np.median(df, axis=0))
    df_t['Min']      = np.round(np.nanmin(df, axis=0))
    df_t['Max']      = np.round(np.nanmax(df, axis=0))
    #np.round(df.describe(percentiles=[.5]), 1).T # we only need min, 50% (median), max
    return df_t

def tab3():
    #df.assign(cntyID = df.sort_values(['state_fps', 'cnty_fps']))
    filter_cols = 'poptot|popdensity|pminority|pcollege|pincome|medincome|pmortgage|cont_totalbranches|cont_brgrowth|cont_total_origin|cont_NumSBL_Rev1|Obs'
    df = pd.read_stata('data/mergersample_controls.dta')
    index = ['popdensity','poptot','medincome','pminority','pcollege','pmortgage','pincome','cont_totalbranches', 'cont_brgrowth','cont_NumSBL_Rev1','cont_total_origin']
    df_t = pd.DataFrame(columns=['Variable', 'Exposed', 'All other', 'p-value 01', 'Control', 'p-value 02'], index=index)
    df.drop_duplicates(keep='first', inplace=True)
    df_exposed = df.loc[df.overlap==1]
    df_exposed=df_exposed.assign(Obs=lambda df_exposed:len(df_exposed))
    df_exposed = df_exposed.filter(regex=filter_cols).T
    df = pd.read_stata('data/mergersample_controls.dta')
    df.drop_duplicates(keep='first', inplace=True)
    df_all     = df.loc[df.overlap==0]
    df_all=df_all.assign(Obs=lambda df_all:len(df_all))
    df_all     = df_all.filter(regex=filter_cols).T
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
    df = df.filter(regex=filter_cols)
    df_t['Variable']  = list(df)
    df_t              = df_t.append({'Variable':'Obs'}, ignore_index=True)
    df_t['Exposed']   = np.round(np.nanmean(df_exposed, axis=1), decimals=3)
    df_t['All other'] = np.round(np.nanmean(df_all, axis=1), decimals=3)
    ptemp = stats.ttest_ind(df_exposed, df_all, axis=1, equal_var=True, nan_policy='omit')
    df_t['p-value 01']   = np.round(np.ma.getdata(ptemp[1]), decimals=3)
    df_t['Control']   = np.round(np.nanmean(df_control, axis=1), decimals=3)
    ptemp = stats.ttest_ind(df_exposed, df_control, axis=1, equal_var=True, nan_policy='omit')
    df_t['p-value 02']   = np.round(np.ma.getdata(ptemp[1]), decimals=3)
    filter_cols = ['poptot','popdensity','pminority','pcollege','pincome','medincome','pmortgage','cont_totalbranches','cont_brgrowth','cont_total_origin','cont_NumSBL_Rev1']
    #print(df_control)
    #np.shape(ptemp)
    return df_t

def tab4():
    filter_cols = 'poptot|popdensity|pminority|pcollege|pincome|medincome|pmortgage|cont_totalbranches|cont_brgrowth|cont_total_origin|cont_NumSBL_Rev1|Obs'
    df = pd.read_stata('data/alltract_controls.dta')
    #index = ['popdensity','poptot','medincome','pminority','pcollege','pmortgage','pincome','cont_totalbranches', 'cont_brgrowth','cont_NumSBL_Rev1','cont_total_origin']
    index = ['popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'pmortgage', 'totalbranches', 'brgrowth', 'NumSBL_Rev1', 'total_origin', 'pincome', 'Obs']
    df_t = pd.DataFrame(columns=['Variable', 'All', 'Closings', 'Merger'], index=index)
    df.drop_duplicates(keep='first', inplace=True)
    df_all = df.loc[df['year']>=2002]
    df_all = df_all.loc[df_all['year']<=2007]
    df_all = df_all.groupby(['state_fps', 'cnty_fps', 'tractstring'])
    df_all = df_all.agg(np.nanmax)
    #df_all = df_all.agg(np.nanmean)
    df_all = df_all.loc[df_all['totalbranches']>0]
    df_all['Obs'] = len(df_all)
    df_all = df_all.agg(np.nanmean)
    alltract_index = 'popdensity|poptot|medincome|pminority|pcollege|pmortgage|totalbranches|brgrowth|NumSBL_Rev1|total_origin|pincome|Obs'
    df_all = df_all.filter(regex=alltract_index)
    df_closing = df.loc[df['year']>=2002]
    df_closing = df_closing.loc[df_closing['year']<=2007]
    df_closing = df_closing.groupby(['state_fps', 'cnty_fps', 'tractstring'])
    df_closing = df_closing.agg(np.nanmax)
    df_closing = df_closing.loc[df_closing['num_closings']>0]
    df_closing['Obs'] = len(df_closing)
    df_closing = df_closing.agg(np.nanmean)
    df_closing = df_closing.filter(regex=alltract_index).T
    df = pd.read_stata('data/replication_input.dta')
    #df_merger      = df.loc[df['year']==2001]
    df_merger = df.loc[df['year']>=2002]
    df_merger = df_merger.loc[df_merger['year']<=2007]
    df01 = pd.read_stata('data/alltract_controls.dta')
    df01.drop_duplicates(keep='first', inplace=True)
    df_merger = pd.merge(df_merger,df01,  on=['state_fps','cnty_fps','tractstring'], how='inner', suffixes=('', '_y'))
    df_merger = df_merger.groupby(['state_fps', 'cnty_fps', 'tractstring'])
    df_merger = df_merger.agg(np.nanmax)
    num= len(df_merger)
    df_merger = df_merger.agg(np.nanmean)
    df_merger.rename(index= {'cont_totalbranches': 'totalbranches', 'cont_brgrowth':'brgrowth', 'cont_NumSBL_Rev1':'NumSBL_Rev1','cont_total_origin':'total_origin'},  inplace = True)
    df_merger = df_merger.filter(regex=alltract_index).T
    df_merger = df_merger.iloc[4:15]
    df_merger['Obs'] = num
    df_t['Variable']  = list(index)
    df_t['All']       = np.round(df_all, decimals=3)
    df_t['Closings']  = np.round(df_closing, decimals=3)
    df_t['Merger']    = np.round(df_merger, decimals=3)
    return df_t

def tab5():
    ## calculating MEDIAN values
    df = pd.read_stata('data/replication_input.dta')
    index = ['popdensity','poptot','medincome','pminority','pcollege','pmortgage','pincome','cont_totalbranches', 'cont_brgrowth','cont_NumSBL_Rev1','cont_total_origin']
    df.drop_duplicates(keep='first', inplace=True)
    df=df.assign(event_year=lambda df:df.year-df.yr_approve)
    df=df.loc[df['event_year']==1]
    p50=df[index].median()
    ## estimate the proportion of ALWAYS TAKERS, NEVER TAKERS and COMPLIERS
    df_at = df.loc[df['overlap']==0]
    p_always = np.nanmean(df_at.closed_branch)
    df_nt = df.assign(temp=lambda df:1-df.closed_branch)
    df_nt = df_nt.loc[df_nt['overlap']==1]
    p_never = np.nanmean(df_nt.temp)
    p_comp=1-p_always-p_never
    ## ESTIMATE AVERAGE CHARACTERISTICS OVER SET OF ALWAYS TAKERS AND COMPLIERS COMBINED (i.e.,Treatment tracts who had closings)
    df_t1 = pd.DataFrame(index=index)
    df_atcomp = df.loc[df['overlap']==1]
    df_atcomp = df_atcomp.loc[df_atcomp['closed_branch']==1]
    n=len(df_atcomp)
    for i in index:
        temp=df_atcomp[df_atcomp[i]>p50[i]].count()
        df_t1[i]=temp/n
    df_t1=df_t1.T
    df_atcomp=df_t1['poptot']
    ## ESTIMATE AVERAGE CHARACTERISTICS OVER ALWAYS TAKERS ONLY (i.e., Control tracts who had closings)
    df_t2 = pd.DataFrame(index=index)
    df_at = df.loc[df['overlap']==0]
    df_at = df_at.loc[df_at['closed_branch']==1]
    n=len(df_at)
    for i in index:
        temp=df_at[df_at[i]>p50[i]].count()
        df_t2[i]=temp/n
    df_t2=df_t2.T
    df_at=df_t2['poptot']
    ##  ESTIMATE AVERAGE CHARACTERISTICS FOR COMPLIERS
    ecomp=((p_always+p_comp)/p_comp)*(df_atcomp-((p_always/(p_always+p_comp))*df_at))
    ## CALCULATE RATIO
    ratio=ecomp/0.5
    ## PRINT to Table
    df_tab = pd.DataFrame(columns=['Variables','ecomp','ratio'], index=index)
    df_tab['Variables']=list(df[index])
    df_tab['ecomp']=ecomp*100
    df_tab['ratio']=ratio
    return df_tab

def fig2():
    df = pd.read_stata('data/replication_input.dta')
    df.drop_duplicates(keep='first', inplace=True)
    df=df.assign(event_year=lambda df:df.year-df.yr_approve)
    index=list(df)
    df['group_timeID']= df.groupby(['state_fps', 'cnty_fps', 'year']).grouper.group_info[0]
    df['indivID']= df.groupby(['state_fps', 'cnty_fps', 'tractstring']).grouper.group_info[0]
    df['clustID']= df.groupby(['state_fps', 'cnty_fps']).grouper.group_info[0] 
    dummy = pd.get_dummies(df['year'])
    chars = ['poptot', 'popdensity', 'pminority', 'pcollege', 'medincome', 'pincome', 'cont_totalbranches', 'cont_brgrowth'] 
    for i in chars:
        for j in range(1999,2014):
            name=i+str(j)
            df[name]=0
            df[name]=df[i].loc[df['year']==j]
    df = df.fillna(0)
    dftemp = df.filter(regex='poptot|popdensity|pminority|pcollege|medincome|pincome|cont_totalbranches|cont_brgrowth')
    dftemp = dftemp.drop(chars, axis=1)  
    controllist = list(dftemp)
    #df[controllist] = df[controllist].fillna(0)
    #temp = df.groupby([i, 'year']).grouper.group_info[0]       
    df.set_index(['indivID', 'group_timeID'], inplace=True)
    dftest=df.copy()
    dftest['num_closings']=(dftest['num_closings']-dftest['num_closings'].min())/(dftest['num_closings'].max()-dftest['num_closings'].min())
    for i in range(-7,9):
        dum='eD'+str(i)
        dftest[dum]=0
        dftest[dum].loc[(dftest['event_year']==i) & dftest['overlap']==1]=1
    dummylist=list(dftest.filter(regex='eD'))
    exog = dummylist + controllist
    index= dummylist
    mod = PanelOLS(dftest.num_closings, dftest[exog], entity_effects=True, time_effects=True, drop_absorbed=True)
    reg = mod.fit(cov_type='clustered', clusters=dftest.clustID)
    mean=reg.params[index]
    std=reg.std_errors[index]
    return [mean, std]

def fig3():
    df = pd.read_stata('data/replication_input.dta')
    df.drop_duplicates(keep='first', inplace=True)
    df=df.assign(event_year=lambda df:df.year-df.yr_approve)
    index=list(df)
    df['group_timeID']= df.groupby(['state_fps', 'cnty_fps', 'year']).grouper.group_info[0]
    df['indivID']= df.groupby(['state_fps', 'cnty_fps', 'tractstring']).grouper.group_info[0]
    df['clustID']= df.groupby(['state_fps', 'cnty_fps']).grouper.group_info[0] 
    dummy = pd.get_dummies(df['year'])
    chars = ['poptot', 'popdensity', 'pminority', 'pcollege', 'medincome', 'pincome', 'cont_totalbranches', 'cont_brgrowth'] 
    for i in chars:
        for j in range(1999,2014):
            name=i+str(j)
            df[name]=0
            df[name]=df[i].loc[df['year']==j]
    df = df.fillna(0)
    dftemp = df.filter(regex='poptot|popdensity|pminority|pcollege|medincome|pincome|cont_totalbranches|cont_brgrowth')
    dftemp = dftemp.drop(chars, axis=1)  
    controllist = list(dftemp)
    #df[controllist] = df[controllist].fillna(0)
    #temp = df.groupby([i, 'year']).grouper.group_info[0]       
    df.set_index(['indivID', 'group_timeID'], inplace=True)
    dftest=df.copy()
    dftest['totalbranches']=(dftest['totalbranches']-dftest['totalbranches'].min())/(dftest['totalbranches'].max()-dftest['totalbranches'].min())
    for i in range(-7,9):
        dum='eD'+str(i)
        dftest[dum]=0
        dftest[dum].loc[(dftest['event_year']==i) & dftest['overlap']==1]=1
    dummylist=list(dftest.filter(regex='eD'))
    exog = dummylist + controllist
    index= dummylist
    mod = PanelOLS(dftest.totalbranches, dftest[exog], entity_effects=True, time_effects=True, drop_absorbed=True)
    reg = mod.fit(cov_type='clustered', clusters=dftest.clustID)
    mean=reg.params[index]
    std=reg.std_errors[index]
    return [mean, std]

def fig4():
    df = pd.read_stata('data/replication_input.dta')
    df.drop_duplicates(keep='first', inplace=True)
    df=df.assign(event_year=lambda df:df.year-df.yr_approve)
    index=list(df)
    df['group_timeID']= df.groupby(['state_fps', 'cnty_fps', 'year']).grouper.group_info[0]
    df['indivID']= df.groupby(['state_fps', 'cnty_fps', 'tractstring']).grouper.group_info[0]
    df['clustID']= df.groupby(['state_fps', 'cnty_fps']).grouper.group_info[0] 
    dummy = pd.get_dummies(df['year'])
    chars = ['poptot', 'popdensity', 'pminority', 'pcollege', 'medincome', 'pincome', 'cont_totalbranches', 'cont_brgrowth'] 
    for i in chars:
        for j in range(1999,2014):
            name=i+str(j)
            df[name]=0
            df[name]=df[i].loc[df['year']==j]
    df = df.fillna(0)
    dftemp = df.filter(regex='poptot|popdensity|pminority|pcollege|medincome|pincome|cont_totalbranches|cont_brgrowth')
    dftemp = dftemp.drop(chars, axis=1)  
    controllist = list(dftemp)
    #df[controllist] = df[controllist].fillna(0)
    #temp = df.groupby([i, 'year']).grouper.group_info[0]       
    df.set_index(['indivID', 'group_timeID'], inplace=True)
    dftest=df.copy()
    dftest['NumSBL_Rev1']=(dftest['NumSBL_Rev1']-dftest['NumSBL_Rev1'].min())/(dftest['NumSBL_Rev1'].max()-dftest['NumSBL_Rev1'].min())
    dftest['total_origin']=(dftest['total_origin']-dftest['total_origin'].min())/(dftest['total_origin'].max()-dftest['total_origin'].min())
    for i in range(-7,9):
        dum='eD'+str(i)
        dftest[dum]=0
        dftest[dum].loc[(dftest['event_year']==i) & dftest['overlap']==1]=1

    dummylist=list(dftest.filter(regex='eD'))
    exog = dummylist + controllist
    index= dummylist
    mod1 = PanelOLS(dftest.NumSBL_Rev1, dftest[exog], entity_effects=True, time_effects=True, drop_absorbed=True)
    reg1 = mod1.fit(cov_type='clustered', clusters=dftest.clustID)
    mean1=reg1.params[index]
    std1=reg1.std_errors[index]
    
    mod2 = PanelOLS(dftest.total_origin, dftest[exog], entity_effects=True, time_effects=True, drop_absorbed=True)
    reg2 = mod2.fit(cov_type='clustered', clusters=dftest.clustID)
    mean2=reg2.params[index]
    std2=reg2.std_errors[index]
    return [mean1, std1, mean2, std2]

def fig4old():
    ## Small Business Lending
    df = pd.read_stata('data/replication_input.dta')
    df.drop_duplicates(keep='first', inplace=True)
    df=df.assign(event_year=lambda df:df.year-df.yr_approve)
    index=list(df)
    dfmean = pd.DataFrame(columns=range(-8, 10), index=index)
    dfstd = pd.DataFrame(columns=range(-8, 10), index=index)
    #df['NumSBL_Rev1']=(df['NumSBL_Rev1']-df['NumSBL_Rev1'].mean())/df['NumSBL_Rev1'].std()
    df['NumSBL_Rev1']=(df['NumSBL_Rev1']-df['NumSBL_Rev1'].min())/(df['NumSBL_Rev1'].max()-df['NumSBL_Rev1'].min())
    for i in range(-8, 11):
        dfmean[i]=df.loc[(df['event_year']==i) & df['overlap']==1].mean()
        dfstd[i]=df.loc[(df['event_year']==i) & df['overlap']==1].std()
    dfmean=dfmean.T
    dfstd=dfstd.T
    mean1=dfmean['NumSBL_Rev1']
    std1=dfstd['NumSBL_Rev1']

    ## Mortgages
    df = pd.read_stata('data/replication_input.dta')
    df.drop_duplicates(keep='first', inplace=True)
    df=df.assign(event_year=lambda df:df.year-df.yr_approve)
    index=list(df)
    dfmean = pd.DataFrame(columns=range(-8, 10), index=index)
    dfstd = pd.DataFrame(columns=range(-8, 10), index=index)
    #df['total_origin']=(df['total_origin']-df['total_origin'].mean())/df['total_origin'].std()
    df['total_origin']=(df['total_origin']-df['total_origin'].min())/(df['total_origin'].max()-df['total_origin'].min())
    for i in range(-8, 11):
        dfmean[i]=df.loc[(df['event_year']==i) & df['overlap']==1].mean()
        dfstd[i]=df.loc[(df['event_year']==i) & df['overlap']==1].std()
    dfmean=dfmean.T
    dfstd=dfstd.T
    mean2=dfmean['total_origin']
    std2=dfstd['total_origin']
    return [mean1, std1, mean2, std2]

def tab6():
    df = pd.read_stata('data/replication_input.dta')
    df.drop_duplicates(keep='first', inplace=True)
    df=df.assign(event_year=lambda df:df.year-df.yr_approve)
    index=list(df)
    df['group_timeID']= df.groupby(['state_fps', 'cnty_fps', 'year']).grouper.group_info[0]
    df['indivID']= df.groupby(['state_fps', 'cnty_fps', 'tractstring']).grouper.group_info[0]
    df['clustID']= df.groupby(['state_fps', 'cnty_fps']).grouper.group_info[0] 
    dummy = pd.get_dummies(df['year'])
    chars = ['poptot', 'popdensity', 'pminority', 'pcollege', 'medincome', 'pincome', 'cont_totalbranches', 'cont_brgrowth'] 
    for i in chars:
        for j in range(1999,2014):
            name=i+str(j)
            df[name]=0
            df[name]=df[i].loc[df['year']==j]
    df = df.fillna(0)
    dftemp = df.filter(regex='poptot|popdensity|pminority|pcollege|medincome|pincome|cont_totalbranches|cont_brgrowth')
    dftemp = dftemp.drop(chars, axis=1)  
    controllist = list(dftemp)
    #df[controllist] = df[controllist].fillna(0)
    #temp = df.groupby([i, 'year']).grouper.group_info[0]       
    df.set_index(['indivID', 'group_timeID'], inplace=True)
    dftest=df.copy()
    dftest['eDl']=0
    dftest['eDl'].loc[(dftest['event_year']<-1) & dftest['overlap']==1]=1
    for i in range(0,7):
        dum='eD'+str(i)
        dftest[dum]=0
        dftest[dum].loc[(dftest['event_year']==i) & dftest['overlap']==1]=1

    dftest['eDu']=0
    dftest['eDu'].loc[(dftest['event_year']>6) & dftest['overlap']==1]=1
    dummylist=list(dftest.filter(regex='eD'))
    exog = dummylist + controllist
    index=['eDl','eD0','eD1','eD2','eD3','eD4','eD5','eD6','eDu']
    return [dftest, exog, index]

def tab7():
    df = pd.read_stata('data/replication_input.dta')
    df.drop_duplicates(keep='first', inplace=True)
    df=df.assign(event_year=lambda df:df.year-df.yr_approve)
    index=list(df)
    df['close_2yr']=0
    df['close_2yr']=df['closed_branch'].loc[(df.event_year==0) | (df.event_year==1)]
    df['close_2yr'].fillna(0, inplace=True)
    dftemp=df.groupby(['state_fps', 'cnty_fps', 'tractstring', 'overlap', 'mergerID'], sort=False)['close_2yr'].max()
    df=pd.merge(df,dftemp,on=['state_fps', 'cnty_fps', 'tractstring', 'overlap', 'mergerID'], validate='many_to_one')
    df['POST']=0
    df['POST'].loc[df.event_year>0]=1
    df['POST_close']=df.POST * df.close_2yr_y
    df['POST_expose']= df.POST * df.overlap 
    df['group_timeID']= df.groupby(['state_fps', 'cnty_fps', 'year']).grouper.group_info[0]
    df['indivID']= df.groupby(['state_fps', 'cnty_fps', 'tractstring']).grouper.group_info[0]
    df['clustID']= df.groupby(['state_fps', 'cnty_fps']).grouper.group_info[0] 
    dummy = pd.get_dummies(df['year'])
    chars = ['poptot', 'popdensity', 'pminority', 'pcollege', 'medincome', 'pincome', 'cont_totalbranches', 'cont_brgrowth'] 
    for i in chars:
        for j in range(1999,2014):
            name=i+str(j)
            df[name]=0
            df[name]=df[i].loc[df['year']==j]

    dftemp = df.filter(regex='poptot|popdensity|pminority|pcollege|medincome|pincome|cont_totalbranches|cont_brgrowth')
    dftemp = dftemp.drop(chars, axis=1)  
    controllist = list(dftemp)
    #df[controllist] = df[controllist].fillna(0)
    iID = pd.Categorical(df.indivID)
    grID = pd.Categorical(df.group_timeID)
    df = df.set_index(['indivID', 'group_timeID'])
    df['iID'] = iID
    df['grID'] = grID
    return[df, controllist]




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