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
    #.rename(index=latex)
    .dropna(how="all")
    .xs([m.name for m in model_list], axis=1)
    .round(2)
    .rename(columns={"mean": "Mean", "std": "SD"}, level=1)
    #.to_latex(na_rep="", escape=False, multicolumn_format="c") new table format
)

with open("figures-tables/main-posterior-table.tex", "w") as f: 
    f.write("\\begin{tabular}{lccccc}\n\\toprule\n")
    f.write(''.join([''] + ['& %s ' % m.name for m in model_list]) + '\\\\ \n')
    for para in all_parameters:
        try: 
            mu = ['%20s' % latex[para]] + [(' &  %5.2f  ' % _).replace('NaN','') for _ in tbl.loc[para].unstack().Mean]
            sd = ['%20s' % ''] + [(' & (%5.2f) ' % _).replace('NaN','') for _ in tbl.loc[para].unstack().SD]
            f.write(''.join(mu) + '\\\\  \n' + ''.join(sd) + '\\\\ [0.25em] \n')
        except:
            pass
        
    f.write('\\bottomrule\n\\end{tabular}')

print(tbl)
