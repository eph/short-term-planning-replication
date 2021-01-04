from fortress import make_smc, SMCDriver
from dsge.translate import smc, write_prior_file
from dsge.symbols import Parameter
from dsge.DSGE import DSGE

def fix_parameters(model, **kwargs):
    """Takes an estimated parameter from a DSGEModel
    and converts it to a calibrated one."""
    for para, value in kwargs.items():
        para = Parameter(para)
        model['par_ordering'].remove(para)
        model['other_para'].append(para)
        model['para_func'][str(para)] = value
    return model


class ModelAttributes(object):

    __slots__ = ("name",
                 "yaml_file",
                 "fortran_directory",
                 "fixed_parameters",
                 "model")

    def __init__(self, name, yaml_file, fortran_directory, fixed_parameters={}):
        self.name = name
        self.yaml_file = yaml_file
        self.fortran_directory = fortran_directory
        self.fixed_parameters = fixed_parameters

    def load(self):
        self.model = DSGE.read(self.yaml_file)
        fix_parameters(self.model, **self.fixed_parameters)

    def linear_model(self):
        return self.model.compile_model()

    def create_fortran_model(self, smc_file=None):
        if smc_file is None:                                 
            smc_file = smc(self.model)                            
        model_linear = self.model.compile_model()                 
        other_files = {'data.txt': model_linear.yy,          
                       'prior.txt': 'prior.txt'}             
        make_smc(smc_file, other_files=other_files,          
                 output_directory=self.fortran_directory)                      
        write_prior_file(model_linear.prior, self.fortran_directory)           

    def estimate(self, **kwargs):
        smc = SMCDriver('./' + self.fortran_directory + '/smc')
        smc.run(**kwargs)


canonical_NK = ModelAttributes(
    name="Canonical NK",
    yaml_file="models/finite_horizon.yaml",
    fortran_directory="fortran/canonical_NK",
    fixed_parameters={
        "rho": 1,
        "gamma": 0.1,
        "gammatilde": 0.1,
        "phipiLR": "phipi",
        "phiyLR": "phiy",
        "alpha": 0.75,
    },
)


finite_horizon = ModelAttributes(
    name="FH",
    yaml_file="models/finite_horizon.yaml",
    fortran_directory="fortran/finite_horizon",
    fixed_parameters={
        "gammatilde": "gamma",
        "phipiLR": "phipi",
        "phiyLR": "phiy",
        "alpha": 0.75,
    },
)


finite_horizon = ModelAttributes(
    name="FH",
    yaml_file="models/finite_horizon.yaml",
    fortran_directory="fortran/finite_horizon",
    fixed_parameters={
        "gammatilde": "gamma",
        "phipiLR": "phipi",
        "phiyLR": "phiy",
        "alpha": 0.75,
    },
)

finite_horizon_phibar = ModelAttributes(
    name=r"$FH-\bar\phi$",
    yaml_file="models/finite_horizon.yaml",
    fortran_directory="fortran/finite_horizon",
    fixed_parameters={
        "gammatilde": "gamma",
        "alpha": 0.75,
    },
)

finite_horizon_gamma = ModelAttributes(
    name=r"$FH-\tilde\gamma$",
    yaml_file="models/finite_horizon.yaml",
    fortran_directory="fortran/finite_horizon",
    fixed_parameters={
        "phipiLR": "phipi",
        "phiyLR": "phiy",
        "alpha": 0.75,
    },
)


trends = ModelAttributes(
    name="Stat. Trends",
    yaml_file="finite_horizon_trend.yaml",
    fortran_directory="fortran/statistical_trends",
    fixed_parameters={
        "rho": 1.0,
        "gamma": 0.5,
        "gammatilde": "gamma",
        "phipiLR": 1.5,
        "phiyLR": 0.25,
        "alpha": 0.75,
    },
)
