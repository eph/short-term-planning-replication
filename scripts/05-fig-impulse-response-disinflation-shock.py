from models import finite_horizon_phibar
from figures import saved_figure

import numpy as np
from numpy.linalg import matrix_power

finite_horizon_phibar.load(add_shocks=True)
linear_model = finite_horizon_phibar.linear_model()

# Calibration -- see Table 3
p0 = [2.39, #rA
      3.80, # piA
      0.45, # yQ
      0.46, # rho
      0.03, # kappa                                                          
      3.72, # sigma                                                          
      0.94, # rule coefficient on dp                                         
      0.75, # rule coefficient on y                                          
      2.08, # demand shock std                                              
      5.99, # suppy shock std                                               
      0.58, # mon shock std                                                 
      0.97, # demand shock persistence                                      
      0.97, # monetary shock persistence                                    
      0.57, # supply shock persistence                                      
      0.11, # learning parameter for HHs/Firms                                     
      2.09, # LR coeff of rule on dp                                         
      0.05  # LR coeff of rule on y                                          
      ]

# Here we change the monetary policy rule to Taylor (1993)
p0[6] = 1.5
p0[7] = 0.125
p0[15] = p0[6]
p0[16] = p0[7]
p0[12] = 0.9999
p0[10] = 0.5/4  #shock size

T = 20                          # horizon of IRF
fh_irf = linear_model.impulse_response(p0, T)['epsi']
fh_TT, fh_RR, fh_unique = linear_model.solve_LRE(p0)

p0[14] = 0.5
fh_large_gain_irf = linear_model.impulse_response(p0, T)['epsi']
fh_large_gain_TT, fh_large_gain_RR, fh_large_gain_unique = linear_model.solve_LRE(p0)

p0[3] = 1.0
re_irf = linear_model.impulse_response(p0, T)['epsi']
re_TT, re_RR, re_unique = linear_model.solve_LRE(p0) 

fh_TT_T = matrix_power(fh_TT,T+1)
fh_large_gain_TT_T = matrix_power(fh_large_gain_TT,T+1)
re_TT_T = matrix_power(re_TT,T+1)

fh_Epi = np.zeros(T+1)
fh_large_gain_Epi = np.zeros(T+1)
re_Epi = np.zeros(T+1)
for tt in np.arange(T+1):
    y0 = np.array(fh_irf.loc[tt])
    yT = fh_TT_T @ y0
    fh_Epi[tt] = yT[1] 

    y0 = np.array(fh_large_gain_irf.loc[tt])
    yT = fh_large_gain_TT_T @ y0
    fh_large_gain_Epi[tt] = yT[1]

    y0 = np.array(re_irf.loc[tt])
    yT = re_TT_T @ y0
    re_Epi[tt] = yT[1]

fh_irf['expdp'] = fh_Epi
fh_large_gain_irf['expdp'] = fh_large_gain_Epi
re_irf['expdp'] = re_Epi

#add aggregate tilde variables to fh_irf df
fh_irf['ytilde'] = fh_irf['y']-fh_irf['ybar']
fh_irf['ppitilde'] = fh_irf['ppi']-fh_irf['pibar']
fh_irf['itilde'] = fh_irf['i']-fh_irf['ibar']

fh_large_gain_irf['ytilde'] = fh_large_gain_irf['y']-fh_large_gain_irf['ybar']
fh_large_gain_irf['ppitilde'] = fh_large_gain_irf['ppi']-fh_large_gain_irf['pibar']
fh_large_gain_irf['itilde'] = fh_large_gain_irf['i']-fh_large_gain_irf['ibar']

re_irf['ytilde'] = re_irf['y']-re_irf['ybar']
re_irf['ppitilde'] = re_irf['ppi']-re_irf['pibar']
re_irf['itilde'] = re_irf['i']-re_irf['ibar']

fh_irf['rrate'] = fh_irf['i']-fh_irf['ppi(1)']
fh_large_gain_irf['rrate'] = fh_large_gain_irf['i']-fh_large_gain_irf['ppi(1)']
re_irf['rrate'] = re_irf['i']-re_irf['ppi(1)']


with saved_figure('figures-tables/disinflation_shock.pdf',nrows=3, ncols=2) as (fig,ax):
    fh_irf['y'].plot(ax=ax[0,0],linewidth=3,label='Estimated FH')
    re_irf['y'].plot(ax=ax[0,0],linestyle='dotted',linewidth=3,label='Canonical NK')
    fh_large_gain_irf['y'].plot(ax=ax[0,0],linestyle='dashed',linewidth=3,label='FH with greater updating')
    ax[0,0].set_title(r'$y_t$')
    #ax[0,0].set_ylim(-0.55,0.1)
    #  
    (4*fh_irf['ppi']).plot(ax=ax[0,1],linewidth=3)
    (4*re_irf['ppi']).plot(ax=ax[0,1],linestyle='dotted',linewidth=3)
    (4*fh_large_gain_irf['ppi']).plot(ax=ax[0,1],linestyle='dashed',linewidth=3)
    ax[0,1].set_title(r'$\pi^A_t$')
    ax[0,1].set_ylim(-1.05,0.1)
      
    (4*fh_irf['rrate']).plot(ax=ax[1,0],linewidth=3)
    (4*re_irf['rrate']).plot(ax=ax[1,0],linestyle='dotted',linewidth=3)
    (4*fh_large_gain_irf['rrate']).plot(ax=ax[1,0],linestyle='dashed',linewidth=3)
    ax[1,0].set_title(r'$i^A_t-E_t\pi^A_{t+1}$')
    ax[1,0].set_ylim(-0.05,0.35)
     
    (4*fh_irf['expdp']).plot(ax=ax[1,1],linewidth=3)
    (4*re_irf['expdp']).plot(ax=ax[1,1],linestyle='dotted',linewidth=3)
    (4*fh_large_gain_irf['expdp']).plot(ax=ax[1,1],linestyle='dashed',linewidth=3)
    ax[1,1].set_title(r'$E_t \pi^A_{t+20}$')
    ax[1,1].set_ylim(-1.1,0.1)
     
    fh_irf['ybar'].plot(ax=ax[2,0],linewidth=3)
    (np.nan*re_irf['ybar']).plot(ax=ax[2,0],linestyle='dotted',linewidth=3)
    fh_large_gain_irf['ybar'].plot(ax=ax[2,0],linestyle='dashed',linewidth=3)
    ax[2,0].set_title(r'$\bar{y}_t$')
     
    (4*fh_irf['pibar']).plot(ax=ax[2,1],linewidth=3,label='Estimated FHP')
    (4*np.nan*re_irf['pibar']).plot(ax=ax[2,1],linestyle='dotted',linewidth=3,label='Canonical NK')
    (4*fh_large_gain_irf['pibar']).plot(ax=ax[2,1],linestyle='dashed',linewidth=3,label='FHP with greater updating')
    ax[2,1].set_title(r'$\bar{\pi}^A_t$')
    ax[2,1].set_ylim(-1,0.1)
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.12)
    ax[2,0].legend([r'Estimated FHP-\(\bar\phi\)', 'Canonical NK', r'FHP-\(\bar\phi\) with greater updating'], 
                     ncol=3,frameon=False,loc=(0.15,-0.53))
    #
    [axi.axhline(0,linewidth=0.3,alpha=0.7,color='black') for axi in ax.reshape(-1)]
    [axi.set_xlim(0,19) for axi in ax.reshape(-1)]

    


