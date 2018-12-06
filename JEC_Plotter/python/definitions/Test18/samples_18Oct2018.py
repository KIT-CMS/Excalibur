import numpy as np

from copy import deepcopy

from Excalibur.JEC_Plotter.core import Sample
from _common import *
import os

# -- Samples: each sample is a ROOT file containing Excalibur output

_SAMPLE_DIR_DICT = dict(
    #V10="/storage/c/dsavoiu/excalibur_results_calibration/Fall17/09May2018_V10_2018-06-22",
    V10="/ceph/msauter/actual_data",
    #V10_noMETmodification="/storage/c/dsavoiu/excalibur_results_calibration/Fall17/09May2018_V10_noMETmodification_2018-07-11",
    #V10_noMETmodification="/storage/c/dsavoiu/excalibur_results_calibration/Fall17/09May2018_V10_noMETmodification_2018-07-11",
)

SAMPLES = dict()

# -- DATA

#for _channel in ('ee', 'mm'):
for _channel in ('mm', 'ee'):
    for _jecv, _sample_dir in _SAMPLE_DIR_DICT.iteritems():
        for _run_period in ('B', 'C', 'D', 'E', 'F', 'BCDEF'):
            #_filename = 'excalibur_data18_{}_{}.root'.format(_channel, _run_period)
            _filename = 'data18_{}_{}_18Oct.root'.format(_channel, _run_period)
            # TODO: SAMPLES????
            if os.path.exists(os.path.join(_sample_dir, _filename)):
                SAMPLES.update({
                    'Data_Z{}_{}_Test18_JEC{}'.format(_channel, _run_period, _jecv): Sample.load_using_convention(
                        sample_dir=_sample_dir,
                        sample_file=_filename
                    ),
                })

# -- MC
_JECVS_MC = ['V10']
#for _channel in ('ee', 'mm'):
for _channel in ('mm',):
    for _jecv in _JECVS_MC:
        _sample_dir = _SAMPLE_DIR_DICT[_jecv]
        #_filename = 'excalibur_mc18_{}_DY4J_Madgraph.root'.format(_channel)
        _filename = 'mc18_{}_DYNJ_Madgraph.root'.format(_channel)
        print('MC_Z{}_DYNJ_Test18_JEC{}'.format(_channel, _jecv))
        if os.path.exists(os.path.join(_sample_dir, _filename)):
            SAMPLES.update({
                'MC_Z{}_DYNJ_Test18_JEC{}'.format(_channel, _jecv): Sample.load_using_convention(
                    sample_dir=_SAMPLE_DIR_DICT[_jecv],
                    sample_file=_filename)
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
]


if __name__ == "__main__":
    for _sn, _s in SAMPLES.iteritems():
        print "Sample '{}':".format(_sn)
        for k, v in _s._dict.iteritems():
            print "\t{}: {}".format(k, v)
