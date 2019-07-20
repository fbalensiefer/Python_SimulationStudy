import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
from patsy import dmatrices
import matplotlib.pyplot as plt
from scipy import stats
import warnings

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
    df['group_timeID']= df.groupby(['state_fps', 'cnty_fps', 'year']).grouper.group_info[0]
    df['indivID']= df.groupby(['state_fps', 'cnty_fps', 'tractstring']).grouper.group_info[0]
    df['clustID']= df.groupby(['state_fps', 'cnty_fps']).grouper.group_info[0] 
    index=list(df)
    dfmean = pd.DataFrame(columns=range(-8, 10), index=index)
    dfstd = pd.DataFrame(columns=range(-8, 10), index=index)
    #df['num_closings']=(df['num_closings']-df['num_closings'].mean())/df['num_closings'].std()
    df['num_closings']=(df['num_closings']-df['num_closings'].min())/(df['num_closings'].max()-df['num_closings'].min())
    for i in range(-8, 11):
        dfmean[i]=df.loc[(df['event_year']==i) & df['overlap']==1].mean()
        dfstd[i]=df.loc[(df['event_year']==i) & df['overlap']==1].std()
    #for i in range(-8, 11):
    #    df['D'] = 0
    #    df.loc[df['event_year'] >= i , 'D'] = 1
    #    temp=df.loc[(df['event_year']==i) & df['overlap']==1]
    #    model = smf.ols(formula='num_closings ~ D + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + C(indivID) + C(group_timeID)', data=temp).fit(cov_type='HC2')
    #    dfmean[i]=model.params['D']
    #    dfstd[i]=model.HC2_se['D']
    dfmean=dfmean.T
    dfstd=dfstd.T
    mean=dfmean['num_closings']
    std=dfstd['num_closings']
    return [mean, std]

def fig3():
    df = pd.read_stata('data/replication_input.dta')
    df.drop_duplicates(keep='first', inplace=True)
    df=df.assign(event_year=lambda df:df.year-df.yr_approve)
    df['group_timeID']= df.groupby(['state_fps', 'cnty_fps', 'year']).grouper.group_info[0]
    df['indivID']= df.groupby(['state_fps', 'cnty_fps', 'tractstring']).grouper.group_info[0]
    df['clustID']= df.groupby(['state_fps', 'cnty_fps']).grouper.group_info[0] 
    index=list(df)
    dfmean = pd.DataFrame(columns=range(-8, 10), index=index)
    dfstd = pd.DataFrame(columns=range(-8, 10), index=index)
    #df['cont_totalbranches']=(df['cont_totalbranches']-df['cont_totalbranches'].mean())/df['cont_totalbranches'].std()
    df['totalbranches']=(df['totalbranches']-df['totalbranches'].min())/(df['totalbranches'].max()-df['totalbranches'].min())
    for i in range(-8, 11):
        dfmean[i]=df.loc[(df['event_year']==i) & df['overlap']==1].mean()
        dfstd[i]=df.loc[(df['event_year']==i) & df['overlap']==1].std()
    #for i in range(-8, 11):
    #    df['D'] = 0
    #    df.loc[df['event_year'] >= i , 'D'] = 1
    #    temp=df.loc[(df['event_year']==i) & df['overlap']==1]
    #    model = smf.ols(formula='totalbranches ~ D + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + C(indivID) + C(group_timeID)', data=temp).fit(cov_type='HC2')
        #model = smf.ols(formula='totalbranches ~ D + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + C(indivID) + C(group_timeID)', data=temp).fit(cov_type='cluster', cov_kwds={'groups': df['clustID']})
    #    dfmean[i]=model.params['D']
    #    dfstd[i]=model.HC2_se['D']
    dfmean=dfmean.T
    dfstd=dfstd.T
    mean=dfmean['totalbranches']
    std=dfstd['totalbranches']
    return [mean, std]

def fig4():
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
    mean=dfmean['NumSBL_Rev1']
    std=dfstd['NumSBL_Rev1']
    plt.subplot(2,2,1)
    plt.errorbar(mean.index, mean, xerr=0.5, yerr=2*std, linestyle='')
    plt.title('New Small Business loans')
    #plt.show() 

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
    mean=dfmean['total_origin']
    std=dfstd['total_origin']
    return [mean, std]