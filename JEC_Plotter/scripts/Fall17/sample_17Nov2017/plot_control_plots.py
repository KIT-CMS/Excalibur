from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D
from Excalibur.JEC_Plotter.definitions.Fall17.samples_17Nov2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
)

from copy import deepcopy

_CORR_FOLDER = "L1L2L3"

_QUANTITIES = [
    'mpf', 'ptbalance',
    'npv', 'rho',
    #'npumean',
    'zpt_log', 'zphi', 'zmass',
    'jet1pt', 'jet2pt', 'jet3pt',
    'met', 'metphi',
    'jet1phi', 'jet2phi', 'jet3phi',
    'jet1pt_over_jet1ptraw'
]

# _QUANTITY_PAIRS = [
#     ('jet1phi', 'jet1eta'),
#     ('jet2phi', 'jet2eta'),
#     ('jet3phi', 'jet3eta')
# ]

_SELECTION_CUTS = [SELECTION_CUTS['finalcuts']]

_ADDITIONAL_CUTS = [
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
#    {
#        'cut': ADDITIONAL_CUTS['run_periods']['runG'],
#        'label': r"RunG",
#        'color': 'green'
#    },
#    {
#        'cut': ADDITIONAL_CUTS['run_periods']['runH'],
#        'label': r"RunH",
#        'color': 'orange'
#    }
]

def _workflow(sample, jecv):
    _phs = []

    _add_cuts = [_ac['cut'] for _ac in _ADDITIONAL_CUTS]

    _SAMPLES = []
    for _ac in _ADDITIONAL_CUTS:
        _SAMPLES.append(deepcopy(sample))
        _SAMPLES[-1]['color'] = _ac['color']
        _SAMPLES[-1]['source_label'] = '{}'.format(_ac['label'])

    _ph = PlotHistograms1D(
        basename="control_plots_hist1d_17Nov2017",
        # there is one subplot per sample and cut in each plot
        samples=_SAMPLES,
        corrections=_CORR_FOLDER,
        additional_cuts=_add_cuts,
        # each quantity cut generates a different plot
        quantities=_QUANTITIES,
        # each selection cut generates a new plot
        selection_cuts=_SELECTION_CUTS,
        show_ratio_to_first=True,
        show_cut_info_text=False,
        jec_version_label="Fall17 JEC {}".format(jecv)
    )

    _ph2 = PlotHistograms1D(
        basename="control_plots_hist1d_norm_17Nov2017",
        # there is one subplot per sample and cut in each plot
        samples=_SAMPLES,
        corrections=_CORR_FOLDER,
        additional_cuts=_add_cuts,
        # each quantity cut generates a different plot
        quantities=_QUANTITIES,
        # each selection cut generates a new plot
        selection_cuts=_SELECTION_CUTS,
        normalize_to_first=True,
        show_ratio_to_first=True,
        show_cut_info_text=False
    )

    for _plot in _ph._plots:
        pass

    #_phs.append(_ph)
    _phs.append(_ph2)

    for _ph in _phs:
        _ph.make_plots()

if __name__ == "__main__":
    _jecv = "V4"
    _workflow(SAMPLES['Data_Zmm_BCDEF_Fall17_{}'.format(_jecv)], jecv=_jecv)
    _workflow(SAMPLES['Data_Zee_BCDEF_Fall17_{}'.format(_jecv)], jecv=_jecv)
