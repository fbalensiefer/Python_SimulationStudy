clear all
cls
cd "C:\Users\fabia\Google Drive\UniBonn\X_Microeconometrics\student-project-fbalensiefer"

import delimited "panel_sample.csv"

forvalues i=1/4 {
	gen grD`i' = 0
	replace grD`i'=1 if groupid==`i'
	}

reghdfe y m x l e grD*, abs(individ)

egen meangr1 = mean(y) if groupid==1
egen meangr2 = mean(y) if groupid==2
egen meangr3 = mean(y) if groupid==3
egen meangr4 = mean(y) if groupid==4

