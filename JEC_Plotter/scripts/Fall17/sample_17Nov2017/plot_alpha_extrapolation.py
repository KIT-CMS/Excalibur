from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D, PlotResponseExtrapolation, QUANTITIES, BinSpec, CutSet
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

_QUANTITY_PAIRS = [
    ('alpha', 'ptbalance'),
    ('alpha', 'mpf'),
]

_cut_final_no_eta = CutSet("basicToNoEta",
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
    #SELECTION_CUTS['basiccuts'] + _cut_final_no_eta
]

_ADDITIONAL_CUTS = [
    {
        'cut': None,
        'label': r"RunsBCDEF",
        'color': 'black'
    },
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

def _workflow(sample_data, sample_mc, jecv):
    _phs = []



    #for _corr_level in ('L1L2L3', 'L1L2L3Res'):
    for _corr_level in ('L1L2L3',):
        _ph = PlotResponseExtrapolation(
            basename='extrapolation_17Nov2017_JEC{}'.format(jecv),
            sample_data=sample_data,
            sample_mc=sample_mc,
            response_quantities=("ptbalance", "mpf"),
            selection_cuts=_SELECTION_CUTS,
            extrapolation_quantity='alpha',
            n_extrapolation_bins=6,
            corrections=_corr_level,
            jec_version_label="Fall17 JEC {}".format(jecv),
            additional_cut_dicts=_ADDITIONAL_CUTS,
        )

        for _plot in _ph._plots:
            pass

        _phs.append(_ph)

        for _ph in _phs:
            _ph.make_plots()

if __name__ == "__main__":
    for _jecv in ("V4",):
        _workflow(sample_data=SAMPLES['Data_Zmm_BCDEF_Fall17_{}'.format(_jecv)],
                  sample_mc=SAMPLES['MC_Zmm_DYNJ_Fall17_{}'.format(_jecv)],
                  jecv=_jecv)
        _workflow(sample_data=SAMPLES['Data_Zee_BCDEF_Fall17_{}'.format(_jecv)],
                  sample_mc=SAMPLES['MC_Zee_DYNJ_Fall17_{}'.format(_jecv)],
                  jecv=_jecv)
