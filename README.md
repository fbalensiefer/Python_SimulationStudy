# Student Project – Fabian Balensiefer
## Replication Study: *"Are Credit Markets Still Local? Evidence from Bank Branch Closings"* by Hoai-Luu Q. Nguyen

<a href="https://nbviewer.jupyter.org/github/HumanCapitalAnalysis/student-project-fbalensiefer/blob/master/fbalensiefer.ipynb"
   target="_parent">
   <img align="center"
  src="https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.png"
      width="109" height="20">
</a>
<a href="https://mybinder.org/v2/gh/HumanCapitalAnalysis/student-project-fbalensiefer/master?filepath=fbalensiefer.ipyn"
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
The paper, data and stata-code is available at: <a href="https://www.aeaweb.org/articles?id=10.1257/app.20170543">here</a>
## Causal Tree
Causal trees break down complex relationships into simple, transparent and easy to interpret graphs. I create a causal tree to show this relationship in the paper’s framework. Especially, to illustrate the authors identification strategy and to discuss potential identification issues.
## Simulation Study
To further emphasize the identification strategy, I create a simulated dataset. This simulated data I later use to check the framework for causal identification of the local average treatment effect (LATE).
## References
*Degryse, H., & Ongena, S. (2005). Distance, lending relationships, and competition. The Journal of Finance, 60(1), 231-266.*

*Frölich, M., & Sperlich, S. (2019). Impact evaluation. Cambridge University Press.*

*Nguyen, H. L. Q. (2019). Are credit markets still local? evidence from bank branch closings. American Economic Journal: Applied Economics, 11(1), 1-32.*

*Petersen, M. A., & Rajan, R. G. (2002). Does distance still matter? The information revolution in small business lending. The journal of Finance, 57(6), 2533-2570.*

*Wooldridge, J. M. (2015). Introductory econometrics: A modern approach. Nelson Education.*


[![Build Status](https://travis-ci.org/HumanCapitalAnalysis/student-project-fbalensiefer.svg?branch=master)](https://travis-ci.org/HumanCapitalAnalysis/student-project-fbalensiefer) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](HumanCapitalAnalysis/student-project-fbalensiefer/blob/master/LICENSE)
