from fortress import make_smc, SMCDriver, load_estimates
from dsge.translate import smc, write_prior_file
from dsge.symbols import Parameter, Variable, Equation
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
                 "model", 
                 "smc_file")

    estimation_settings = {"nphi": 500,
                           "nblocks": 3,
                           "npart": 16000,
                           "pe": 1000}



    def __init__(self, name, yaml_file, fortran_directory, fixed_parameters={}, estimation_settings={}, smc_file=None):
        self.name = name
        self.yaml_file = yaml_file
        self.fortran_directory = fortran_directory
        self.fixed_parameters = fixed_parameters
        self.estimation_settings.update(estimation_settings)
        self.smc_file = smc_file 

    def load(self, add_shocks=False, add_hats=False):
        self.model = DSGE.read(self.yaml_file)
        fix_parameters(self.model, **self.fixed_parameters)

        if add_shocks:
            v_epsxi = Variable('v_epsxi')
            v_epsi = Variable('v_epsi')
            v_epsy = Variable('v_epsy')
            self.model['var_ordering'] = self.model['var_ordering'] + [v_epsxi, v_epsi, v_epsy]
            self.model['perturb_eq'] = (self.model['perturb_eq'] + 
                                        [Equation(v_epsxi, self.model.shocks[0]),
                                         Equation(v_epsi, self.model.shocks[1]),
                                         Equation(v_epsy, self.model.shocks[2])])

        if add_hats:
            v_yhat = Variable('yhat')
            v_pihat = Variable('pihat')
            self.model['var_ordering'] = self.model['var_ordering'] + [v_yhat, v_pihat]
            self.model['perturb_eq'] = (self.model['perturb_eq'] + 
                                           [Equation(v_yhat, self.model.variables[0] - self.model.variables[3]),
                                            Equation(v_pihat, self.model.variables[1] - self.model.variables[4])])


    def parameters(self):
        return [str(para) for para in self.model.parameters]

    def linear_model(self):
        return self.model.compile_model()

   

    def create_fortran_model(self):
        if self.smc_file is None:                                 
            smc_file = smc(self.model)
        else:
            smc_file = self.smc_file 

        model_linear = self.model.compile_model()                 
        other_files = {'data.txt': model_linear.yy,          
                       'prior.txt': 'prior.txt'}             
        make_smc(smc_file, other_files=other_files,          
                 output_directory=self.fortran_directory)                      
        write_prior_file(model_linear.prior, self.fortran_directory)           

    def estimate(self, **kwargs):
        smc = SMCDriver('./' + self.fortran_directory + '/smc')
        smc.run(**kwargs)

    def load_estimates(self, **kwargs):
        return load_estimates(self.fortran_directory + '/output-*.json',
                              paranames=self.parameters(),
                              **kwargs)


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
    fortran_directory="fortran/finite_horizon_phibar",
    fixed_parameters={
        "gammatilde": "gamma",
        "alpha": 0.75,
    },
)

finite_horizon_gamma = ModelAttributes(
    name=r"$FH-\tilde\gamma$",
    yaml_file="models/finite_horizon.yaml",
    fortran_directory="fortran/finite_horizon_gamma",
    fixed_parameters={
        "phipiLR": "phipi",
        "phiyLR": "phiy",
        "alpha": 0.75,
    },
)

trends = ModelAttributes(
    name="Stat. Trends",
    yaml_file="models/finite_horizon_trend.yaml",
    fortran_directory="fortran/statistical_trends",
    fixed_parameters={
        "alpha": 0.75,
    },
)


angeletos_lian = ModelAttributes(
    name="Angeletos-Lian",
    yaml_file='models/finite_horizon_angeletos_lian.yaml',
    fortran_directory='fortran/angeletos_lian',
    fixed_parameters={
        "alpha":0.75,
        "phipiLR":1.5, 
        "phiyLR":0.25
    },
)
    
habits = ModelAttributes(
    name="Hybrid NK",
    yaml_file='models/finite_horizon_habits_lam.yaml',
    fortran_directory='fortran/habits',
    fixed_parameters={
        "alpha":0.75,
        "lampi":0.75
    },
)


habits_lampi = ModelAttributes(
    name=r"Hybrid NK-\(\lambda_\pi\)",
    yaml_file='models/finite_horizon_habits_lam.yaml',
    fortran_directory='fortran/habits_lampi',
    fixed_parameters={
        "alpha":0.75,
    },
)


single_agent_template = open('single_agent_template.f90').read()

single_agent_models = [
    ModelAttributes(
        name=r"$FH-\bar\phi$ Rep. Agent ($k=%d)" % k,
        yaml_file="models/finite_horizon.yaml",
        fortran_directory="fortran/finite_horizon_phibar_k%d" % k,
        fixed_parameters={
            "gammatilde": "gamma",
            "alpha": 0.75,
        },
        smc_file=single_agent_template.format(k=k)
    )
    for k in range(5)]

