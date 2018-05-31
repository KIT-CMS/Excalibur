from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
    RUN_PERIOD_CUT_DICTS,
)

from copy import deepcopy

_CORR_FOLDER = "L1L2L3"

_QUANTITY_PAIRS = [
    ('alpha', 'ptbalance'),
    ('alpha', 'mpf'),
    #('alpha', 'jetrpf'),
    ('jet1eta', 'jet1phi'),
]

_SELECTION_CUTS = [SELECTION_CUTS['noalphacut']]


def _workflow(sample):
    _phs = []

    _add_cuts = [_ac['cut'] for _ac in RUN_PERIOD_CUT_DICTS]

    _SAMPLES = []
    for _ac in RUN_PERIOD_CUT_DICTS:
        _SAMPLES.append(deepcopy(sample))
        _SAMPLES[-1]['color'] = _ac['color']
        _SAMPLES[-1]['source_label'] = '{}'.format(_ac['label'])

    _ph = PlotHistograms2D(
        basename="responses_2d_07Aug2017",
        # there is one subplot per sample and cut in each plot
        sample=sample,
        jec_correction_string=_CORR_FOLDER,
        # each quantity cut generates a different plot
        quantity_pairs=_QUANTITY_PAIRS,
        # each selection cut generates a new plot
        selection_cuts=_SELECTION_CUTS,
        show_cut_info_text=False
    )

    for _p in _ph._plots:
        #_p._basic_dict['lines'] = [1.0]
        _p._basic_dict['z_expressions'] = ['jet1res']
        _p._basic_dict['z_lims'] = [0.8, 1.1]
        _p._basic_dict['tree_draw_options'] = 'prof'

    _ph.make_plots()

if __name__ == "__main__":
    for _channel in ("ee", "mm"):
        _workflow(SAMPLES['Data_Z{}_BCDEFGH_Summer16_JECV6'.format(_channel)])
