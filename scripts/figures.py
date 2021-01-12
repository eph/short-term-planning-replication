from contextlib import contextmanager

import numpy as np
import pandas as p

import matplotlib.pyplot as plt

plt.style.use("seaborn-white")
plt.matplotlib.rcParams["xtick.top"] = False
plt.matplotlib.rcParams["ytick.right"] = False
plt.matplotlib.rcParams["axes.spines.right"] = False
plt.matplotlib.rcParams["axes.spines.top"] = False
plt.matplotlib.rcParams["font.sans-serif"] = "Fira Code"
plt.matplotlib.rcParams["text.usetex"] = True


data = {"xgap": np.loadtxt("data/xgap.txt"),
        "USRECQ": np.loadtxt("data/usrec.txt")}

data = p.DataFrame(data,
                   index=p.period_range("1966", "2007Q4", freq="Q"))

latex = {
    "rA": r"$r^A$",
    "sigma": r"$\sigma$",
    "rho": r"$\rho$",
    "kappa": r"$\kappa$",
    "alpha": r"$\alpha$",
    "phipi": r"$\phi_\pi$",
    "phiy": r"$\phi_y$",
    "phipiLR": r"$\bar\phi_\pi$",
    "phiyLR": r"$\bar\phi_y$",
    "gamma": r"$\gamma$",
    "gammatilde": r"$\tilde\gamma$",
    "epsxi": r"$\xi_t$",
    "epsi": r"$r^*_t$",
    "epsy": r"$y^*_t$",
    "piA": r"$\pi^A$",
    "yQ": r"$\mu^Q$",
    "rhoxi": r"$\rho_\xi$",
    "rhoy": r"$\rho_{y^*}$",
    "rhoi": r"$\rho_{i^*}$",
    "sigxi": r"$\sigma_\xi$",
    "sigy": r"$\sigma_{y^*}$",
    "sigi": r"$\sigma_{i^*}$",
    "rhoibar": r"$\rho_{\bar i}$",
    "rhoybar": r"$\rho_{\bar y}$",
    "rhopibar": r"$\rho_{\bar \pi}$",
    "sigibar": r"$\sigma_{\bar i}$",
    "sigybar": r"$\sigma_{\bar y}$",
    "sigpibar": r"$\sigma_{\bar \pi}$",
    "nu": r"$\nu$",
    "lam": r"$\lambda$",
    "rhof": r"$\rho_f$",
    "a": r"$a$",
    "lambda_y": r"$\lambda_y$",
    "lambda_pi": r"$\lambda_\pi$",
    "lampi": r"$\lambda_\pi$",
    "logmdd": r"Log MDD",
}


def add_rec_bars(ax):
    ylims = ax.get_ylim()
    ax.fill_between(
        data.index.to_timestamp(),
        data.USRECQ * ylims[0],
        data.USRECQ * ylims[1],
        alpha=0.1,
        color="black",
    )
    ax.set_ylim(ylims)
    return ax


@contextmanager
def saved_figure(fname, **kwds):
    """
    Saves a figure in `fname`.
    """
    fig, ax = plt.subplots(**kwds)
    try:
        yield (fig, ax)
    finally:
        fig.savefig(fname, bbox_inches='tight')
        plt.close(fig)
