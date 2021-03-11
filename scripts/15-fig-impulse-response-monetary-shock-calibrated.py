from models import finite_horizon_phibar
from figures import saved_figure

finite_horizon_phibar.load()
linear_model = finite_horizon_phibar.linear_model()


p0 = finite_horizon_phibar.model.p0()

p1 = p0.copy()
p1[3] = 0.5
p1[-4:-2] = [0.5,0.5]

p2 = p1.copy()
p2[-4:-2] = [0.15, 0.15]


irf0 = linear_model.impulse_response(p0)
irf1 = linear_model.impulse_response(p1)
irf2 = linear_model.impulse_response(p2)

irfs = [irf1, irf2, irf0]


shock = 'epsi'
with saved_figure('figures-tables/example_irf_epsi.pdf', nrows=3, ncols=3) as (fig, ax): 
    [(irf[shock]['y']).plot(ax=ax[0,0],linewidth=3,style=style) for irf,style in zip(irfs,['--','-.','-'])]
    [(4*irf[shock]['ppi']).plot(ax=ax[0,1],kind='line',linewidth=3,style=style) for irf,style in zip(irfs,['--','-.','-'])]
    [(4*irf[shock]['i']).plot(ax=ax[0,2],linewidth=3,style=style) for irf,style in zip(irfs,['--','-.','-'])]

    [irf[shock].ybar.plot(ax=ax[1,0],linewidth=3,style=style) for irf,style in zip(irfs,['--','-.','-'])]
    [(4*irf[shock].pibar).plot(ax=ax[1,1],linewidth=3,style=style) for irf,style in zip(irfs,['--','-.','-'])]
    [(4*irf[shock].ibar).plot(ax=ax[1,2],linewidth=3,style=style) for irf,style in zip(irfs,['--','-.','-'])]

    [(irf[shock]['y']-irf[shock].ybar).plot(ax=ax[2,0],linewidth=3,style=style) for irf,style in zip(irfs,['--','-.','-'])]
    [(4*(irf[shock]['ppi']-irf[shock].pibar)).plot(ax=ax[2,1],linewidth=3,style=style) for irf,style in zip(irfs,['--','-.','-'])]
    [(4*(irf[shock]['i']-irf[shock].ibar)).plot(ax=ax[2,2],linewidth=3,style=style) for irf,style in zip(irfs,['--','-.','-'])]

    fig.set_size_inches(12,9)
    [axi.axhline(0, color='black', alpha=0.3) for axi in ax.reshape(-1)]
    ax[2,0].set_title(r'$y_t - \bar y_t$', fontsize=16,usetex=True)
    ax[2,1].set_title(r'$\pi_t^A - \bar \pi_t^A$', fontsize=16, usetex=True)
    ax[2,2].set_title(r'$i_t^A - \bar i_t^A$', fontsize=16, usetex=True)
    ax[1,0].set_title(r'$\bar y_t$', fontsize=16, usetex=True)
    ax[1,1].set_title(r'$\bar \pi_t^A$', fontsize=16, usetex=True)
    ax[1,2].set_title(r'$\bar i_t^A$', fontsize=16, usetex=True)
    ax[0,0].set_title(r'$y_t$', fontsize=16, usetex=True)
    ax[0,1].set_title(r'$\pi_t^A$', fontsize=16, usetex=True)
    ax[0,2].set_title(r'$i_t^A$', fontsize=16, usetex=True)

    ax[0,0].legend(['Large Gain', 'Small Gain', 'Canonical NK'], loc='lower right', fontsize=14)
    [axi.set_xlim(0,20) for axi in ax.reshape(-1)]
    fig.tight_layout()
 

