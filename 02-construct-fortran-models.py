from fortress import make_smc
from dsge.translate import smc, write_prior_file
from dsge.symbols import Parameter


def fix_parameters(model, **kwargs):
    """Takes an estimated parameter from a DSGEModel
    and converts it to a calibrated one."""
    for para, value in kwargs.items():
        para = Parameter(para)
        model['par_ordering'].remove(para)
        model['other_para'].append(para)
        model['para_func'][str(para)] = value
    return model


def create_fortran_model(model, name, smc_file=None):
    """Creates a fortran model from a DSGE model"""
    if smc_file is None:
        smc_file = smc(model)
    model_linear = model.compile_model()
    other_files = {'data.txt': model_linear.yy,
                   'prior.txt': 'prior.txt'}
    make_smc(smc_file, other_files=other_files,
             f90='/msu/home/m1eph00/miniconda2/envs/proxy-svar/bin/mpif90',
             lib_path='/msu/home/m1eph00/miniconda2/envs/proxy-svar/lib/',
             inc_path='/msu/home/m1eph00/miniconda2/envs/proxy-svar/include/',
             output_directory=name)
    write_prior_file(model_linear.prior, name)
    return model_linear
