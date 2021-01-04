from models import finite_horizon_phibar
from figures import saved_figure

finite_horizon_phibar.load()
linear_model = finite_horizon_phibar.linear_model()

# Calibration -- see Table 1
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

T = 20                          # horizon of IRF
fh_irf = linear_model.impulse_response(p0, T)['epsi']
fh_TT, fh_RR, fh_unique = linear_model.solve_LRE(p0)

p0[14] = 0.5
fh_large_gain_irf = linear_model.impulse_response(p0, T)['epsi']
fh_large_gain_TT, fh_large_gain_RR, fh_large_gain_unique = linear_model.solve_LRE(p0)

p0[3] = 1.0
re_irf = linear_model.impulse_response(p0, T)['epsi']
re_TT, re_RR, re_unique = linear_model.solve_LRE(p0) 

re_TT_T = matrix_power(AA,H)
AA1_H = matrix_power(AA1,H)
AA2_H = matrix_power(AA2,H)

expdp = np.zeros(TT)
expdp1 = np.zeros(TT)
expdp2 = np.zeros(TT)
for tt in np.arange(TT):
    y0 = np.array(xirf1.loc[tt])
    yh = AA1_H @ y0
    expdp1[tt] = yh[1] 
    y0 = np.array(xirf.loc[tt])
    yh = AA_H @ y0
    expdp[tt] = yh[1]
    y0 = np.array(xirf2.loc[tt])
    yh = AA2_H @ y0
    expdp2[tt] = yh[1]

xirf['expdp'] = expdp
xirf1['expdp'] = expdp1
xirf2['expdp'] = expdp2

#add aggregate tilde variables to xirf df
xirf['ytilde'] = xirf['y']-xirf['ybar']
xirf['ppitilde'] = xirf['ppi']-xirf['pibar']
xirf['itilde'] = xirf['i']-xirf['ibar']

xirf1['ytilde'] = xirf1['y']-xirf1['ybar']
xirf1['ppitilde'] = xirf1['ppi']-xirf1['pibar']
xirf1['itilde'] = xirf1['i']-xirf1['ibar']

xirf2['ytilde'] = xirf2['y']-xirf2['ybar']
xirf2['ppitilde'] = xirf2['ppi']-xirf2['pibar']
xirf2['itilde'] = xirf2['i']-xirf2['ibar']

xirf['rrate'] = xirf['i']-xirf['ppi(1)']
xirf1['rrate'] = xirf1['i']-xirf1['ppi(1)']
xirf2['rrate'] = xirf2['i']-xirf2['ppi(1)']



with saved_figure('figures-tables/disinflation_shock.pdf',nrows=2,ncols=2) as (fig,ax):
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
    ax[0,1].set_ylim(-1.0,0.1)
      
    # (4*fh_irf['rrate']).plot(ax=ax[1,0],linewidth=3)
    # (4*fh_irf1['rrate']).plot(ax=ax[1,0],linestyle='dotted',linewidth=3)
    # (4*fh_irf2['rrate']).plot(ax=ax[1,0],linestyle='dashed',linewidth=3)
    # ax[1,0].set_title(r'$i^A_t-E_t\pi^A_{t+1}$')
    # ax[1,0].set_ylim(-0.05,0.35)
    #  
    # (4*fh_irf['expdp']).plot(ax=ax[1,1],linewidth=3)
    # (4*fh_irf1['expdp']).plot(ax=ax[1,1],linestyle='dotted',linewidth=3)
    # (4*fh_irf2['expdp']).plot(ax=ax[1,1],linestyle='dashed',linewidth=3)
    # ax[1,1].set_title(r'$E_t \pi^A_{t+20}$')
    # ax[1,1].set_ylim(-1.1,0.1)
    #  
    # fh_irf['ybar'].plot(ax=ax[2,0],linewidth=3)
    # (np.nan*fh_irf1['ybar']).plot(ax=ax[2,0],linestyle='dotted',linewidth=3)
    # fh_irf2['ybar'].plot(ax=ax[2,0],linestyle='dashed',linewidth=3)
    # ax[2,0].set_title(r'$\bar{y}_t$')
    #  
    # (4*fh_irf['pibar']).plot(ax=ax[2,1],linewidth=3,label='Estimated FH')
    # (4*np.nan*fh_irf1['pibar']).plot(ax=ax[2,1],linestyle='dotted',linewidth=3,label='Canonical NK')
    # (4*fh_irf2['pibar']).plot(ax=ax[2,1],linestyle='dashed',linewidth=3,label='FH with greater updating')
    # ax[2,1].set_title(r'$\bar{\pi}^A_t$')
    # ax[2,1].set_ylim(-1,0.1)
    # fig2.tight_layout()
    # fig2.subplots_adjust(bottom=0.12)
    # ax[2,0].legend([r'Estimated FH-\(\bar\phi\)', 'Canonical NK', r'FH-\(\bar\phi\) with greater updating'], 
    #                  ncol=3,frameon=False,loc=(0.15,-0.53))
    # #
    # [axi.axhline(0,linewidth=0.3,alpha=0.7,color='black') for axi in ax.reshape(-1)]
    # [axi.set_xlim(0,19) for axi in ax.reshape(-1)]

    


