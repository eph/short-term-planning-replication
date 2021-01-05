from models import finite_horizon_phibar
from figures import saved_figure

import numpy as np 
import pandas as p 

finite_horizon_phibar.load()
linear_model = finite_horizon_phibar.linear_model()
parasim = finite_horizon_phibar.load_estimates()

nsim = 250

filts = p.DataFrame()
for i in range(nsim):
    p0 = parasim.iloc[i][finite_horizon_phibar.parameters()]
    filt = linear_model.kf_everything(p0,shocks=False)['smoothed_means']
    filts = filts.append(filt)

q05 = filts.groupby(filts.index).quantile(0.05)
q95 = filts.groupby(filts.index).quantile(0.95)
mu = filts.groupby(filts.index).mean()
index = q05.index.to_timestamp()

with saved_figure('figures-tables/shock_series.pdf', nrows=1, ncols=3) as (fig,ax):
     for (axi, plotvar) in zip(ax.reshape(-1), ['xi', 'istar', 'ystar']):
         axi.fill_between(index, q05[plotvar], q95[plotvar], alpha=0.3)
         axi.plot(index, mu[plotvar].values)

     fig.set_size_inches(14,3);
     ax[0].set_title(r'$\xi_t$', fontsize=19, usetex=True)
     ax[1].set_title(r'$i^*_t$', fontsize=19, usetex=True)
     ax[2].set_title(r'$y^*_t$', fontsize=19, usetex=True)
     fig.tight_layout()

