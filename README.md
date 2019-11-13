# Student Project – Fabian Balensiefer
## Replication Study: *"Are Credit Markets Still Local? Evidence from Bank Branch Closings"* by Hoai-Luu Q. Nguyen

<a href="https://nbviewer.jupyter.org/github/fbalensiefer/Python_SimulationStudy/blob/master/fbalensiefer.ipynb"
   target="_parent">
   <img align="center"
  src="https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.png"
      width="109" height="20">
</a>
<a href="https://mybinder.org/v2/gh/fbalensiefer/Python_SimulationStudy/blob/master/fbalensiefer.ipynb"
    target="_parent">
    <img align="center"
       src="https://mybinder.org/badge_logo.svg"
       width="109" height="20">
</a>

## Abstract
The scope of this project is to replicate the major findings from the paper "Are Credit Markets Still Local? Evidence from Bank Branch Closings" by Hoai-Luu Q. Nguyen by using Python as Data Science tool.
The paper by Nguyen 2019 studies whether distance shapes credit allocation. In other words, she tests whether a local bank branch help to get access to funding. Since opening and closing decisions for branches are not random, Nguyen uses bank merger as instrument for closings. She designed a difference-in-differences framework to estimate the local average treatment effect (LATE).
As result, Nguyen 2019 finds that distance still matters. Bank branch closings lead to a persistence decline for loans to local small business. While the effect for private lending (mortgages) is temporary.
Additionally, I create a simulated dataset to show the robustness of the identification strategy.
The paper, data and stata-code is available <a href="https://www.aeaweb.org/articles?id=10.1257/app.20170543">here</a>
## Causal graph
Causal graphs break down complex relationships into simple, transparent and easy to interpret visualizations. I create a causal graph to show this relationship in the paper’s framework. Especially, to illustrate the authors identification strategy and to discuss potential identification issues.
## Simulation Study
To further emphasize the identification strategy, I create a simulated dataset. This simulated data I later use to check the framework for causal identification of the local average treatment effect (LATE).
## References
*Akerlof, G. A. (1970). The market for lemons: Quality and the market mechanism. Quarterly. Journal Economics, 84, 488-500.*

*Angrist, J. D., & Pischke, J. S. (2008). Mostly harmless econometrics: An empiricist's companion. Princeton university press.*

*Frölich, M., & Sperlich, S. (2019). Impact evaluation. Cambridge University Press.*

*Nguyen, H. L. Q. (2019). Are credit markets still local? evidence from bank branch closings. American Economic Journal: Applied Economics, 11(1), 1-32.*

*Stiglitz, J. E., & Weiss, A. (1981). Credit rationing in markets with imperfect information. The American economic review, 71(3), 393-410.*

*Wooldridge, J. M. (2015). Introductory econometrics: A modern approach. Nelson Education.*


[![Build Status](https://travis-ci.org/fbalensiefer/Python_SimulationStudy) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](HumanCapitalAnalysis/student-project-fbalensiefer/blob/master/LICENSE)
