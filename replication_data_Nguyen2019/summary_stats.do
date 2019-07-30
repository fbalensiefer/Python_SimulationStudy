/*******************************
summary_stats.do

Code for generating Tables 1-5.
********************************/

/********************
TABLE 1: MERGER SAMPLE
*********************/

use replication_input, clear
keep acq_instname out_instname yr_approve approved
duplicates drop
sort approved
br


/*********************
TABLE 2: MERGER SUMMARY STATISTICS
**********************/

use replication_input, clear
keep mergerID premerger_acq* premerger_out*
duplicates drop
sum premerger_acq*, d
sum premerger_out*, d


/*********************
TABLE 3: SUMMARY STATISTICS FOR EXPOSED AND CONTROL TRACTS
**********************/

// Columns 1-2
use mergersample_controls, clear

egen cntyID = group(state_fps cnty_fps)

local covars poptot popdensity pminority pcollege pincome medincome ///
	pmortgage cont_totalbranches cont_brgrowth cont_total_origin ///
	cont_NumSBL_Rev1
	
scalar drop _all

foreach var in `covars' {
	sum `var' if overlap==1, d
	scalar define `var'_mean_Exp = r(mean)
	scalar define `var'_sd_Exp = r(sd)
	sum state_fps if overlap==1
	scalar define N_Exp = r(N)
	
	sum `var' if overlap==0, d
	scalar define `var'_mean_All = r(mean)
	scalar define `var'_sd_All = r(sd)
	sum state_fps if overlap==0
	scalar define N_All = r(N)
	}
	
foreach var in `covars' {
	scalar list `var'_mean_Exp
	scalar list `var'_sd_Exp
	scalar list `var'_mean_All
	scalar list `var'_sd_All
	}
	
scalar list N_Exp
scalar list N_All


//Column 3
foreach var in poptot popdensity pminority pcollege pincome medincome ///
	pmortgage cont_totalbranches cont_brgrowth cont_total_origin ///
	cont_NumSBL_Rev1 {
	
	disp "`var'"
	quietly areg `var' overlap, absorb(cntyID) robust
	if "`var'"=="poptot" {
		outreg2 overlap using covarbal_ALL.xls, ///
			replace excel ctitle("`var'") stats(coef se pval)
		}

	else {
		outreg2 overlap using covarbal_ALL.xls, ///
			append excel ctitle("`var'") stats(coef se pval)
		}
	
	}


// restrict sample to just Exposed and Control tracts
use replication_input, clear
keep state_fps cnty_fps tractstring overlap mergerID
duplicates drop
merge 1:1 state_fps cnty_fps tractstring mergerID using mergersample_controls
keep if _merge==3
drop _merge

// Column 4
egen cntyID = group(state_fps cnty_fps)

local covars poptot popdensity pminority pcollege pincome medincome ///
	pmortgage cont_totalbranches cont_brgrowth cont_total_origin ///
	cont_NumSBL_Rev1 

scalar drop _all

foreach var in `covars' {
	sum `var' if overlap==0, d
	scalar define `var'_mean_Con = r(mean)
	scalar define `var'_sd_Con = r(sd)
	sum state_fps if overlap==0
	scalar define N_Con = r(N)
	}
	
foreach var in `covars' {
	scalar list `var'_mean_Con
	scalar list `var'_sd_Con
	}
	
scalar list N_Con

// Column 5
foreach var in poptot popdensity pminority pcollege pincome medincome ///
	pmortgage cont_totalbranches cont_brgrowth cont_total_origin ///
	cont_NumSBL_Rev1 {
	
	disp "`var'"
	quietly areg `var' overlap, absorb(cntyID) robust
	if "`var'"=="poptot" {
		outreg2 overlap using covarbal.xls, ///
			replace excel ctitle("`var'") stats(coef se pval)
		}

	else {
		outreg2 overlap using covarbal, ///
			append excel ctitle("`var'") stats(coef se pval)
		}
	
	}


/*********************
TABLE 4: REPRESENTATIVENESS OF THE MERGER SAMPLE
**********************/

local covars poptot popdensity pminority pcollege pincome medincome ///
	pmortgage totalbranches brgrowth total_origin NumSBL_Rev1 	
	
scalar drop _all

** All US tracts that were branched at some point 2002-2007
use alltract_controls, clear
keep if year>=2002 & year<=2007
collapse (max) totalbranches, by(state_fps cnty_fps tractstring)
keep if totalbranches>0
keep state_fps cnty_fps tractstring
tempfile temptracts
save "`temptracts'", replace

use alltract_controls, clear
merge m:1 state_fps cnty_fps tractstring using "`temptracts'"
keep if _merge==3
drop _merge

keep if year==2001

foreach var in `covars' {
	sum `var', d
	scalar define `var'_mean_ALL = r(mean)
	scalar define `var'_sd_ALL = r(sd)
	}
	
sum state_fps
scalar define N_ALL = r(N)

** All branched tracts that experienced a closing at some point 2002-2007
use alltract_controls, clear
keep if year>=2002 & year<=2007
collapse (max) num_closings, by(state_fps cnty_fps tractstring)
keep if num_closings>0
keep state_fps cnty_fps tractstring
tempfile temptracts
save "`temptracts'", replace

use alltract_controls, clear
merge m:1 state_fps cnty_fps tractstring using "`temptracts'"
keep if _merge==3
drop _merge

keep if year==2001

foreach var in `covars' {
	sum `var', d
	scalar define `var'_mean_CLOSE = r(mean)
	scalar define `var'_sd_CLOSE = r(sd)
	}
	
sum state_fps
scalar define N_CLOSE = r(N)
	

** All tracts in the merger sample
use replication_input, clear
keep state_fps cnty_fps tractstring
duplicates drop
tempfile tempsample
save "`tempsample'", replace

use alltract_controls, clear
keep if year==2001
merge 1:1 state_fps cnty_fps tractstring using "`tempsample'"
keep if _merge==3

foreach var in `covars' {
	sum `var', d
	scalar define `var'_mean_SAMPLE = r(mean)
	scalar define `var'_sd_SAMPLE = r(sd)
	}
	
sum state_fps
scalar define N_SAMPLE = r(N)


** List all table entries
foreach var in `covars' {
	scalar list `var'_mean_ALL
	scalar list `var'_sd_ALL
	scalar list `var'_mean_CLOSE
	scalar list `var'_sd_CLOSE
	scalar list `var'_mean_SAMPLE
	scalar list `var'_sd_SAMPLE
	}
	
scalar list N_ALL
scalar list N_CLOSE
scalar list N_SAMPLE


/************************
TABLE 5: COMPLIER CHARACTERISTICS
*************************/

local covars poptot popdensity pminority pcollege pincome medincome ///
	pmortgage cont_totalbranches cont_brgrowth cont_total_origin ///
	cont_NumSBL_Rev1

use replication_input, clear

scalar drop _all

gen event_year = year-yr_approve

keep if event_year==1


** calculate variable for being above the median for each variable
foreach var in `covars' {
	sum `var', d
	scalar define `var'_mean = r(mean)
	scalar define `var'_median = r(p50)
	gen `var'_above = (`var'>r(p50))
	}


** percentages for compliers
// ESTIMATE PROPORTION OF ALWAYS TAKERS 
// among Control tracts, how many still had closings in the
// merger year?
sum closed_branch if overlap==0
scalar define p_always = r(mean)
scalar list p_always

// ESTIMATE PROPORTION OF NEVER TAKERS
// among Treatment tracts, how many did NOT have any closings
// in the merger year?
gen temp = 1-closed_branch
sum temp if overlap==1
scalar define p_never = r(mean)
scalar list p_never
drop temp

// ESTIMATE PROPORTION OF COMPLIERS
// P(complier) = 1 - P(always taker) - P(never taker)
scalar define p_comp = 1 - p_always - p_never
scalar list p_comp

// ESTIMATE AVERAGE CHARACTERISTICS OVER SET OF ALWAYS TAKERS AND
// COMPLIERS COMBINED (i.e., Treatment tracts who had closings)
foreach var in `covars' {
	sum `var'_above if overlap==1 & closed_branch==1
	scalar define EZ1D1_`var' = r(mean)
	}

// ESTIMATE AVERAGE CHARACTERISTICS OVER ALWAYS TAKERS ONLY
// (i.e., Control tracts who had closings)
foreach var in `covars' {
	sum `var'_above if overlap==0 & closed_branch==1
	scalar define EZ0D1_`var' = r(mean)
	}

// ESTIMATE AVERAGE CHARACTERISTICS FOR COMPLIERS
foreach var in `covars' {
	scalar define Ecomp_`var' = ((p_always+p_comp)/p_comp)* ///
		(EZ1D1_`var'-((p_always/(p_always+p_comp))*EZ0D1_`var'))
	}

// CALCULATE RATIO
foreach var in `covars' {
//	scalar define ratio_`var' = Ecomp_`var' / overlap_`var'
	scalar define ratio_`var' = Ecomp_`var' / 0.50
	}

foreach var in `covars' {
	scalar list `var'_mean
	scalar list `var'_median
	scalar list Ecomp_`var'
	scalar list ratio_`var'
	}
