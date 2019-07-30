/*******************************
master_run.do

Master do-file for replicating the results from "Are Credit Markets Still Local?
Evidence from Bank Branch Closings"
********************************/

** Install necessary packages
ssc install outreg2
ssc install regsave
ssc install reghdfe
ssc install eclplot
ssc install ivreg2
ssc install ranktest


** Summary statistics: Tables 1-5
do summary_stats.do


** Main results: Figures 2-5, Tables 6-7
do main_results.do


** Extensions: Figure 6, Tables 8-9
do extensions.do


** Spillovers: Figure 7
do spillovers.do

