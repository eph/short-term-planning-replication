from models import (
    canonical_NK,
    finite_horizon,
    finite_horizon_gamma,
    finite_horizon_phibar,
    trends,
)


for model in [
    canonical_NK,
    finite_horizon,
    finite_horizon_gamma,
    finite_horizon_phibar,
]:
    model.load()
    model.create_fortran_model()
