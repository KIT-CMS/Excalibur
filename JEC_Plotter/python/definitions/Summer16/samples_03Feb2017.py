import numpy as np

from Excalibur.JEC_Plotter.core import Sample
from _common import *

# -- Samples: each sample is a ROOT file containing Excalibur output

_SAMPLE_DIR = "/storage/c/tberger/excalibur_results_calibration/Summer16_03Feb2017BCD_V3_2017-11-13"

SAMPLES = {
    'Data_Zmm_BCDEFGH': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR,
        sample_file='data16_mm_BCDEFGH_DoMuRemini.root'
    ),
    'Data_Zmm_BCD': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR,
        sample_file='data16_mm_BCD_DoMuRemini.root'
    ),
    'Data_Zee_BCDEFGH': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR,
        sample_file='data16_ee_BCDEFGH_DoElRemini.root'
    ),
    'Data_Zee_BCD': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR,
        sample_file='data16_ee_BCD_DoElRemini.root'
    ),
}

if __name__ == "__main__":
    for _sn, _s in SAMPLES.iteritems():
        print "Sample '{}':".format(_sn)
        for k, v in _s._dict.iteritems():
            print "\t{}: {}".format(k, v)
