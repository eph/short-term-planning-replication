from models import canonical_NK
from figures import saved_figure

import pandas as p 

import json

import numpy as np

canonical_NK.load()
index = canonical_NK.linear_model().yy.index

H = 168
def load_Z_estimates(path):
    results = []
    for i in range(1, H+1):
        json_file = json.loads(open(path.format(i)).read())
        results.append({'T': i, 
                        'Z': np.array(json_file['Z_estimates']).sum()})
    return p.DataFrame(results)


mdd_baseline = load_Z_estimates('fortran/finite_horizon_phibar/time-posteriors/output-{:}.json')
mdd_forward = load_Z_estimates('fortran/canonical_NK/time-posteriors/output-{:}.json')

diff = mdd_baseline.Z-mdd_forward.Z
diff.index = index

with saved_figure('figures-tables/cumulative_logmdd_difference.pdf') as (fig, ax):
    diff.plot(ax=ax)
    ax.axhline(0, color='black', alpha=0.3)
    ax.set_xlim(diff.index.to_timestamp()[0], diff.index.to_timestamp()[-1])



