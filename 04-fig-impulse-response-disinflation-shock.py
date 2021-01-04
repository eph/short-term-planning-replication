from models import finite_horizon
from figures import saved_figure

finite_horizon.load()
linear_model = finite_horizon.linear_model()

# Calibration -- see Table 1
p0 = [2.39, #rA
      3.80, # dpbar
      0.45, # gamma
      0.46, # rho
      
      ]


with (fig, ax) as saved_figure('figures/disinflation_shock.pdf'):
    pass
