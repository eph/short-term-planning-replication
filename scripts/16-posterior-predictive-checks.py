from models import (
    finite_horizon_phibar,
    habits,
    habits_lampi
    )
from figures import saved_figure
import pandas as p

model_list = [
    finite_horizon_phibar,
    habits,
    habits_lampi
]
pred_checks = {}
for model in model_list:
    model.load()
    results = model.load_estimates()
    linmod = model.linear_model()

    df_results = [] 
    for i in range(200):

        p0 = results[model.parameters()].iloc[i]
        yylong = linmod.simulate(p0, 168)

        df = p.DataFrame(yylong,columns=linmod.yy.columns)
        covs = df.rename(columns={c:'Cov['+c+']' for c in linmod.yy.columns}).var().to_dict()
        corrs = {'Cov[ygr,infl]': df.corr().ygr.infl,
                 'Cov[ygr,int]': df.corr().ygr.int,
                 'Cov[infl,int]': df.corr().infl.int}

        autocorrs = {'ACF[%s]' %c : df[c].autocorr() for c in df.columns}

        covs.update(corrs)
        covs.update(autocorrs)
        df_results.append(covs)

    pred_checks[model.name] = p.DataFrame(df_results)

df = linmod.yy
truth = df.rename(columns={c:'Cov['+c+']' for c in linmod.yy.columns}).var().to_dict()
corrs = {'Cov[ygr,infl]': df.corr().ygr.infl,
         'Cov[ygr,int]': df.corr().ygr.int,
         'Cov[infl,int]': df.corr().infl.int}

autocorrs = {'ACF[%s]' %c : df[c].autocorr() for c in df.columns}

truth.update(corrs)
truth.update(autocorrs)
  
with saved_figure('figures-tables/posterior-predictive-checks.pdf', nrows=1, ncols=3) as (fig,ax):
    keys = {'Cov[ygr]': 'Variance of Output Growth',
            'Cov[ygr,infl]': 'Corr. of Output Growth and Inflation',
            'ACF[ygr]': '1st Autocorr. of Output Growth'}
    for axi,col in zip(ax.reshape(-1), keys.keys()):
        [pred_checks[key][col].plot(kind='kde',ax=axi,style=style) for key,style in zip(pred_checks.keys(),['--','-.','-'])]
        axi.axvline(truth[col],color='black')
        axi.set_title(keys[col])

    ax[0].legend(list(pred_checks.keys()) + ['Data'], 
                 ncol=4,frameon=False,loc=(0.15,-0.17))

    fig.set_size_inches(9,3)
    #fig.tight_layout()
    fig.subplots_adjust(bottom=0.12)

