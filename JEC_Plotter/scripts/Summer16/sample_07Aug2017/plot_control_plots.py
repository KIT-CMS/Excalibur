from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
)

from copy import deepcopy

_CORR_FOLDER = "L1L2L3"

_QUANTITIES = [
    'jet1pt', 'jet2pt', 'jet3pt',
    'zpt',
    'mpf', 'ptbalance', 'alpha',
]

_QUANTITY_PAIRS = [
    ('jet1phi', 'jet1eta'),
    ('jet2phi', 'jet2eta'),
    ('jet3phi', 'jet3eta')
]

_SELECTION_CUTS = [SELECTION_CUTS['finalcuts']]

_ADDITIONAL_CUTS = [
    {
        'cut': ADDITIONAL_CUTS['jec_iovs']['BCD'],
        'color': 'red',
        'label': 'BCD'
    },
    {
        'cut': ADDITIONAL_CUTS['jec_iovs']['EFearly'],
        'color': 'blue',
        'label': 'EFearly'
    },
    {
        'cut': ADDITIONAL_CUTS['jec_iovs']['FlateG'],
        'color': 'green',
        'label': 'FlateG'
    },
    {
        'cut': ADDITIONAL_CUTS['jec_iovs']['H'],
        'color': 'orange',
        'label': 'H'
    },
]

def _workflow(sample):
    _phs = []

    _add_cuts = [_ac['cut'] for _ac in _ADDITIONAL_CUTS]

    _SAMPLES = []
    for _ac in _ADDITIONAL_CUTS:
        _SAMPLES.append(deepcopy(sample))
        _SAMPLES[-1]['color'] = _ac['color']
        _SAMPLES[-1]['source_label'] = '{}'.format(_ac['label'])

    _ph = PlotHistograms1D(
        basename="control_plots_hist1d_07Aug2017",
        # there is one subplot per sample and cut in each plot
        samples=_SAMPLES,
        corrections=_CORR_FOLDER,
        additional_cuts=_add_cuts,
        # each quantity cut generates a different plot
        quantities=_QUANTITIES,
        # each selection cut generates a new plot
        selection_cuts=_SELECTION_CUTS,
        show_ratio_to_first=True,
        show_cut_info_text=False
    )

    for _plot in _ph._plots:
        pass

    _phs.append(_ph)

    for _ph in _phs:
        _ph.make_plots()

if __name__ == "__main__":
    _workflow(SAMPLES['Data_Zmm_BCDEFGH_JECV5'])
    _workflow(SAMPLES['Data_Zee_BCDEFGH_JECV5'])
