from models import (
    canonical_NK,
    trends,
    finite_horizon,
    finite_horizon_gamma,
    finite_horizon_phibar,
    angeletos_lian,
    habits,
    habits_lampi,
    single_agent_models
)


for model in [
    canonical_NK,
    trends,
    finite_horizon,
    finite_horizon_gamma,
    finite_horizon_phibar,
    angeletos_lian,
    habits,
    habits_lampi,
]:
   model.load()
   model.create_fortran_model()


# now the single agent models
for model in single_agent_models:
    model.load()
    model.create_fortran_model()
