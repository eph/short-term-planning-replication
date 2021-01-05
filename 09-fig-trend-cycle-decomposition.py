from models import finite_horizon_phibar
from figures import saved_figure, add_rec_bars, data

import pandas as p 

finite_horizon_phibar.load()
linear_model = finite_horizon_phibar.linear_model()
parasim = finite_horizon_phibar.load_estimates()


nsim = 250

filts = p.DataFrame()
for i in range(nsim):
    p0 = parasim.iloc[i][finite_horizon_phibar.parameters()]
    filt = linear_model.kf_everything(p0,shocks=False)['smoothed_means']
    filt['ytilde'] = filt.y - filt.ybar
    filt['trend'] = np.arange(1, filt.shape[0]+1)
    filt['yobs'] = p0[2]*filt.trend + filt.ybar
    filt['ygrobs'] = p0[2] + filt.ybar.diff()
    filt['pibarobs'] = 4*filt.pibar + p0[1]
    filt['ibarobs'] = 4*filt.ibar + p0[1] + p0[0]
    filt['realibarobs'] = filt.ibarobs - filt.pibarobs
    filts = filts.append(filt)


filts['ytrend'] = filts.y - filts.ybar
filts['itrend'] = filts.i - filts.ibar
filts['pitrend'] = filts.ppi - filts.pibar
q05 = filts.groupby(filts.index).quantile(0.05)
q95 = filts.groupby(filts.index).quantile(0.95)
mu = filts.groupby(filts.index).mean()
index = q05.index.to_timestamp()

with saved_figure('figures-tables/woodford_terminal_smooth_shaded.pdf', nrows=3) as (fig, ax):
    ax[0].fill_between(index, q05.pibarobs, q95.pibarobs, alpha=0.3)
    ax[0].plot(index, linear_model.yy.infl,color='black', alpha=0.8,linewidth=1)
     
    ax[1].fill_between(index, q05.pitrend, q95.pitrend, alpha=0.3)
    ax[1].axhline(0, color='black', alpha=0.3)
     
    ax[0].set_title(r'$\pi^A + \bar \pi_t^A$', fontsize=18, usetex=True)
    ax[1].set_title(r'$\pi_t^A - \bar \pi_t^A$', fontsize=18, usetex=True)
     
     
    # ptr = p.read_csv('data/raw/inflexp.txt',names=['date','ptr'],delim_whitespace=True).ptr
    # ptr.index = p.period_range(start='1964Q2',freq='Q', periods=ptr.shape[0])
    # ptr.fillna(method='ffill').plot(ax=ax[2],color='black',linestyle='dashed')
    ax[2].fill_between(index, q05.pibarobs, q95.pibarobs, alpha=0.3)
    ax[2].set_title(r'$\pi^A + \bar\pi_t^A$ and Long Run Inflation Expectations', usetex=True, fontsize=18);
    ax[2].set_xlim('1979Q4','2007')
     
    [add_rec_bars(axi) for axi in ax.reshape(-1)]
    fig.set_size_inches(12,6.2)
    fig.tight_layout()



with saved_figure('figures-tables/woodford_terminal_smooth_shaded_i.pdf', nrows=2) as (fig, ax):
    ax[0].fill_between(index, q05.ibarobs, q95.ibarobs, alpha=0.3)
    ax[0].plot(index, linear_model.yy.int,color='black', alpha=0.8,linewidth=1)
   
    ax[1].fill_between(index, q05.itrend, q95.itrend, alpha=0.3)
    ax[1].axhline(0, color='black', alpha=0.3)
   
    ax[0].set_title(r'$\pi^A + r^A + \bar i_t^A$', fontsize=18, usetex=True)
    ax[1].set_title(r'$i_t^A - \bar i_t^A$', fontsize=18, usetex=True)
   
    [add_rec_bars(axi) for axi in ax.reshape(-1)]


with saved_figure('figures-tables/woodford_terminal_y_level.pdf', nrows=2) as (fig,ax):
  ax = ax[::-1]
  mu = filts.groupby(filts.index).mean()
  q05 = filts.groupby(filts.index).quantile(0.05)
  q95 = filts.groupby(filts.index).quantile(0.95)
  ax[1].fill_between(q05.index.to_timestamp(), q05.ytilde, q95.ytilde, alpha=0.4)
  ax[1].plot(q05.index.to_timestamp(), 100*data['xgap']['1966':'2007'].values, color='black')
  ax[1].set_title(r"$y_t - \bar y_t$", fontsize=18, usetex=True)

  (linear_model.yy.ygr.cumsum()-filts.groupby(filts.index).ytilde.mean()).plot(ax=ax[0])
  (linear_model.yy.ygr.cumsum()).plot(ax=ax[0],linestyle='dashed')

  ax[0].legend([r'Trend Output', r'Actual Output'], fontsize=18);
  ax[0].set_title("Trend Output Level", fontsize=18)
  ax[0] = add_rec_bars(ax[0])
  ax[1] = add_rec_bars(ax[1])

  ax[1].legend([r'CBO Output Gap',r'Model Output Gap'], fontsize=18, loc='lower left')

  fig.set_size_inches(15,5.8)
  fig.tight_layout()


