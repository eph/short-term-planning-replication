from models import single_agent_models, finite_horizon_phibar

import numpy as np
import pandas as p

k_results = []
for model in single_agent_models:
    model.load()
    df_k = model.load_estimates()
    k_results.append(df_k)

finite_horizon_phibar.load()
df_het = finite_horizon_phibar.load_estimates()
k_results.append(df_het)
results_k = p.concat(k_results, 
                     keys=[model.name for model in single_agent_models]+[r'FHP-$\bar\phi$ Het. Agent'])
                                     
mdd_table = results_k.groupby(level=[0,1]).mean().groupby(level=0).agg([np.mean, np.std]).round(2).logmdd.to_latex(escape=False)
     

with open('figures-tables/single-agent-table.tex', 'w') as f:
    f.write(mdd_table)

print(mdd_table)



