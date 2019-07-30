/*******************************
execute_yearbyyear.do

Code to estimate Equation 3.

The syntax to call execute_yearbyyear.do from another do-file is:

do execute_yearbyyear.do `min' `max' `outcome' `output' `first' `agg'

where

(1) `min' = minimum event time
(2) `max' = maximum event time
(3) `outcome' = outcome variable
(4) `output' = name for output file name
(5) `first' = name for first outcome variable
(6) `agg' = level of aggregation

********************************/

local drop = abs(`1')+abs(`2')
local abs_min = abs(`1')


/******************
CONTROL VARIABLES
*******************/

if "`6'"=="tract" {
	local controls poptot* popdensity* pminority* pcollege* ///
	medincome* cont_totalbranches* cont_brgrowth*
	}


/*******************
BASELINE SPECIFICATIONS
********************/

reghdfe `3' edum* `controls', absorb(indivID group_timeID) vce(cluster clustID)

if "`3'"=="`5'" {
	outreg2 edum* using "`4'.xls", ///
		replace label excel ctitle("`3'")
	}
else {
	outreg2 edum* using "`4'.xls", ///
		append label excel ctitle("`3'")
	}


**keep outputs of interest and save in an intermediate data file
regsave, tstat pval ci
drop if _n > `drop'
gen tau = real(substr(var,5,.)) - `abs_min'
gen outcome = "`3'"
if "`3'"=="`5'" {
	save "`4'", replace
	}
else {
	append using "`4'"
	save "`4'", replace
	}

