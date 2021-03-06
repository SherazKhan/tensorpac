"""
==============================
Basic phase amplitude coupling
==============================

For the visualization, we used a comodulogram.
"""
import matplotlib.pyplot as plt
from tensorpac.utils import pac_signals_tort
from tensorpac import Pac
plt.style.use('seaborn-poster')

# First, we generate a dataset of signals artificially coupled between 10hz
# and 100hz. By default, this dataset is organized as (ntrials, npts) where
# npts is the number of time points.
n = 10  # number of datasets
npts = 4000  # number of time points
data, time = pac_signals_tort(fpha=10, famp=100, noise=3., ntrials=n,
                              npts=npts, dpha=10, damp=5, chi=.8)

# First, let's use the MVL, without any further correction by surrogates :
p = Pac(idpac=(1, 0, 0), fpha=(2, 30, 1, .5), famp=(60, 150, 10, 1))
xpac = p.filterfit(1024, data, axis=1)
t1 = p.method + '\n' + p.surro + '\n' + p.norm

# Now, we still use the MVL method, but in addition we shuffle amplitude time
# series and then, subtract then divide by the mean of surrogates :
p.idpac = (1, 1, 1)
xpac_corr = p.filterfit(1024, data, data, axis=1, nperm=10)
t2 = p.method + '\n' + p.surro + '\n' + p.norm
# Now, we plot the result by taking the mean across the dataset dimension.
plt.figure(figsize=(20, 7))
plt.subplot(1, 2, 1)
p.comodulogram(xpac.mean(-1), title=t1)

plt.subplot(1, 2, 2)
p.comodulogram(xpac_corr.mean(-1), title=t2)
plt.show()
