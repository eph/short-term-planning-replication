from models import finite_horizon_phibar





     fig, ax = plt.subplots(nrows=1,ncols=3)

     for (axi, plotvar) in zip(ax.reshape(-1), ['xi', 'istar', 'ystar']):#, 'v_epsxi', 'v_epsi', 'v_epsy']):
         (states['smoothed_means'][plotvar]).plot(ax=axi)


     fig.set_size_inches(14,3);
     ax[0].set_title(r'$\xi_t$', fontsize=19, usetex=True)
     ax[1].set_title(r'$i^*_t$', fontsize=19, usetex=True)
     ax[2].set_title(r'$y^*_t$', fontsize=19, usetex=True)
     fig.tight_layout()
     plt.savefig('figures-tables/shock_series.pdf')
