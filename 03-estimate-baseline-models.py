import argparse
from models import (
    canonical_NK,
    trends,
    finite_horizon,
    finite_horizon_gamma,
    finite_horizon_phibar,
    angeletos_lian,
    habits,
    habits_lampi,
    single_agent_models,
)

model_dict = {
    "canonical_NK": canonical_NK,
    "trends": trends,
    "finite_horizon": finite_horizon,
    "finite_horizon_gamma": finite_horizon_gamma,
    "finite_horizon_phibar": finite_horizon_phibar,
    "angeletos_lian": angeletos_lian,
    "habits": habits,
    "habits_lampi": habits_lampi,
    "finite_horizon_phibar_k0": single_agent_models[0],
    "finite_horizon_phibar_k1": single_agent_models[1],
    "finite_horizon_phibar_k2": single_agent_models[2],
    "finite_horizon_phibar_k3": single_agent_models[3],
    "finite_horizon_phibar_k4": single_agent_models[4],
}




parser = argparse.ArgumentParser(
    description="Estimate a Bayesian DSGE model 10 times via SMC"
)
parser.add_argument(
    "--model",
    choices=[
        "canonical_NK",
        "trends",
        "finite_horizon",
        "finite_horizon_gamma",
        "finite_horizon_phibar",
        "angeetos_lian",
        "habits",
        "habits_lampi" "finite_horizon_phibar_k0",
        "finite_horizon_phibar_k1",
        "finite_horizon_phibar_k2",
        "finite_horizon_phibar_k3",
        "finite_horizon_phibar_k4",
    ],
    default='canonical_NK'
)
parser.add_argument("--nprocs", default=4)
args = parser.parse_args()

model = model_dict[args.model]
NPROCS = args.nprocs
es = model.estimation_settings
shell_script = f"""#!/bin/bash
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
mpirun -n {NPROCS} ./{model.fortran_directory}/smc --nphi {es['nphi']} --nblocks {es['nblocks']} -pe {es['pe']} --output-file {model.fortran_directory}/output-01.json --seed 1
mpirun -n {NPROCS} ./{model.fortran_directory}/smc --nphi {es['nphi']} --nblocks {es['nblocks']} -pe {es['pe']} --output-file {model.fortran_directory}/output-02.json --seed 2
mpirun -n {NPROCS} ./{model.fortran_directory}/smc --nphi {es['nphi']} --nblocks {es['nblocks']} -pe {es['pe']} --output-file {model.fortran_directory}/output-03.json --seed 3
mpirun -n {NPROCS} ./{model.fortran_directory}/smc --nphi {es['nphi']} --nblocks {es['nblocks']} -pe {es['pe']} --output-file {model.fortran_directory}/output-04.json --seed 4
mpirun -n {NPROCS} ./{model.fortran_directory}/smc --nphi {es['nphi']} --nblocks {es['nblocks']} -pe {es['pe']} --output-file {model.fortran_directory}/output-05.json --seed 5
mpirun -n {NPROCS} ./{model.fortran_directory}/smc --nphi {es['nphi']} --nblocks {es['nblocks']} -pe {es['pe']} --output-file {model.fortran_directory}/output-06.json --seed 6
mpirun -n {NPROCS} ./{model.fortran_directory}/smc --nphi {es['nphi']} --nblocks {es['nblocks']} -pe {es['pe']} --output-file {model.fortran_directory}/output-07.json --seed 7
mpirun -n {NPROCS} ./{model.fortran_directory}/smc --nphi {es['nphi']} --nblocks {es['nblocks']} -pe {es['pe']} --output-file {model.fortran_directory}/output-08.json --seed 8
mpirun -n {NPROCS} ./{model.fortran_directory}/smc --nphi {es['nphi']} --nblocks {es['nblocks']} -pe {es['pe']} --output-file {model.fortran_directory}/output-09.json --seed 9
mpirun -n {NPROCS} ./{model.fortran_directory}/smc --nphi {es['nphi']} --nblocks {es['nblocks']} -pe {es['pe']} --output-file {model.fortran_directory}/output-10.json --seed 10
"""
import os

path = "estimation.sh"
with open(path, "w") as f:
    f.write(shell_script)

mode = os.stat(path).st_mode
mode |= (mode & 0o444) >> 2  # copy R bits to X
os.chmod(path, mode)

import subprocess

output = subprocess.call("./estimation.sh")
