# Argo Canada BGC Quality Control

[![Anaconda-Server Badge](https://anaconda.org/conda-forge/bgcargo/badges/installer/conda.svg)](https://anaconda.org/conda-forge/bgcargo) 
[![Build Status](https://travis-ci.com/ArgoCanada/bgcArgo.svg?branch=master)](https://travis-ci.com/ArgoCanada/bgcArgo) 
[![Documentation Status](https://readthedocs.org/projects/bgcargo/badge/?version=latest)](https://bgcargo.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/ArgoCanada/bgcArgo/branch/master/graph/badge.svg)](https://codecov.io/gh/ArgoCanada/bgcArgo)

## disclaimer

This code is in _very_ active development. Use of this code is available (encouraged even), but will likely throw errors, behave in undesired ways, etc. Submission of issues is also encouraged to help in development!

## installation

The recommended install is through the conda-forge channel, via the command:

```bash
conda install -c conda-forge bgcargo
```

The package is also available through the python package index <https://pypi.org/project/bgcArgo/>, install with:

```bash
pip install bgcArgo
```

## general description

A `python` library of functions for quality controlling dissolved oxygen data.
Heavily based on the [SOCCOM BGC Argo QC methods](https://github.com/SOCCOM-BGCArgo/ARGO_PROCESSING)
program in `matlab`, uses either
[NCEP](https://psl.noaa.gov/data/gridded/data.ncep.reanalysis.html)
or [World Ocean Atlas](https://www.nodc.noaa.gov/OC5/woa18/) data to
calculate oxygen gains
([*Johnson et al. 2015*](https://doi.org/10.1175/JTECH-D-15-0101.1)).

## bgcArgo dependencies

- Must run on `python3.4` or higher, not supported on `python2.x` (uses [pathlib](https://docs.python.org/3/library/pathlib.html), introduced in python version 3.4)
- TEOS-10 package [gsw](https://teos-10.github.io/GSW-Python/), but will also work with the [seawater](https://pypi.org/project/seawater/) package, though it is deprecated in favor of gsw
- [netCDF4](https://pypi.org/project/netCDF4/) module for `.nc` files
- [pandas](https://pandas.pydata.org/) is required (and highly recommended for all your data science needs!)
- [seaborn](https://seaborn.pydata.org/) is recommended but not required, through there will be some reduced (non-essential) functionality
- [cmocean](https://matplotlib.org/cmocean/) is also recommended for nicer plots, but not required

## basic functionality

Although functions in the `bgcArgo` module may be of use in other situations, the majority of the functionality is lies within two classes, `profiles` for typical profile files and `sprof` for synthetic profiles.

```python
import bgcArgo as bgc

# setup for your system - these directories need to already exist!
argo_path = 'your/argo/data/path' # where to save Argo data
ncep_path = 'your/ncep/data/path' # where to save NCEP reanalysis data
woa_path  = 'your/woa18/data/path' # where to save WOA data

# download the data - this can take some time depending on connection
# Argo
wmos = [4902481, 6902905]
for w in wmos:
  bgc.io.get_argo(w, local_path=argo_path)
# NCEP
bgc.io.get_ncep('pres', local_path=ncep_path)
bgc.io.get_ncep('land', local_path=ncep_path)
# WOA
bgc.io.get_woa18('O2sat', local_path=woa_path)

# tell the package where to look for data
bgc.set_dirs(argo_path=argo_path, ncep_path=ncep_path, woa_path=woa_path)
# load data  for the first 10 profiles for two floats
flts = bgc.profiles(wmos, cycles=list(range(1,11)))
df = flts.to_dataframe()
>>> print(df)

# load a synthetic profile
syn = bgc.sprof(4902481)
# plot a time vs. depth section for the top 500m
g1 = syn.plot('cscatter', varname='DOXY', ylim=(0,500))
# plot the first 10 profiles for temperature, practical salinity, oxygen
g2 = syn.plot('profiles', varlist=['TEMP','PSAL', 'DOXY'], Ncycle=1, Nprof=10, ylim=(0,500))

# calculate gains in-air and using saturation data
inair_g = syn.calc_gains()
surf_g  = syn.calc_gains(ref='WOA')

>>> print(f'Mean in-air gain: {np.nanmean(inair_g):.2f}')
>>> print(f'Mean in-water gain: {np.nanmean(surf_g):.2f}')
```

The above code would produce the following output and plots:

```text
       CYCLE           SDN      WMO   LATITUDE  ...  DOXY_ADJUSTED  DOXY_ADJUSTED_QC      O2Sat  O2Sat_QC
0        1.0  17921.627083  6902905 -52.503939  ...            NaN               4.0        NaN       4.0
1        1.0  17921.627083  6902905 -52.503939  ...            NaN               4.0        NaN       4.0
2        1.0  17921.627083  6902905 -52.503939  ...            NaN               4.0        NaN       4.0
3        1.0  17921.627083  6902905 -52.503939  ...            NaN               4.0        NaN       4.0
4        1.0  17921.627083  6902905 -52.503939  ...            NaN               4.0        NaN       4.0
...      ...           ...      ...        ...  ...            ...               ...        ...       ...
30545   10.0  18151.225694  4902481  55.530190  ...            NaN               4.0  82.866123       3.0
30546   10.0  18151.225694  4902481  55.530190  ...            NaN               4.0  82.660113       3.0
30547   10.0  18151.225694  4902481  55.530190  ...            NaN               4.0  82.495289       3.0
30548   10.0  18151.225694  4902481  55.530190  ...            NaN               4.0  82.368619       3.0
30549   10.0  18151.225694  4902481  55.530190  ...            NaN               4.0  82.078116       3.0

Mean in-air gain: 1.31
Mean in-water gain: 1.04
```

<img src="https://raw.githubusercontent.com/ArgoCanada/bgcArgo/master/figures/example_p1.png" width="800">
<img src="https://raw.githubusercontent.com/ArgoCanada/bgcArgo/master/figures/example_p2.png" width="600">

## version history

0.1: April 20, 2020 - Initial creation

0.2: May 13, 2020 - Major change to how end user would use module, change to more object-oriented, create argo class

0.2.1: June 23, 2020 - pandas is now required, makes reading of global index significantly easier and more efficient

0.2.2: August 28, 2020 - remove pylab dependency (is part of matplotlib), built and uploaded to PyPI, build conda-forge recipe

0.2.3 - 0.2.6: September 3, 2020 - updates to pass all checks on conda-forge pull request, updated on PyPI as well

0.2.7 - 0.2.8: September 29, 2020 - re-spun for PyPI and PR to conda-feedstock
