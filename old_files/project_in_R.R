# -*- coding: utf-8 -*-
###############################################################################
#       Preface
###############################################################################

rm(list=ls())
setwd('/Users/Fabian/Google Drive/UniBonn/X_Microeconometrics/student-project-fbalensiefer')

# preface loading packages required for R
#library(plm)
library(haven)
library(dplyr)
library(dummies)

###############################################################################
###         Main Results
###############################################################################

# Table 6: First-Stage and Reduced-Form estimates 
df = read_dta('data/replication_input.dta')
distinct(df)
df['event_year'] = df['year']-df['yr_approve']
index=list(df)
df['group_timeID']= df %>% group_by(df$state_fps, df$cnty_fps, df$year) %>% group_indices
df['indivID']= df %>% group_by(df$state_fps, df$cnty_fps, df$tractstring) %>% group_indices
df['clustID']= df %>% group_by(df$state_fps, df$cnty_fps) %>% group_indices
dummy = dummy(df$year)
chars = c('poptot', 'popdensity', 'pminority', 'pcollege', 'medincome', 'pincome', 'cont_totalbranches', 'cont_brgrowth') 
# for (i in chars){
#   for (j in 1999:2014){
#     name=paste(i,j)
#     df[name]=0
#     temp=filter(df,year==j)
#     df[name]=temp[i]}
# }
for (i in chars){
  for (j in dummy){
    name=paste(i,j)
    df[name]=df[i]*j
    }
}
#df.set_index(['indivID', 'group_timeID'], inplace=True)

## estimates of column 1 (number of closings)
est_numclose= data.frame('beta', 'SE', rownames=range(-8, 10))
beta=data.frame(rownames=range(-8, 10))
std=data.frame(rownames=range(-8, 10))
for (i in -8:11){
  df$D = as.numeric(df$event_year >= i)
  temp=filter(df, (df$event_year==i) & (df$overlap==1))
  reg = lm('num_closings ~ D + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + factor(indivID) + factor(group_timeID)', data=temp)
  #summary(reg)
  beta[i]=reg$coefficients['D']
  std[i]=reg$residuals['D']
}
est_numclose['beta']=t(beta)
est_numclose['SE']=t(std)

## estimates of column 2 (total branches)
est_totalbranches= pd.DataFrame(columns=['beta', 'SE'], index=range(-8, 10))
for (i in -8:11):
  df['D'] = 0
df.loc[df['event_year'] >= i , 'D'] = 1
temp=df.loc[(df['event_year']==i) & df['overlap']==1]
y, x = dmatrices('totalbranches ~ D + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=temp)
model_spec = sm.OLS(y, x)
results = model_spec.fit()
#results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.totalbranches, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
beta[i]=results.params[2]
std[i]=results.HC0_se[2]
#pd.options.display.float_format = '{:.3f}'.format
est_totalbranches['beta']=beta.T
est_totalbranches['SE']=std.T

## estimates of column 3 (SBL origin)
est_SBLorigin= pd.DataFrame(columns=['beta', 'SE'], index=range(-8, 10))
for i in range(-8, 11):
  df['D'] = 0
df.loc[df['event_year'] >= i , 'D'] = 1
temp=df.loc[(df['event_year']==i) & df['overlap']==1]
y, x = dmatrices('NumSBL_Rev1 ~ D + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=temp)
model_spec = sm.OLS(y, x)
results = model_spec.fit()
#results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.NumSBL_Rev1, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
beta[i]=results.params[2]
std[i]=results.HC0_se[2]
#pd.options.display.float_format = '{:.3f}'.format
est_SBLorigin['beta']=beta.T
est_SBLorigin['SE']=std.T

## estimates of column 4 (Mortgage origin)
est_Morigin= pd.DataFrame(columns=['beta', 'SE'], index=range(-8, 10))
for i in range(-8, 11):
  df['D'] = 0
df.loc[df['event_year'] >= i , 'D'] = 1
temp=df.loc[(df['event_year']==i) & df['overlap']==1]
y, x = dmatrices('total_origin ~ D + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=temp)
model_spec = sm.OLS(y, x)
results = model_spec.fit()
#results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
beta[i]=results.params[2]
std[i]=results.HC0_se[2]
#pd.options.display.float_format = '{:.3f}'.format
est_Morigin['beta']=beta.T
est_Morigin['SE']=std.T

## finish table 6 by producing a df containing all estimates
df_t= pd.DataFrame(columns=['Num_closings', 'Total_branches', 'SBL_origin', 'Mortgage_origin'], index=range(-8, 10))
df_t['Num_closings']      = est_totalbranches['beta']
df_t['Total_branches']    = est_totalbranches['beta']
df_t['SBL_origin']        = est_SBLorigin['beta']
df_t['Mortgage_origin']   = est_Morigin['beta']

###############################################################################

# Table 6: First-Stage and Reduced-Form estimates 
df = pd.read_stata('data/replication_input.dta')
df.drop_duplicates(keep='first', inplace=True)
df=df.assign(event_year=lambda df:df.year-df.yr_approve)
index=list(df)
df['group_timeID']= df.groupby(['state_fps', 'cnty_fps', 'year']).grouper.group_info[0]
df['indivID']= df.groupby(['state_fps', 'cnty_fps', 'tractstring']).grouper.group_info[0]
df['clustID']= df.groupby(['state_fps', 'cnty_fps']).grouper.group_info[0] 
#df.set_index(['indivID', 'group_timeID'], inplace=True)

## estimates of column 1 (number of closings)
est_numclose= pd.DataFrame(columns=['beta', 'SE'], index=range(-8, 10))
beta=pd.DataFrame(index=range(-8, 10))
std=pd.DataFrame(index=range(-8, 10))
for i in range(-8, 11):
  df['D'] = 0
df.loc[df['event_year'] >= i , 'D'] = 1
temp=df.loc[(df['event_year']==i) & df['overlap']==1]
model = smf.ols(formula='num_closings ~ D + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + C(indivID) + C(group_timeID)', data=temp).fit(cov_type = 'HC2')
#print(model.summary())
beta[i]=model.params['D']
std[i]=model.HC0_se['D']
pd.options.display.float_format = '{:.3f}'.format
est_numclose['beta']=beta.T
est_numclose['SE']=std.T

###############################################################################

# Figure 3: Exposure to consolidation and local branch levels

df = pd.read_stata('data/replication_input.dta')
df.drop_duplicates(keep='first', inplace=True)
df=df.assign(event_year=lambda df:df.year-df.yr_approve)
index=list(df)
dfmean = pd.DataFrame(columns=range(-8, 10), index=index)
dfstd = pd.DataFrame(columns=range(-8, 10), index=index)
#df['cont_totalbranches']=(df['cont_totalbranches']-df['cont_totalbranches'].mean())/df['cont_totalbranches'].std()
df['cont_totalbranches']=(df['cont_totalbranches']-df['cont_totalbranches'].min())/(df['cont_totalbranches'].max()-df['cont_totalbranches'].min())
for i in range(-8, 11):
  dfmean[i]=df.loc[(df['event_year']==i) & df['overlap']==1].mean()
dfstd[i]=df.loc[(df['event_year']==i) & df['overlap']==1].std()
dfmean=dfmean.T
dfstd=dfstd.T
mean=dfmean['cont_totalbranches']
std=dfstd['cont_totalbranches']
plt.errorbar(mean.index, mean, xerr=0.5, yerr=2*std, linestyle='')
plt.show()  

###############################################################################

# Figure 4: Exposure to consolidation and the volume of new lending

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
plt.errorbar(mean.index, mean, xerr=0.5, yerr=2*std, linestyle='')
plt.show() 

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
plt.errorbar(mean.index, mean, xerr=0.5, yerr=2*std, linestyle='')
plt.show() 

###############################################################################

# Figure 5: The effect of subsequent bank entry on local credit supply
plt.figure()

## Small Business Lending
df = pd.read_stata('data/replication_input.dta')
df.drop_duplicates(keep='first', inplace=True)
df=df.assign(event_year=lambda df:df.year-df.yr_approve)
index=list(df)
dfmean = pd.DataFrame(columns=range(-8, 10), index=index)
#df['NumSBL_Rev1']=(df['NumSBL_Rev1']-df['NumSBL_Rev1'].mean())/df['NumSBL_Rev1'].std()
df['NumSBL_Rev1']=(df['NumSBL_Rev1']-df['NumSBL_Rev1'].min())/(df['NumSBL_Rev1'].max()-df['NumSBL_Rev1'].min())
df['totalbranches']=(df['totalbranches']-df['totalbranches'].min())/(df['totalbranches'].max()-df['totalbranches'].min())
for i in range(-8, 11):
  dfmean[i]=df.loc[(df['event_year']==i) & df['overlap']==1].mean()
dfmean=dfmean.T
mean=dfmean['NumSBL_Rev1']
plt.subplot(2,2,1)
plt.scatter(mean.index, mean)
plt.subplot(2,2,1)
plt.scatter(mean.index, dfmean['totalbranches'])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15))
plt.title('New Small Business loans')
#plt.show() 

## Mortgages
df = pd.read_stata('data/replication_input.dta')
df.drop_duplicates(keep='first', inplace=True)
df=df.assign(event_year=lambda df:df.year-df.yr_approve)
index=list(df)
dfmean = pd.DataFrame(columns=range(-8, 10), index=index)
#df['total_origin']=(df['total_origin']-df['total_origin'].mean())/df['total_origin'].std()
df['total_origin']=(df['total_origin']-df['total_origin'].min())/(df['total_origin'].max()-df['total_origin'].min())
df['totalbranches']=(df['totalbranches']-df['totalbranches'].min())/(df['totalbranches'].max()-df['totalbranches'].min())
for i in range(-8, 11):
  dfmean[i]=df.loc[(df['event_year']==i) & df['overlap']==1].mean()
dfmean=dfmean.T
mean=dfmean['total_origin']
plt.subplot(2,2,2)
plt.scatter(mean.index, mean)
plt.subplot(2,2,2)
plt.scatter(mean.index, dfmean['totalbranches'])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15))
plt.title('New Mortgages')
#plt.show() 

###############################################################################

# Table 7: IV-Estimates of the effect of closings an local credit supply
df = pd.read_stata('data/replication_input.dta')
df.drop_duplicates(keep='first', inplace=True)
df=df.assign(event_year=lambda df:df.year-df.yr_approve)
index=list(df)
df['close_2yr']=0
df['close_2yr']=df['closed_branch'].loc[(df.event_year==0) | (df.event_year==1)]
df['close_2yr'].fillna(0, inplace=True)
df['POST']=df['event_year'].loc[df.event_year>0]
df['POST_close']=df.POST * df.close_2yr
df['POST_expose']= df.POST * df.overlap 

df['group_timeID']= df.groupby(['state_fps', 'cnty_fps', 'year']).grouper.group_info[0]
df['indivID']= df.groupby(['state_fps', 'cnty_fps', 'tractstring']).grouper.group_info[0]
df['clustID']= df.groupby(['state_fps', 'cnty_fps']).grouper.group_info[0] 
df.set_index(['indivID', 'group_timeID'], inplace=True)

#################################################################################

## OLS
# NumSBL_Rev1
y, x = dmatrices('NumSBL_Rev1 ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
mod = PanelOLS(y, x, entity_effects=True)
results = mod.fit(cov_type='clustered', other_effects=['indivID', 'group_timeID'])
print(results.summary())

#################################################################################

## OLS
# NumSBL_Rev1
y, x = dmatrices('NumSBL_Rev1 ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
model_spec = sm.OLS(mod)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = mt.reg(temp, temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], fe_name=['indivID', 'group_timeID'], cluster='clustID')
#results = model_spec.fit()
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# AmtSBL_Rev1
y, x = dmatrices('AmtSBL_Rev1 ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# total_origin
y, x = dmatrices('total_origin ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# loan_amount
y, x = dmatrices('loan_amount ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())    

## Reduced Form
# NumSBL_Rev1
y, x = dmatrices('total_origin ~ POST_expose + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# AmtSBL_Rev1
y, x = dmatrices('AmtSBL_Rev1 ~ POST_expose + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# total_origin
y, x = dmatrices('total_origin ~ POST_expose + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# loan_amount
y, x = dmatrices('loan_amount ~ POST_expose + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

## IV ESTIMATION
# NumSBL_Rev1 - IV2SLS.from_formula()
y, x = dmatrices('NumSBL_Rev1 ~ popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + [POST_close ~ POST_expose]', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# AmtSBL_Rev1
y, x = dmatrices('AmtSBL_Rev1 ~ popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + [POST_close ~ POST_expose]', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# total_origin
y, x = dmatrices('total_origin ~ popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + [POST_close ~ POST_expose]', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# loan_amount
y, x = dmatrices('loan_amount ~ popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + [POST_close ~ POST_expose]', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())


###############################################################################
### Remaining Part is not relevant for further analysis
###############################################################################

# Resampling to control for overrepresentation in the sample
# (Idea: banks concentrade their closings in areas deemed to be "over-branched")
# Resample tracts across counties and states to test for robustness of the results

# Table 7 - Resampled: IV-Estimates of the effect of closings an local credit supply
df = pd.read_stata('data/replication_input.dta')
df.drop_duplicates(keep='first', inplace=True)
df=df.assign(event_year=lambda df:df.year-df.yr_approve)
index=list(df)
df['close_2yr']=0
df['close_2yr']=df['closed_branch'].loc[(df.event_year==0) | (df.event_year==1)]
df['close_2yr'].fillna(0, inplace=True)
df['POST']=df['event_year'].loc[df.event_year>0]
df['POST_close']=df.POST * df.close_2yr
df['POST_expose']= df.POST * df.overlap 

df['group_timeID']= df.groupby(['state_fps', 'cnty_fps', 'year']).grouper.group_info[0]
df['indivID']= df.groupby(['state_fps', 'cnty_fps', 'tractstring']).grouper.group_info[0]
df['clustID']= df.groupby(['state_fps', 'cnty_fps']).grouper.group_info[0] 
df.set_index(['indivID', 'group_timeID'], inplace=True)

#df = (df.set_index('indivID').reindex(range(df.indivID.min(), df.indivID.max())).interpolate().reset_index())

## OLS
# NumSBL_Rev1
y, x = dmatrices('NumSBL_Rev1 ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = mt.reg(temp, temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], fe_name=['indivID', 'group_timeID'], cluster='clustID')
#results = model_spec.fit()
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# AmtSBL_Rev1
y, x = dmatrices('AmtSBL_Rev1 ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# total_origin
y, x = dmatrices('total_origin ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# loan_amount
y, x = dmatrices('loan_amount ~ POST_close + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())    

## Reduced Form
# NumSBL_Rev1
y, x = dmatrices('total_origin ~ POST_expose + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# AmtSBL_Rev1
y, x = dmatrices('AmtSBL_Rev1 ~ POST_expose + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# total_origin
y, x = dmatrices('total_origin ~ POST_expose + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# loan_amount
y, x = dmatrices('loan_amount ~ POST_expose + popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

## IV ESTIMATION
# NumSBL_Rev1 - IV2SLS.from_formula()
y, x = dmatrices('NumSBL_Rev1 ~ popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + [POST_close ~ POST_expose]', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# AmtSBL_Rev1
y, x = dmatrices('AmtSBL_Rev1 ~ popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + [POST_close ~ POST_expose]', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# total_origin
y, x = dmatrices('total_origin ~ popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + [POST_close ~ POST_expose]', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())

# loan_amount
y, x = dmatrices('loan_amount ~ popdensity + poptot + medincome + pminority + pcollege +  cont_totalbranches + cont_brgrowth + [POST_close ~ POST_expose]', data=df)
model_spec = sm.OLS(y, x)
results = model_spec.fit(cov_type='HAC',cov_kwds={'maxlags':1})
#model_spec = PanelOLS(temp.total_origin, temp[['D', 'popdensity', 'poptot', 'medincome', 'pminority', 'pcollege', 'cont_totalbranches', 'cont_brgrowth']], entity_effects=True)
#results = model_spec.fit(cov_type='clustered', cluster_entity=True)
print(results.summary())
