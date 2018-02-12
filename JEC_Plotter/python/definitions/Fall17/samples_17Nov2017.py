import numpy as np

from copy import deepcopy

from Excalibur.JEC_Plotter.core import Sample
from _common import *

# -- Samples: each sample is a ROOT file containing Excalibur output

_SAMPLE_DIR_V3 = "/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V3_2018-01-31"
_SAMPLE_DIR_V4 = "/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V4_2018-02-08"

SAMPLES = {
    'MC_Zmm_DYNJ_Fall17_V3': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR_V3,
        sample_file='mc17_mm_DYNJ_Madgraph.root'
    ),
    'MC_Zee_DYNJ_Fall17_V3': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR_V3,
        sample_file='mc17_ee_DYNJ_Madgraph.root'
    ),
    'MC_Zmm_DYNJ_Fall17_V4': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR_V4,
        sample_file='mc17_mm_DYNJ_Madgraph.root'
    ),
    'MC_Zee_DYNJ_Fall17_V4': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR_V4,
        sample_file='mc17_ee_DYNJ_Madgraph.root'
    ),
}

for _run_period in ('B', 'C', 'D', 'E', 'F', 'BCDEF'):
    SAMPLES.update({
        'Data_Zmm_{}_Fall17_V3'.format(_run_period): Sample.load_using_convention(
            sample_dir=_SAMPLE_DIR_V3,
            sample_file='data17_mm_{}_17Nov2017.root'.format(_run_period)
        ),
        'Data_Zee_{}_Fall17_V3'.format(_run_period): Sample.load_using_convention(
            sample_dir=_SAMPLE_DIR_V3,
            sample_file='data17_ee_{}_17Nov2017.root'.format(_run_period)
        ),
        'Data_Zmm_{}_Fall17_V4'.format(_run_period): Sample.load_using_convention(
            sample_dir=_SAMPLE_DIR_V4,
            sample_file='data17_mm_{}_17Nov2017.root'.format(_run_period)
        ),
        'Data_Zee_{}_Fall17_V4'.format(_run_period): Sample.load_using_convention(
            sample_dir=_SAMPLE_DIR_V4,
            sample_file='data17_ee_{}_17Nov2017.root'.format(_run_period)
        ),
    })

# -- Additional Cuts

if __name__ == "__main__":
    for _sn, _s in SAMPLES.iteritems():
        print "Sample '{}':".format(_sn)
        for k, v in _s._dict.iteritems():
            print "\t{}: {}".format(k, v)
