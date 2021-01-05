export OPENBLAS_NUM_THREADS=1
export NPROCS=4
cd fortran/finite_horizon_phibar
mkdir -p time-posteriors
for t in {1..168}                                                                                                 
do                                                                                                                
   sed -i "s/T = [0-9]\\+/T = $t/g" model_t.f90                                                                
   make smc_driver                                                                                                
   mpirun -n $NPROCS ./smc --npart 8000 --nblocks 3 --output-file time-posteriors/output-$t.json --seed $t 
done                                                                                                              
cd ../canonical_NK
mkdir -p time-posteriors
for t in {1..168}                                                                                                 
do                                                                                                                
    sed -i "s/T = [0-9]\\+/T = $t/g" model_t.f90                                                                
    make smc_driver                                                                                                
    mpirun -n $NPROCS ./smc --npart 8000 --nblocks 3 --output-file time-posteriors/output-$t.json --seed $t 
done                                                                                                              
cd ../..
