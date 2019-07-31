/*******************************
extensions.do

Code for generating Figure 6, Tables 8-9.
********************************/


/*********************
TABLE 8, PANEL A: CALL REPORT DATA
**********************/

** CRA BANKS AND SMALL BANKS

use replication_input, clear

gen event_year = year - yr_approve

preserve
gen close_2yr=0
replace close_2yr = closed_branch if event_year==0 | event_year==1
collapse (sum) close_2yr, by(state_fps cnty_fps tractstring overlap mergerID)
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

reghdfe sum_amt_CRA POST_expose ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_close using "RF_smallbanks.xls", ///
	replace label excel ctitle("sum_amt_CRA")

reghdfe sum_amt_notCRA POST_expose ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_close using "RF_smallbanks.xls", ///
	append label excel ctitle("sum_amt_notCRA")
	
	
** CREDIT UNIONS

use replication_input, clear

gen event_year = year - yr_approve

preserve
gen close_2yr=0
replace close_2yr = closed_branch if event_year==0 | event_year==1
collapse (sum) close_2yr, by(state_fps cnty_fps tractstring overlap mergerID)
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

reghdfe amt_MBLS_branchonly POST_expose ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_close using "RF_creditunions.xls", ///
	replace label excel ctitle("amt_MBLS_branchonly")


/**********************
TABLE 8, PANEL B: TARGET ONLY TRACTS
***********************/
	
use replication_input_TargetOnly, clear

gen event_year = year - yr_approve

preserve
gen close_2yr=0
replace close_2yr = closed_branch if event_year==0 | event_year==1
collapse (max) close_2yr, by(state_fps cnty_fps tractstring targetonly mergerID)
tempfile tempclose2
save "`tempclose2'", replace
restore

merge m:1 state_fps cnty_fps tractstring targetonly mergerID using ///
	"`tempclose2'"
drop _merge

gen POST = (event_year>0)
gen POST_close = POST * close_2yr
gen POST_expose = POST * targetonly 

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


reghdfe NumSBL_Rev1 POST_expose ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_expose using "RF_TargetOnly.xls", ///
	replace label excel ctitle("NumSBL_Rev1")


/**********************
TABLE 9: USING TARGET ONLY TRACTS AS A CONTROL GROUP
***********************/

use replication_input_TargetOnly_Control, clear

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


//REDUCED FORM
reghdfe NumSBL_Rev1 POST_expose ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_expose using "target_control.xls", ///
	replace label excel ctitle("NumSBL_Rev1 - RF")

reghdfe AmtSBL_Rev1 POST_expose ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth*, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_expose using "target_control.xls", ///
	append label excel ctitle("AmtSBL_Rev1 - RF")


//IV 
reghdfe NumSBL_Rev1 ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth* ///
	(POST_close = POST_expose), ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_close using "target_control_IV.xls", ///
	replace label excel ctitle("NumSBL_Rev1 - IV")


reghdfe AmtSBL_Rev1 ///
	poptot* popdensity* pminority* pcollege* medincome* ///
	cont_totalbranches* cont_brgrowth* ///
	(POST_close = POST_expose), ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID)
outreg2 POST_close using "target_control_IV.xls", ///
	append label excel ctitle("AmtSBL_Rev1 - IV")


/**********************
TABLE 8, PANEL C: BOOM VS. BUST
***********************/

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

reghdfe NumSBL_Rev1 POST_expose ///
	poptot* popdensity* pminority* medincome* ///
	cont_totalbranches* cont_brgrowth* ///
	if yr_approve<2006, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID) 
outreg2 POST_close using "RF_GRrobustness.xls", ///
	replace label excel ctitle("NumSBL_Rev1, boom")

reghdfe NumSBL_Rev1 POST_expose ///
	poptot* popdensity* pminority* medincome* ///
	cont_totalbranches* cont_brgrowth* ///
	if yr_approve>=2006, ///
	absorb(indivID group_timeID) ///
	vce(cluster clustID) 
outreg2 POST_close using "RF_GRrobustness.xls", ///
	append label excel ctitle("NumSBL_Rev1, bust")


/**********************
TABLE 8, PANEL D: SPLIT BY TRACT DEMOGRAPHIC
***********************/

use replication_input, clear
gen pwhite = 1-pminority
replace pwhite=. if pwhite<0
tempfile tempredefine
save "`tempredefine'", replace

quietly foreach control in pwhite medincome {

noisily display "$S_TIME"
noisily display "`control'"

use "`tempredefine'", clear

preserve
keep state_fps cnty_fps tractstring `control'
duplicates drop
_pctile `control', p(50)
gen below = (`control'<=r(r1))
replace below=. if `control'==.
keep state_fps cnty_fps tractstring below
tempfile tempbelow
save "`tempbelow'", replace
restore

merge m:1 state_fps cnty_fps tractstring using "`tempbelow'"
drop _merge

gen event_year = year - yr_approve

preserve
gen close_2yr=0
replace close_2yr = closed_branch if event_year==0 | event_year==1
collapse (sum) close_2yr, by(state_fps cnty_fps tractstring overlap mergerID)
tempfile tempclose2
save "`tempclose2'", replace
restore

merge m:1 state_fps cnty_fps tractstring overlap mergerID using ///
	"`tempclose2'"
drop _merge

gen POST = (event_year>0)

gen POST_close = POST * close_2yr
gen POST_close_below = POST_close * below

gen POST_expose = POST * overlap 
gen POST_expose_below = POST_expose * below


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

if "`control'"=="pwhite" {

	reghdfe NumSBL_Rev1 POST_expose ///
		poptot* popdensity* pcollege* medincome* ///
		cont_totalbranches* cont_brgrowth* if below==1, ///
		absorb(indivID group_timeID) ///
		vce(cluster clustID)
	outreg2 POST_expose using "SBL_crosscuts.xls", ///
		replace label excel ctitle("pwhite-below")

	reghdfe NumSBL_Rev1 POST_expose ///
		poptot* popdensity* pcollege* medincome* ///
		cont_totalbranches* cont_brgrowth* if below==0, ///
		absorb(indivID group_timeID) ///
		vce(cluster clustID)
	outreg2 POST_expose using "SBL_crosscuts.xls", ///
		append label excel ctitle("pwhite-above")
		
	}
		
else {

	reghdfe NumSBL_Rev1 POST_expose ///
		poptot* popdensity* pcollege* pminority* ///
		cont_totalbranches* cont_brgrowth* if below==1, ///
		absorb(indivID group_timeID) ///
		vce(cluster clustID)
	outreg2 POST_expose using "SBL_crosscuts.xls", ///
		append label excel ctitle("below")

	reghdfe NumSBL_Rev1 POST_expose ///
		poptot* popdensity* pcollege* pminority* ///
		cont_totalbranches* cont_brgrowth* if below==0, ///
		absorb(indivID group_timeID) ///
		vce(cluster clustID)
	outreg2 POST_expose using "SBL_crosscuts.xls", ///
		append label excel ctitle("above")
		
		}
	
}

seeout using "SBL_crosscuts.txt", label


/**********************
FIGURE 6: DIFFERENTIAL EFFECT OF BRANCH CLOSINGS, BY TRACT INCOME LEVEL
***********************/

use replication_input, clear

preserve
keep state_fps cnty_fps tractstring medincome
duplicates drop
_pctile medincome, p(49)
gen below = (medincome<=r(r1))
replace below=. if medincome==.
_pctile medincome, p(50)
gen above = (medincome>=r(r1))
replace above=. if medincome==.
keep state_fps cnty_fps tractstring below above
tempfile tempbelow
save "`tempbelow'", replace
restore

merge m:1 state_fps cnty_fps tractstring using "`tempbelow'"
drop _merge

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
egen clustID = group(state_fps cnty_fps tractstring)

sum event_year
local min = r(min)
local max = r(max)

** set tau=r(min) to be the omitted category
local j=-1 + abs(`min')
drop edum`j'


foreach var in NumSBL_Rev1 {
	disp "$S_TIME"
	disp "`var'"
	preserve
	keep if below==1
	quietly do execute_yearbyyear.do `min' `max' `var' SBL_ptile_medincome_B NumSBL_Rev1 tract
	restore
	preserve
	keep if above==1
	quietly do execute_yearbyyear.do `min' `max' `var' SBL_ptile_medincome_A NumSBL_Rev1 tract
	restore
	}


// FIGURE
use SBL_ptile_medincome_A, clear
foreach var in NumSBL_Rev1 {
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
rename coef fullcoef
tempfile tempfull
save "`tempfull'", replace
	
use SBL_ptile_medincome_B, clear
foreach var in NumSBL_Rev1 {
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
rename coef medincomecoef
merge 1:1 tau using "`tempfull'"

twoway (scatter fullcoef tau, yaxis(1) mcolor(dkgreen)) ///
	(scatter medincomecoef tau, yaxis(2) msymbol(T) mcolor(dkorange)), ///
	scheme(s1mono) ///
	graphregion(fcolor(white)) ///
	bgcolor(white) ///
	ylabel(,nogrid) ///
	ylabel(-6(3)6) ///
	ylabel(-6(3)6,axis(2)) ///
	ytitle(Loans, axis(1)) ///
	ytitle(Loans, axis(2)) ///
	xline(0,lpattern(dash) lcolor(gs11)) ///
	yline(0,lpattern(dash) lcolor(gs11)) ///
	xline(-4, lcolor(gs14)) ///
	xline(6, lcolor(gs14)) ///
	xtitle(Years since merger) ///
	legend(label(1 "Above-Median") label(2 "Below-Median")) ///
	title("New Small Business Loans", size(large)) 
