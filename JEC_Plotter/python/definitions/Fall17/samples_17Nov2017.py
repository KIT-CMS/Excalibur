import numpy as np

from copy import deepcopy

from Excalibur.JEC_Plotter.core import Sample
from _common import *

# -- Samples: each sample is a ROOT file containing Excalibur output

_SAMPLE_DIR_V3 = "/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V3_2018-01-31"
_SAMPLE_DIR_V4 = "/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V4_2018-02-08"

SAMPLES = {
    'Data_Zmm_BCDEF_Fall17_V3': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR_V3,
        sample_file='data17_mm_BCDEF_17Nov2017.root'
    ),
    'Data_Zee_BCDEF_Fall17_V3': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR_V3,
        sample_file='data17_ee_BCDEF_17Nov2017.root'
    ),
    'MC_Zmm_DYNJ_Fall17_V3': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR_V3,
        sample_file='mc17_mm_DYNJ_Madgraph.root'
    ),
    'MC_Zee_DYNJ_Fall17_V3': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR_V3,
        sample_file='mc17_ee_DYNJ_Madgraph.root'
    ),


    'Data_Zmm_BCDEF_Fall17_V4': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR_V4,
        sample_file='data17_mm_BCDEF_17Nov2017.root'
    ),
    'Data_Zee_BCDEF_Fall17_V4': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR_V4,
        sample_file='data17_ee_BCDEF_17Nov2017.root'
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

# -- Additional Cuts

if __name__ == "__main__":
    for _sn, _s in SAMPLES.iteritems():
        print "Sample '{}':".format(_sn)
        for k, v in _s._dict.iteritems():
            print "\t{}: {}".format(k, v)
