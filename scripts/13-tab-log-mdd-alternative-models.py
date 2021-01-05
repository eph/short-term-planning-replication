from models import (
    canonical_NK,
    trends,
    finite_horizon,
    finite_horizon_gamma,
    finite_horizon_phibar,
    angeletos_lian,
    habits,
    habits_lampi,
)

import numpy as np
import pandas as p

model_list = [
    canonical_NK,
    trends,
    finite_horizon,
    finite_horizon_gamma,
    finite_horizon_phibar,
    angeletos_lian,
    habits,
    habits_lampi
]

results = []
np.random.seed(1848)
for model in model_list:
    model.load()
    results_model = model.load_estimates()
    results.append(results_model)
results = p.concat(results, keys=[m.name for m in model_list])

mdd_table = (results.groupby(level=[0,1]).mean()
             .groupby(level=0).agg([np.mean, np.std])
             .round(2).logmdd
             .rename(columns={'mean': 'Mean', 'std': 'Std. Dev.'})
             .to_latex(escape=False))

with open('figures-tables/other-nk-mdd-table.tex', 'w') as f:
    f.write(mdd_table)

print(mdd_table)

