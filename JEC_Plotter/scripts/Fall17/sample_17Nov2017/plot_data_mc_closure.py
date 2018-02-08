from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D, QUANTITIES, BinSpec, CutSet
from Excalibur.JEC_Plotter.definitions.Fall17.samples_17Nov2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
)

from copy import deepcopy

_CORR_FOLDER = "L1L2L3"

QUANTITIES['mpf'].bin_spec = BinSpec.make_equidistant(50, (0.8, 1.2))
QUANTITIES['ptbalance'].bin_spec = BinSpec.make_equidistant(50, (0.8, 1.2))
QUANTITIES['alpha'].bin_spec = BinSpec.make_from_bin_edges([0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.5])

QUANTITIES['jet1eta_narrow'] = deepcopy(QUANTITIES['jet1eta'])
QUANTITIES['jet1eta_narrow'].name = 'jet1eta_narrow'
QUANTITIES['jet1eta_narrow'].bin_spec = BinSpec.make_from_bin_edges([0.000, 0.261, 0.522, 0.783, 1.044, 1.305,
                                                                     1.479, 1.653, 1.930, 2.172, 2.322, 2.500,
                                                                     2.650, 2.853, 2.964, 3.139, 3.489, 3.839,
                                                                     5.191])

#QUANTITIES['jet1eta_wide'] = deepcopy(QUANTITIES['jet1eta'])
#QUANTITIES['jet1eta_wide'].name = 'jet1eta_wide'
#QUANTITIES['jet1eta_wide'].bin_spec = BinSpec.make_from_bin_edges([0, 0.783, 1.305, 1.93, 2.5, 2.964, 3.2, 5.191])

_QUANTITIES = [
    'mpf', 'ptbalance',
    'rhoo',
    #'npumean',
    'zpt_log', 'zphi', 'zmass',
    'jet1pt', 'jet2pt', 'jet3pt',
    'met', 'metphi',
    'jet1phi', 'jet2phi', 'jet3phi',
]

_QUANTITY_PAIRS = [
    ('zpt_log', 'ptbalance'),
    ('zpt_log', 'mpf'),
    ('alpha', 'ptbalance'),
    ('alpha', 'mpf'),
    #('jet1eta_wide', 'ptbalance'),
    #('jet1eta_wide', 'mpf'),
    ('jet1eta_narrow', 'ptbalance'),
    ('jet1eta_narrow', 'mpf'),
]

_cut_final_no_eta = CutSet("basicToNoAlpha",
    weights=[
        "alpha<0.3",
        "zpt>30",
    ],
    labels=[
        r"$\\alpha<0.3$",
        r"$p_\\mathrm{T}^\\mathrm{Z}>30~GeV$",
    ]
)

_SELECTION_CUTS = [
    SELECTION_CUTS['finalcuts'],
    SELECTION_CUTS['basiccuts'] + _cut_final_no_eta
]

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

def _workflow(sample_data, sample_mc, jecv):
    _phs = []

    _add_cuts = [_ac['cut'] for _ac in _ADDITIONAL_CUTS]

    _add_cuts.insert(0, None)

    _SAMPLES = []

    _SAMPLES.append(deepcopy(sample_mc))
    _SAMPLES[-1]['color'] = 'k'
    _SAMPLES[-1]['source_label'] = sample_mc['source_label']

    for _ac in _ADDITIONAL_CUTS:
        _SAMPLES.append(deepcopy(sample_data))
        _SAMPLES[-1]['color'] = _ac['color']
        _SAMPLES[-1]['source_label'] = '{}'.format(_ac['label'])

    #for _corr_level in ('L1L2L3', 'L1L2L3Res'):
    for _corr_level in ('L1L2L3',):
        _ph2 = PlotHistograms2D(
            basename="data_mc_17Nov2017_JEC{}".format(jecv),
            # there is one subplot per sample and cut in each plot
            samples=_SAMPLES,
            corrections=_corr_level,
            additional_cuts=_add_cuts,
            # each quantity cut generates a different plot
            quantity_pairs=_QUANTITY_PAIRS,
            # each selection cut generates a new plot
            selection_cuts=_SELECTION_CUTS,
            show_as_profile=True,
            show_ratio_to_first=True,
            show_cut_info_text=False
        )
        _ph = PlotHistograms1D(
            basename="data_mc_hist_17Nov2017_JEC{}".format(jecv),
            # there is one subplot per sample and cut in each plot
            samples=_SAMPLES,
            corrections=_corr_level,
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

        _phs.append(_ph)
        _phs.append(_ph2)

        for _ph in _phs:
            _ph.make_plots()

if __name__ == "__main__":
    _jecv = "V3"
    _workflow(sample_data=SAMPLES['Data_Zmm_BCDEF_Fall17_{}'.format(_jecv)],
              sample_mc=SAMPLES['MC_Zmm_DYNJ_Fall17_{}'.format(_jecv)],
              jecv=_jecv)
    _workflow(sample_data=SAMPLES['Data_Zee_BCDEF_Fall17_{}'.format(_jecv)],
              sample_mc=SAMPLES['MC_Zee_DYNJ_Fall17_{}'.format(_jecv)],
              jecv=_jecv)

    _jecv = "V4"
    _workflow(sample_data=SAMPLES['Data_Zmm_BCDEF_Fall17_{}'.format(_jecv)],
              sample_mc=SAMPLES['MC_Zmm_DYNJ_Fall17_{}'.format(_jecv)],
              jecv=_jecv)
    _workflow(sample_data=SAMPLES['Data_Zee_BCDEF_Fall17_{}'.format(_jecv)],
              sample_mc=SAMPLES['MC_Zee_DYNJ_Fall17_{}'.format(_jecv)],
              jecv=_jecv)
