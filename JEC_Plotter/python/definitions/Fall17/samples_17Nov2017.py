import numpy as np

from copy import deepcopy

from Excalibur.JEC_Plotter.core import Sample
from _common import *

# -- Samples: each sample is a ROOT file containing Excalibur output

_SAMPLE_DIR = "/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V3_2018-01-31"

SAMPLES = {
    'Data_Zmm_BCDEF_Fall17_V3': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR,
        sample_file='data17_mm_BCDEF_17Nov2017.root'
    ),
    'Data_Zee_BCDEF_Fall17_V3': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR,
        sample_file='data17_ee_BCDEF_17Nov2017.root'
    ),
}

# -- Additional Cuts

if __name__ == "__main__":
    for _sn, _s in SAMPLES.iteritems():
        print "Sample '{}':".format(_sn)
        for k, v in _s._dict.iteritems():
            print "\t{}: {}".format(k, v)
