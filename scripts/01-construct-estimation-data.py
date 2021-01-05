import numpy as np
from pandas_datareader import get_data_fred


fred = ["GDPC1", "GDPDEF", "CNP16OV",
        "FEDFUNDS", 'GDPPOT', 'USRECQ']

data = (get_data_fred(fred, '1965', '2007Q4')
        .resample('Q')
        .mean()
        .to_period())

data['LNSindex'] = data['CNP16OV'] / data['CNP16OV']['1992Q3']
data['output'] = np.log(data['GDPC1'] / data['LNSindex']) * 100
data['inflation'] = np.log(data['GDPDEF'] / data['GDPDEF'].shift(1)) * 400
data['interest rate'] = data['FEDFUNDS']


data['ygr'] = data['output'].diff()
data['xgap'] = np.log(data.GDPC1/data.GDPPOT)
data['USRECQ'][data.USRECQ == 0] = np.nan

obs = ['ygr', 'inflation', 'interest rate']
np.savetxt('data/longsample.txt', data[obs]['1966':'2007'])
np.savetxt('data/post83sample.txt', data[obs]['1984':'2007'])
np.savetxt('data/post91sample.txt', data[obs]['1992':'2007'])
np.savetxt('data/xgap.txt', data['xgap']['1966':'2007'])
np.savetxt('data/usrec.txt', data['USRECQ']['1966':'2007'])
