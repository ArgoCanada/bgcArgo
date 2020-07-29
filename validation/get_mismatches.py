#!/usr/bin/python

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from bgcArgo import sprof

# summary comparison between bgcArgo and SAGE/DOXY audit
fn = Path('../data/doxy_audit_vs_bgcArgo_py_comparison_20200725.csv')
df = pd.read_csv(fn)
df['diffGAIN'] = np.abs(df.pyGAIN - df.sageGAIN)

audit_file = Path('../data/DOXY_audit_070720.TXT')
xf = pd.read_csv(audit_file, sep='\t', header=25)

nan = df[df.diffGAIN.isnull()]
big = df[df.diffGAIN >= 0.2]

# by dac
sys.stdout.write('%nan (N)\t%big (N)\t%audit (N)\t dac\n')
for dac in xf.DAC.unique():
    sub_nan = nan[nan.DAC == dac]
    sub_big = big[big.DAC == dac]
    sub_audit = xf[xf.DAC == dac]
    sys.stdout.write('{:.2f} ({:d})\t{:.2f} ({:d})\t{:.2f} ({:d})\t{}\n'.format(100*sub_nan.shape[0]/nan.shape[0], sub_nan.shape[0], 100*sub_big.shape[0]/big.shape[0], sub_big.shape[0], 100*sub_audit.shape[0]/xf.shape[0], sub_audit.shape[0], dac))

# looks like disproportionate amount of coriolis are nan or big - look into it
# sub = df[np.logical_or(df.diffGAIN.isnull(), df.diffGAIN >= 0.2)]
# sub = df[df.pyGAIN.isnull()]
sub = df[df.diffGAIN >= 1]
sub = sub[sub.DAC == 'coriolis']

sprof.set_dirs(argo_path='/Users/gordonc/Documents/data/Argo', woa_path='/Users/gordonc/Documents/data/WOA18')
for wmo in sub.WMO.unique():
    dac = sub.DAC.iloc[0]
    syn = sprof(wmo)
    syn.clean()
    wf = sub[sub.WMO == wmo]
    ff = syn.to_dataframe()
    ff = ff[ff.CYCLE.isin(wf.CYCLE)]

    if not ff.DOXY_ADJUSTED.isnull().all():
        print('{} {:d}: There are some adjusted oxygen values'.format(dac, wmo))
    else:
        print('{} {:d}: No adjusted oxygen levels'.format(dac, wmo))