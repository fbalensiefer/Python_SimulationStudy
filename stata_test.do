clear all
cls
set more off
cd "C:\Users\fabia\Google Drive\UniBonn\X_Microeconometrics\student-project-fbalensiefer"

import delimited "panel_sample.csv"

forvalues i=1/4 {
	forvalues j=1999/2013 {
	gen grD`i'`j' = 0
	replace grD`i'`j'=1 if groupid==`i' & year==`j'
	}
	}
gen dd=m*exp

*reghdfe y dd x l e grD*, abs(individ)

reghdfe y d, abs(iid group_timeid) vce(cluster groupid)

reghdfe y dd, abs(individ group_timeid) vce(cluster groupid)
reghdfe y dd x l e, abs(individ group_timeid) vce(cluster groupid)

egen meangr1 = mean(y) if groupid==1
egen meangr2 = mean(y) if groupid==2
egen meangr3 = mean(y) if groupid==3
egen meangr4 = mean(y) if groupid==4

