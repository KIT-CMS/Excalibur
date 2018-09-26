import numpy as np

from copy import deepcopy

from Excalibur.JEC_Plotter.core import Sample
from _common import *
import os

# -- Samples: each sample is a ROOT file containing Excalibur output

_SAMPLE_DIR_DICT = dict(
    V3="/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V3_2018-01-31",
    V4="/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V4_JetID_90X_2018-02-17",
    V5="/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V5_2018-02-22",
    V6="/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V6_2018-02-22",
    V10="/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_2018-06-13",
    V10_noMETmodification="/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_noMETmodification_2018-07-11",
    V24="/ceph/dsavoiu/JEC/Fall17/17Nov2017_V24_2018-09-14",
)

SAMPLES = dict()

# -- DATA

for _channel in ('ee', 'mm'):
    for _jecv, _sample_dir in _SAMPLE_DIR_DICT.iteritems():
        for _run_period in ('B', 'C', 'D', 'E', 'F', 'BCDEF'):
            _filename = 'data17_{}_{}_17Nov2017.root'.format(_channel, _run_period)
            if os.path.exists(os.path.join(_sample_dir, _filename)):
                SAMPLES.update({
                    'Data_Z{}_{}_Fall17_JEC{}'.format(_channel, _run_period, _jecv): Sample.load_using_convention(
                        sample_dir=_sample_dir,
                        sample_file=_filename
                    ),
                })

# -- MC
_JECVS_MC = ['V3', 'V4', 'V10', 'V24']
for _channel in ('ee', 'mm'):
    for _jecv in _JECVS_MC:
        _sample_dir = _SAMPLE_DIR_DICT[_jecv]
        _filename = 'mc17_{}_DYNJ_Madgraph.root'.format(_channel)
        if os.path.exists(os.path.join(_sample_dir, _filename)):
            SAMPLES.update({
                'MC_Z{}_DYNJ_Fall17_JEC{}'.format(_channel, _jecv): Sample.load_using_convention(
                sample_dir=_SAMPLE_DIR_DICT[_jecv],
                sample_file=_filename
                ),
            })
# -- Additional Cuts

RUN_PERIOD_CUT_DICTS = [
    {
        'cut': ADDITIONAL_CUTS['run_periods']['runB'],
        'label': r"RunB",
        'color': 'pink'
    },
    {
        'cut': ADDITIONAL_CUTS['run_periods']['runC'],
        'label': r"RunC",
        'color': 'red'
    },
    {
        'cut': ADDITIONAL_CUTS['run_periods']['runD'],
        'label': r"RunD",
        'color': 'darkred'
    },
    {
        'cut': ADDITIONAL_CUTS['run_periods']['runE'],
        'label': r"RunE",
        'color': 'blue'
    },
    {
        'cut': ADDITIONAL_CUTS['run_periods']['runF'],
        'label': r"RunF",
        'color': 'cyan'
    },
]


if __name__ == "__main__":
    for _sn, _s in SAMPLES.iteritems():
        print "Sample '{}':".format(_sn)
        for k, v in _s._dict.iteritems():
            print "\t{}: {}".format(k, v)
