from models import finite_horizon_phibar
from figures import saved_figure

finite_horizon_phibar.load()
priosim = finite_horizon_phibar.load_estimates(posterior='prior')
parasim = finite_horizon_phibar.load_estimates()

with saved_figure('figures-tables/rho_gamma_scatter.pdf') as (fig, ax):
    ax.scatter(parasim.gamma.iloc[:500], parasim.rho.iloc[:500], alpha=0.3)
    ax.scatter(priosim.gamma.iloc[:500], priosim.rho.iloc[:500], alpha=0.2,color='grey')
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.set_xlabel(r'$\gamma$',fontsize=16, usetex=True);
    ax.set_ylabel(r'$\rho$',fontsize=16, usetex=True);

