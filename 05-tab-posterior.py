import numpy as np
import pandas as p
from models import (
    canonical_NK,
    finite_horizon,
    finite_horizon_gamma,
    finite_horizon_phibar,
)
from fortress import load_estimates

import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


results = []


np.random.seed(1848)
for (path, model, name) in models:
    paranames = [str(para) for para in model.parameters]
    results_model = load_estimates(
        "_fortress_" + path + "/output-*", paranames=paranames
    )
    results.append(results_model)

results = p.concat(results, keys=[m[-1] for m in models])


all_parameters = [
    "rA",
    "piA",
    "yQ",
    "rho",
    "gamma",
    "gammatilde",
    "rhof",
    "lam",
    "nu",
    "a",
    "sigma",
    "kappa",
    "phipi",
    "phiy",
    "phipiLR",
    "phiyLR",
    "rhoxi",
    "rhoy",
    "rhoi",
    "sigxi",
    "sigy",
    "sigi",
    "logmdd",
]
tbl = (
    results.groupby(level=0)
    .agg([np.mean, np.std])
    .stack(level=-1)
    .T.round(2)
    .reindex(all_parameters)
    .rename(index=latex)
    .dropna(how="all")
    .xs([m[-1] for m in models], axis=1)
    .round(2)
    .rename(columns={"mean": "Mean", "std": "SD"}, level=1)
    .to_latex(na_rep="", escape=False, multicolumn_format="c")
)

f = open("figures-tables/main-posterior-table.tex", "w")
f.write(tbl)
f.close()
print(tbl)
