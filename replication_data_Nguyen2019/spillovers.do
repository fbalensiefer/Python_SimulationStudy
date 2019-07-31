/*******************************
spillovers.do

Code for generating Figure 7.
********************************/

/**********************
FIGURE 7: THE GEOGRAPHIC SPILLOVER OF BANK BRANCH CLOSINGS
***********************/

forvalues x = 0/10 {

use spillover_`x', clear
//drop if year==2013

gen event_year = year - yr_approve

gen POST = (event_year>0 & treated==1)

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

disp "`x'"

if "`x'"=="0" {
		disp "$S_TIME"
		disp "`var'"
		reghdfe NumSBL_Rev1 POST ///
			poptot* popdensity* pminority* pcollege* medincome* ///
			cont_totalbranches* cont_brgrowth*, ///
			absorb(indivID group_timeID) vce(cluster clustID)
		
		regsave, tstat pval ci
		drop if _n > 1
		gen buffer = "`x'"
		save spillover_estimates, replace
		}

else {
		disp "$S_TIME"
		disp "`var'"
		reghdfe NumSBL_Rev1 POST ///
			poptot* popdensity* pminority* pcollege* medincome* ///
			cont_totalbranches* cont_brgrowth*, ///
			absorb(indivID group_timeID) vce(cluster clustID)
		
		regsave, tstat pval ci
		drop if _n > 1
		gen buffer = "`x'"
		append using spillover_estimates
		save spillover_estimates, replace
		}
		
}


// FIGURE
use spillover_estimates, clear
drop buffer
gen buffer=.
replace buffer = abs(_n-11)
sort buffer

eclplot coef ci_lower ci_upper buffer, ///
	scheme(s1mono) ///
	graphregion(fcolor(white)) ///
	bgcolor(white) ///
	ylabel(,nogrid) ///
	eplottype(scatter) ///
	estopts(mcolor(cranberry)) ///
	ciopts(blcolor(cranberry)) ///
	rplottype(rcap) ///
	nociforeground ///
	xline(0,lpattern(dash) lcolor(gs11)) ///
	yline(0,lpattern(dash) lcolor(gs11)) ///
	xlabel(0(2)10) ///
	ylabel(-10(5)5) ///
	yscale(range(-11 5)) ///
	ytitle("") ///
	xtitle(Distance from Exposed Tract) ///
	title(New small business loans, size(large)) 
