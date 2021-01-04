from models import finite_horizon_phibar
from figures import saved_figure

import pandas as p 

finite_horizon_phibar.load()
linear_model = finite_horizon_phibar.linear_model()
parasim = finite_horizon_phibar.load_estimates()

nsim = 250
shock = 'epsi'
irfs = p.DataFrame()
for i in range(nsim):
    p0 = parasim.iloc[i][finite_horizon_phibar.parameters()]
    irf = linear_model.impulse_response(p0)[shock]
    irfs = irfs.append(irf)


fout = 'figures-tables/woodford_terminal_irf_%s_shaded.pdf' % shock
with saved_figure(fout, nrows=3, ncols=3) as (fig,ax):
    irfs['ytrend'] = irfs.y - irfs.ybar
    irfs['itrend'] = irfs.i - irfs.ibar
    irfs['pitrend'] = irfs.ppi - irfs.pibar
    q05 = irfs.groupby(irfs.index).quantile(0.05)
    q95 = irfs.groupby(irfs.index).quantile(0.95)
    mu = irfs.groupby(irfs.index).mean()


    ax[0,0].fill_between(q05.index, q05.y, q95.y, alpha=0.3)
    ax[0,0].plot(q05.index, mu.y)
    ax[0,1].fill_between(q05.index, 4*q05.ppi, 4*q95.ppi, alpha=0.3)
    ax[0,1].plot(q05.index, 4*mu.ppi)
    ax[0,2].fill_between(q05.index, 4*q05.i, 4*q95.i, alpha=0.3)
    ax[0,2].plot(q05.index, 4*mu.i)

    ax[1,0].fill_between(q05.index, q05.ybar, q95.ybar, alpha=0.3)
    ax[1,0].plot(q05.index, mu.ybar)
    ax[1,1].fill_between(q05.index, 4*q05.pibar, 4*q95.pibar, alpha=0.3)
    ax[1,1].plot(q05.index, 4*mu.pibar)
    ax[1,2].fill_between(q05.index, 4*q05.ibar, 4*q95.ibar, alpha=0.3)
    ax[1,2].plot(q05.index, 4*mu.ibar)

    ax[2,0].fill_between(q05.index, q05.ytrend, q95.ytrend, alpha=0.3)
    ax[2,0].plot(q05.index, mu.ytrend)
    ax[2,1].fill_between(q05.index, 4*q05.pitrend, 4*q95.pitrend, alpha=0.3)
    ax[2,1].plot(q05.index, 4*mu.pitrend)
    ax[2,2].fill_between(q05.index, 4*q05.itrend, 4*q95.itrend, alpha=0.3)
    ax[2,2].plot(q05.index, 4*mu.itrend)

    fig.set_size_inches(12,9)
    [axi.axhline(0, color='black', alpha=0.3) for axi in ax.reshape(-1)]
    [axi.set_xlim(0,20) for axi in ax.reshape(-1)]
    [axi.set_xticks([0,2,4,6,8,10,12,14,16,18,20]) for axi in ax.reshape(-1)]
    ax[0,0].set_title(r'$y_t$', fontsize=18, usetex=True)
    ax[0,1].set_title(r'$\pi_t^A$', fontsize=18, usetex=True);
    ax[0,2].set_title(r'$i_t^A$', fontsize=18, usetex=True);

    ax[1,0].set_title(r'$\bar y_t$', fontsize=18, usetex=True)
    ax[1,1].set_title(r'$\bar \pi_t^A$', fontsize=18, usetex=True)
    ax[1,2].set_title(r'$\bar i_t^A$', fontsize=18, usetex=True)

    ax[2,0].set_title(r'$y_t - \bar y_t$', fontsize=18, usetex=True)
    ax[2,1].set_title(r'$\pi_t^A - \bar \pi_t^A$', fontsize=18, usetex=True)
    ax[2,2].set_title(r'$i_t^A - \bar i_t^A$', fontsize=18, usetex=True)
    fig.tight_layout()

