from models import (canonical_NK,
                   finite_horizon,
                   finite_horizon_phibar,
                   finite_horizon_gamma,
                   trends,
                   angeletos_lian,
                   habits,
                   habits_lampi)


from figures import latex
import pandas as p 

model_dict = {
'forward': canonical_NK,
'both': finite_horizon,
'both_terminal': finite_horizon_phibar,
'both_gam': finite_horizon_gamma,
'habits_restricted': habits,
'habits_restricted_y': habits_lampi,
'angeletos': angeletos_lian,
}


for fout, model in model_dict.items():
    model.load()
    results = model.load_estimates()
    file_name = 'figures-tables/appendix-posterior-table-%s.tex' % fout
    with open(file_name, 'w') as f:
        mu = results.mean()
        q05 = results.quantile(0.05)
        q95 = results.quantile(0.95)
        std_mu = results.groupby(level=0).mean().std()
        neff = results.var() / std_mu**2

        resi = p.concat([mu, std_mu, q05, q95, neff], keys=['Mean', 'Std(Mean)', 'Q05', 'Q95', 'Neff'], axis=1)
        tbl = (resi.reindex(model.parameters())
               .rename(index=latex)
               .dropna(how='all')
               .round(2)
               .to_latex(na_rep='', escape=False, multicolumn_format='c'))

        f.write(tbl)




model_list = [
    finite_horizon_phibar,
    habits,
    habits_lampi
]
import numpy as np
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
    .agg([np.mean, np.median, np.std])
    .stack(level=-1)
    .T.round(2)
    .reindex(all_parameters)
    .rename(index=latex)
    .dropna(how="all")
    .xs([m.name for m in model_list], axis=1)
    .round(2)
    .rename(columns={"mean": "Mean", "median": "Median", "std": "SD"}, level=1)
    .to_latex(na_rep="", escape=False, multicolumn_format="c")
)

with open("figures-tables/appendix-FH-habits-posterior-table.tex", "w") as f: 
    f.write(tbl)

print(tbl)
