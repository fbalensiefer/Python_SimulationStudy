/*******************************
main_results.do

Code for generating Figures 2-5, Tables 6-7.
********************************/

/**********************
MAIN RESULTS: FIRST STAGE
FIGURES 2-3
***********************/

use replication_input, clear

gen event_year = year - yr_approve

sum event_year
local min = r(min)
local max = r(max)
forvalues i=`min'/`max' {
	local j=`i'+abs(`min')
	gen edum`j'=0
	replace edum`j'=1 if event_year==`i' & overlap==1
	label var edum`j' "tau = `i'"
	}
	
forvalues i=1999/2013 {
	gen ydum`i' = 0
	replace ydum`i'=1 if year==`i'
	}
	
local chars poptot popdensity pminority pcollege ///
	medincome pincome cont_totalbranches cont_brgrowth 

foreach var in `chars' {
	forvalues year = 1999/2013 {
		gen `var'`year' = `var' * ydum`year'
		}
	}
drop `chars'

rename mergerID mergerID_OLD
egen mergerID = group(mergerID_OLD)
sum mergerID
local min = r(min)
local max = r(max)
forvalues i=`min'/`max' {
	gen mdum`i' = 0
	replace mdum`i'=1 if mergerID==`i'
	}

egen group_timeID = group(state_fps cnty_fps year)
egen indivID = group(state_fps cnty_fps tractstring)
egen clustID = group(state_fps cnty_fps)

sum event_year
local min = r(min)
local max = r(max)

** set tau=-1 to be the omitted category
local j=-1 + abs(`min')
drop edum`j'


foreach var in totalbranches num_closings {
	disp "$S_TIME"
	disp "`var'"
	preserve
	quietly do execute_yearbyyear.do `min' `max' `var' firststage totalbranches tract
	restore
	}
	
// Figure 2: Exposure to Consolidation and the Incidence of Branch Closings
use firststage, clear
foreach var in totalbranches num_closings {
	local m = _N+1
	set obs `m'
	replace tau=-1 in `m'
	replace coef=0 in `m'
	replace ci_lower=0 in `m'
	replace ci_upper=0 in `m'
	replace outcome = "`var'" in `m'
	drop if tau<-7 | tau>8
	}

eclplot coef ci_lower ci_upper tau if outcome=="num_closings" & ///
	tau>=-10 & tau<=10, ///
	scheme(s1mono) ///
	graphregion(fcolor(white)) ///
	bgcolor(white) ///
	ylabel(,nogrid) ///
	eplottype(scatter) ///
	estopts(mcolor(blue)) ///
	ciopts(blcolor(blue)) ///
	rplottype(rcap) ///
	nociforeground ///
	xline(0,lpattern(dash) lcolor(gs11)) ///
	yline(0,lpattern(dash) lcolor(gs11)) ///
	xline(-4, lcolor(gs14)) ///
	xline(6, lcolor(gs14)) ///
	ytitle("", size(large)) ///
	xtitle(Years since merger) ///
	title("Number of branch closings", size(large)) 


// Figure 3: Exposure to Consolidation and Local Branch Levels
eclplot coef ci_lower ci_upper tau if outcome=="totalbranches" & ///
	tau>=-10 & tau<=10, ///
	scheme(s1mono) ///
	graphregion(fcolor(white)) ///
	bgcolor(white) ///
	ylabel(,nogrid) ///
	eplottype(scatter) ///
	estopts(mcolor(blue)) ///
	ciopts(blcolor(blue)) ///
	rplottype(rcap) ///
	nociforeground ///
	xline(0,lpattern(dash) lcolor(gs11)) ///
	yline(0,lpattern(dash) lcolor(gs11)) ///
	xline(-4, lcolor(gs14)) ///
	xline(6, lcolor(gs14)) ///
	xtitle(Years since merger) ///
	ytitle("") ///
	title("Total branches", size(large)) 


/**********************
MAIN RESULTS: FIRST STAGE
TABLE 6, COLUMNS 1-2
***********************/

use replication_input, clear
gen event_year = year - yr_approve

gen edum_lessm1 = (event_year<-1 & overlap==1)
gen edum_0 = (event_year==0 & overlap==1)
gen edum_1 = (event_year==1 & overlap==1)
gen edum_2 = (event_year==2 & overlap==1)
gen edum_3 = (event_year==3 & overlap==1)
gen edum_4 = (event_year==4 & overlap==1)
gen edum_5 = (event_year==5 & overlap==1)
gen edum_6 = (event_year==6 & overlap==1)
gen edum_great6 = (event_year>6 & overlap==1)

forvalues i=1999/2013 {
	gen ydum`i' = 0
	replace ydum`i'=1 if year==`i'
	}
	
local chars poptot popdensity pminority pcollege ///
	medincome pincome cont_totalbranches cont_brgrowth 

foreach var in `chars' {
	forvalues year = 1999/2013 {
		gen `var'`year' = `var' * ydum`year'
		}
	}
drop `chars'

rename mergerID mergerID_OLD
egen mergerID = group(mergerID_OLD)
sum mergerID
local min = r(min)
local max = r(max)
forvalues i=`min'/`max' {
	gen mdum`i' = 0
	replace mdum`i'=1 if mergerID==`i'
	}

egen group_timeID = group(state_fps cnty_fps year)
egen indivID = group(state_fps cnty_fps tractstring)
egen clustID = group(state_fps cnty_fps)


reghdfe num_closings ///
	edum* poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 edum* using "FS_lessflex.xls", ///
	replace label excel ctitle("num_closings")

reghdfe totalbranches ///
	edum* poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 edum* using "FS_lessflex.xls", ///
	append label excel ctitle("totalbranches")

scalar drop _all
use replication_input, clear
gen event_year = year - yr_approve
keep if event_year==-1 & overlap==1
foreach var in num_closings totalbranches {
	quietly sum `var'
	scalar define `var' = r(mean)
	}
scalar list


/*********************
MAIN RESULTS: REDUCED FORM
FIGURE 4: EXPOSURE TO CONSOLIDATION AND THE VOLUME OF NEW LENDING
**********************/

use replication_input, clear

gen event_year = year - yr_approve

sum event_year
local min = r(min)
local max = r(max)
forvalues i=`min'/`max' {
	local j=`i'+abs(`min')
	gen edum`j'=0
	replace edum`j'=1 if event_year==`i' & overlap==1
	label var edum`j' "tau = `i'"
	}
	
forvalues i=1999/2012 {
	gen ydum`i' = 0
	replace ydum`i'=1 if year==`i'
	}

local chars poptot popdensity pminority pcollege ///
	medincome pincome cont_totalbranches cont_brgrowth

foreach var in `chars' {
	forvalues year = 1999/2012 {
		gen `var'`year' = `var' * ydum`year'
		}
	}
drop `chars'


rename mergerID mergerID_OLD
egen mergerID = group(mergerID_OLD)
sum mergerID
local min = r(min)
local max = r(max)
forvalues i=`min'/`max' {
	gen mdum`i' = 0
	replace mdum`i'=1 if mergerID==`i'
	}

egen group_timeID = group(state_fps cnty_fps year)
egen indivID = group(state_fps cnty_fps tractstring)
egen clustID = group(state_fps cnty_fps)

sum event_year
local min = r(min)
local max = r(max)

** set tau=r(min) to be the omitted category
local j=-1 + abs(`min')
drop edum`j'

foreach var in total_origin NumSBL_Rev1 {
	disp "$S_TIME"
	disp "`var'"
	preserve
	quietly do execute_yearbyyear.do `min' `max' `var' outcomes_event total_origin tract
	restore
	}

// Figure 4: Small Business Lending
use outcomes_event, clear
foreach var in total_origin NumSBL_Rev1 {
	local m = _N+1
	set obs `m'
	replace tau=-1 in `m'
	replace coef=0 in `m'
	replace ci_lower=0 in `m'
	replace ci_upper=0 in `m'
	replace outcome = "`var'" in `m'
	drop if tau<-7 | tau>8
	}

eclplot coef ci_lower ci_upper tau if outcome=="NumSBL_Rev1" & ///
	tau>=-10 & tau<=10, ///
	scheme(s1mono) ///
	graphregion(fcolor(white)) ///
	bgcolor(white) ///
	ylabel(,nogrid) ///
	ylabel(-6(3)6) ///
	eplottype(scatter) ///
	estopts(mcolor(blue)) ///
	ciopts(blcolor(blue)) ///
	rplottype(rcap) ///
	nociforeground ///
	xline(0,lpattern(dash) lcolor(gs11)) ///
	yline(0,lpattern(dash) lcolor(gs11)) ///
	xline(-4, lcolor(gs14)) ///
	xline(6, lcolor(gs14)) ///
	xtitle(Years since merger) ///
	ytitle("") ///
	title("New small business loans", size(large)) 

// Figure 4: Mortgages
eclplot coef ci_lower ci_upper tau if outcome=="total_origin" & ///
	tau>=-10 & tau<=10, ///
	scheme(s1mono) ///
	graphregion(fcolor(white)) ///
	bgcolor(white) ///
	ylabel(,nogrid) ///
	ylabel(-18(6)18) ///
	eplottype(scatter) ///
	estopts(mcolor(blue)) ///
	ciopts(blcolor(blue)) ///
	rplottype(rcap) ///
	nociforeground ///
	xline(0,lpattern(dash) lcolor(gs11)) ///
	yline(0,lpattern(dash) lcolor(gs11)) ///
	xline(-4, lcolor(gs14)) ///
	xline(6, lcolor(gs14)) ///
	xtitle(Years since merger) ///
	ytitle("") ///
	title("New mortgages", size(large)) 


/*********************
MAIN RESULTS: FIRST STAGE AND REDUCED FORM
FIGURE 5: THE EFFECT OF SUBSEQUENT BANK ENTRY ON LOCAL CREDIT SUPPLY
**********************/
	
** Figure 5: Small Business Lending
use outcomes_event, clear
foreach var in total_origin NumSBL_Rev1 {
	local m = _N+1
	set obs `m'
	replace tau=-1 in `m'
	replace coef=0 in `m'
	replace ci_lower=0 in `m'
	replace ci_upper=0 in `m'
	replace outcome = "`var'" in `m'
	drop if tau<-7 | tau>8
	}
keep if outcome=="NumSBL_Rev1"
keep coef tau 
rename coef SBLcoef
tempfile tempSBL
save "`tempSBL'", replace

use firststage, replace
foreach var in totalbranches {
	local m = _N+1
	set obs `m'
	replace tau=-1 in `m'
	replace coef=0 in `m'
	replace ci_lower=0 in `m'
	replace ci_upper=0 in `m'
	replace outcome = "`var'" in `m'
	drop if tau<-7 | tau>8
	}
keep if outcome=="totalbranches"
keep coef tau
rename coef branchcoef
merge 1:1 tau using "`tempSBL'"

twoway (scatter SBLcoef tau, yaxis(1) mcolor(blue)) ///
	(scatter branchcoef tau, yaxis(2) msymbol(T) mcolor(red)), ///
	scheme(s1mono) ///
	graphregion(fcolor(white)) ///
	bgcolor(white) ///
	ylabel(,nogrid) ///
	ylabel(-6(3)6) ///
	ylabel(-0.8(0.4)0.8,axis(2)) ///
	ytitle(Loans, axis(1)) ///
	ytitle(Total Branches, axis(2)) ///
	xline(0,lpattern(dash) lcolor(gs11)) ///
	yline(0,lpattern(dash) lcolor(gs11)) ///
	xline(-4, lcolor(gs14)) ///
	xline(6, lcolor(gs14)) ///
	xtitle(Years since merger) ///
	legend(label(1 "Loans") label(2 "Branches")) ///
	title("New small business loans", size(large)) 
	

** Figure 5: Mortgages
use outcomes_event, clear
foreach var in total_origin NumSBL_Rev1 {
	local m = _N+1
	set obs `m'
	replace tau=-1 in `m'
	replace coef=0 in `m'
	replace ci_lower=0 in `m'
	replace ci_upper=0 in `m'
	replace outcome = "`var'" in `m'
	drop if tau<-7 | tau>8
	}

keep if outcome=="total_origin"
keep coef tau 
rename coef origin
tempfile temporigin
save "`temporigin'", replace

use firststage, replace
foreach var in totalbranches {
	local m = _N+1
	set obs `m'
	replace tau=-1 in `m'
	replace coef=0 in `m'
	replace ci_lower=0 in `m'
	replace ci_upper=0 in `m'
	replace outcome = "`var'" in `m'
	drop if tau<-7 | tau>8
	}
keep if outcome=="totalbranches"
keep coef tau
rename coef branchcoef
merge 1:1 tau using "`temporigin'"

twoway (scatter origin tau, yaxis(1) mcolor(blue)) ///
	(scatter branchcoef tau, yaxis(2) msymbol(T) mcolor(red)), ///
	scheme(s1mono) ///
	graphregion(fcolor(white)) ///
	bgcolor(white) ///
	ylabel(,nogrid) ///
	ylabel(-18(6)18) ///
	ylabel(-0.8(0.4)0.8,axis(2)) ///
	ytitle(Loans, axis(1)) ///
	ytitle(Total Branches, axis(2)) ///
	xline(0,lpattern(dash) lcolor(gs11)) ///
	yline(0,lpattern(dash) lcolor(gs11)) ///
	xline(-4, lcolor(gs14)) ///
	xline(6, lcolor(gs14)) ///
	xtitle(Years since merger) ///
	legend(label(1 "Loans") label(2 "Branches")) ///
	title("New mortgages", size(large)) 
	
	
/*********************
MAIN RESULTS: REDUCED FORM
TABLE 6 - COLUMNS 3-4
**********************/

use replication_input, clear
gen event_year = year - yr_approve

gen edum_lessm1 = (event_year<-1 & overlap==1)
gen edum_0 = (event_year==0 & overlap==1)
gen edum_1 = (event_year==1 & overlap==1)
gen edum_2 = (event_year==2 & overlap==1)
gen edum_3 = (event_year==3 & overlap==1)
gen edum_4 = (event_year==4 & overlap==1)
gen edum_5 = (event_year==5 & overlap==1)
gen edum_6 = (event_year==6 & overlap==1)
gen edum_great6 = (event_year>6 & overlap==1)


forvalues i=1999/2013 {
	gen ydum`i' = 0
	replace ydum`i'=1 if year==`i'
	}
	
local chars poptot popdensity pminority pcollege ///
	medincome pincome cont_totalbranches cont_brgrowth 

foreach var in `chars' {
	forvalues year = 1999/2013 {
		gen `var'`year' = `var' * ydum`year'
		}
	}
drop `chars'

rename mergerID mergerID_OLD
egen mergerID = group(mergerID_OLD)
sum mergerID
local min = r(min)
local max = r(max)
forvalues i=`min'/`max' {
	gen mdum`i' = 0
	replace mdum`i'=1 if mergerID==`i'
	}

egen group_timeID = group(state_fps cnty_fps year)
egen indivID = group(state_fps cnty_fps tractstring)
egen clustID = group(state_fps cnty_fps)

reghdfe NumSBL_Rev1 ///
	edum* poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 edum* using "RF_table.xls", ///
	replace label excel ctitle("NumSBL_Rev1")

reghdfe total_origin ///
	edum* poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 edum* using "RF_table.xls", ///
	append label excel ctitle("total_origin")


scalar drop _all
use replication_input, clear
drop if year==2013
gen event_year = year - yr_approve
keep if event_year==-1 & overlap==1
foreach var in NumSBL_Rev1 total_origin {
	quietly sum `var'
	scalar define `var' = r(mean)
	}
scalar list


/*********************
MAIN RESULTS: OLS, RF, IV
TABLE 7 - IV ESTIMATES OF THE EFFECT OF CLOSINGS ON LOCAL CREDIT SUPPLY
**********************/

use replication_input, clear

gen event_year = year - yr_approve

preserve
gen close_2yr=0
replace close_2yr = closed_branch if event_year==0 | event_year==1
collapse (max) close_2yr, by(state_fps cnty_fps tractstring overlap mergerID)
tempfile tempclose2
save "`tempclose2'", replace
restore

merge m:1 state_fps cnty_fps tractstring overlap mergerID using ///
	"`tempclose2'"
drop _merge

gen POST = (event_year>0)
gen POST_close = POST * close_2yr
gen POST_expose = POST * overlap 

forvalues i=1999/2012 {
	gen ydum`i' = 0
	replace ydum`i'=1 if year==`i'
	}

local chars poptot popdensity pminority pcollege ///
	medincome pincome cont_totalbranches cont_brgrowth

foreach var in `chars' {
	forvalues year = 1999/2012 {
		gen `var'`year' = `var' * ydum`year'
		}
	}
drop `chars'


rename mergerID mergerID_OLD
egen mergerID = group(mergerID_OLD)
sum mergerID
local min = r(min)
local max = r(max)
forvalues i=`min'/`max' {
	gen mdum`i' = 0
	replace mdum`i'=1 if mergerID==`i'
	}

egen group_timeID = group(state_fps cnty_fps year)
egen indivID = group(state_fps cnty_fps tractstring)
egen clustID = group(state_fps cnty_fps)


//OLS
reghdfe NumSBL_Rev1 POST_close ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_close using "OLS.xls", ///
	replace label excel ctitle("NumSBL_Rev1")

reghdfe AmtSBL_Rev1 POST_close ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_expose using "OLS.xls", ///
	append label excel ctitle("AmtSBL_Rev1")

reghdfe total_origin POST_close ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_expose using "OLS.xls", ///
	append label excel ctitle("total_origin")

reghdfe loan_amount POST_close ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_expose using "OLS.xls", ///
	append label excel ctitle("loan_amount")


//REDUCED FORM
reghdfe NumSBL_Rev1 POST_expose ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_expose using "RF.xls", ///
	replace label excel ctitle("NumSBL_Rev1")

reghdfe AmtSBL_Rev1 POST_expose ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_expose using "RF.xls", ///
	append label excel ctitle("AmtSBL_Rev1")

reghdfe total_origin POST_expose ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_expose using "RF.xls", ///
	append label excel ctitle("total_origin")

reghdfe loan_amount POST_expose ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_expose using "RF.xls", ///
	append label excel ctitle("loan_amount")


//IV ESTIMATION
reghdfe NumSBL_Rev1 ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth* ///
	(POST_close = POST_expose), ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_close using "IV.xls", ///
	replace label excel ctitle("NumSBL_Rev1")
lincom 6*POST_close	

reghdfe AmtSBL_Rev1 ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth* ///
	(POST_close = POST_expose), ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_close using "IV.xls", ///
	append label excel ctitle("AmtSBL_Rev1")
lincom 6*POST_close	

reghdfe total_origin ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth* ///
	(POST_close = POST_expose), ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_close using "IV.xls", ///
	append label excel ctitle("total_origin")
lincom 6*POST_close	

reghdfe loan_amount ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth* ///
	(POST_close = POST_expose), ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_close using "IV.xls", ///
	append label excel ctitle("loan_amount")
lincom 6*POST_close	


scalar drop _all
use replication_input, clear
gen event_year = year - yr_approve
keep if event_year==-1 & overlap==1
foreach var in NumSBL_Rev1 AmtSBL_Rev1 total_origin loan_amount {
	quietly sum `var'
	scalar define `var' = r(mean)
	}
scalar list
