from models import (
    canonical_NK,
    trends,
    finite_horizon,
    finite_horizon_gamma,
    finite_horizon_phibar,
)
from figures import latex

import numpy as np
import pandas as p

model_list = [
    canonical_NK,
    trends,
    finite_horizon,
    finite_horizon_gamma,
    finite_horizon_phibar
]

results = []
np.random.seed(1848)
for model in model_list:
    model.load()
    results_model = model.load_estimates()
    results.append(results_model)

results = p.concat(results, keys=[m.name for m in model_list])

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
    .xs([m.name for m in model_list], axis=1)
    .round(2)
    .rename(columns={"mean": "Mean", "std": "SD"}, level=1)
    .to_latex(na_rep="", escape=False, multicolumn_format="c")
)

f = open("figures-tables/main-posterior-table.tex", "w")
f.write(tbl)
f.close()
print(tbl)
