from models import finite_horizon_phibar
from figures import saved_figure

import numpy as np 
import pandas as p 

finite_horizon_phibar.load(add_shocks=True,add_hats=True)
linear_model = finite_horizon_phibar.linear_model()
parasim = finite_horizon_phibar.load_estimates()

p0 = parasim[finite_horizon_phibar.parameters()].mean()
CC, TT, RR, QQ, DD, ZZ, HH = linear_model.system_matrices(p0)
states = linear_model.kf_everything(p0,shocks=False)


init = 1


shocks = states['smoothed_means'][['v_epsxi', 'v_epsi', 'v_epsy']].values
dfs = []
for i, shock in enumerate(linear_model.shock_names):
    T, ns = states['smoothed_means'].shape
    previous = np.zeros((len(linear_model.state_names)))

    decomp = np.zeros_like(states['smoothed_means'].values)
    for j in range(init,T):
        decomp[j] = TT @ decomp[j-1] + RR[:,i] * shocks[j,i]


    dfs.append(p.DataFrame(decomp, 
               index=linear_model.yy.index, 
               columns=linear_model.state_names))

decomp = np.zeros_like(states['smoothed_means'].values)
decomp[init-1] = states['smoothed_means'].values[init-1]
for j in range(init,T):
    decomp[j] = TT @ decomp[j-1] 

dfs.append(p.DataFrame(decomp, 
           index=linear_model.yy.index, 
           columns=linear_model.state_names))


shock_decomposition = p.concat(dfs, keys=linear_model.shock_names+['Initial Condition'])

with saved_figure('figures-tables/shock_decomposition.pdf', nrows=2, ncols=2) as (fig, ax):
    from itertools import cycle
    lines = cycle(['--','-.',':','--'])


    ax[0,0].set_title(r'$y - \bar y_t$')
    fig.set_size_inches(16,8);
    ax[0,0].set_title(r'$y_t - \bar y_t$', fontsize=24, usetex=True)
    ax[1,0].set_title(r'$\bar y_t$', fontsize=24, usetex=True)
    ax[0,1].set_title(r'$\pi_t^A - \bar \pi_t^A$', fontsize=24, usetex=True)
    ax[1,1].set_title(r'$\bar \pi_t^A$', fontsize=24, usetex=True)

    for (axi, plotvar) in zip(ax.reshape(-1), ['yhat', 'pihat', 'ybar', 'pibar']):
        if 'pi' in plotvar:
            [(4*shock_decomposition.xs(v)[plotvar]).plot(ax=axi,linestyle=next(lines)) 
             for v in shock_decomposition.index.levels[0]]
            (4*states['smoothed_means'][plotvar]).plot(ax=axi, color='black')
        else:
            [shock_decomposition.xs(v)[plotvar].plot(ax=axi,linestyle=next(lines)) 
             for v in shock_decomposition.index.levels[0]]
            (states['smoothed_means'][plotvar]).plot(ax=axi, color='black')


    fig.tight_layout()
    ax[0,0].legend([r'Demand', r'Monetary Policy', r'Supply', r'Initial Condition', r'Total'], fontsize=14, loc='lower right')



