from models import finite_horizon as model

NPROCS = 10
es = model.estimation_settings
shell_script=f"""#!/bin/bash
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
#with os.fdopen(os.open('estimation.sh', os.O_WRONLY | os.O_CREAT, 0o777), 'w') as f:
#    f.write(shell_script)

import subprocess 
output = subprocess.call("./estimation.sh")

