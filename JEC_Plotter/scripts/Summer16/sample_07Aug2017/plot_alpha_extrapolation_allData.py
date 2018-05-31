from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D, PlotExtrapolations, QUANTITIES, BinSpec, CutSet
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
    RUN_PERIOD_CUT_DICTS,
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

RUN_PERIOD_CUT_DICTS.insert(0,
    {
        'cut': None,
        'label': r"RunsBCDEFGH",
        'color': 'black'
    }
)

_ADDITIONAL_CUTS_ZPT = [
    {
        'cut': CutSet(
            '{:0>2d}_{}'.format(_i_z_cut, _z_cut.name),  # for sorting,
            weights=_z_cut.weights_list, labels=[]
        ),
        'label': _z_cut.texts[0]
    }
    for _i_z_cut, _z_cut in enumerate(QUANTITIES['zpt'].make_cutsets_from_binspec())
]

def _workflow(sample_data, sample_mc, jecv):
    _phs = []

    #for _corr_level in ('L1L2L3', 'L1L2L3Res'):
    for _corr_level in ('L1L2L3',):
        _ph = PlotExtrapolations(
            basename='extrapolation_07Aug2017_JEC{}'.format(jecv),
            sample_data=sample_data,
            sample_mc=sample_mc,
            response_quantities=("ptbalance", "mpf"),
            selection_cuts=_SELECTION_CUTS,
            extrapolation_quantity='alpha',
            n_extrapolation_bins=6,
            fit_function_range=[0.0, 0.3],
            jec_correction_string=_corr_level,
            show_corr_folder_text=False,
            plot_label="Run2016, 35.82 fb$^{-1}$ (13 TeV)",
            additional_cut_dicts=RUN_PERIOD_CUT_DICTS[:1],
        )

        # add cut labels as text
        for _p in _ph._plots:
            _p._basic_dict['formats'] = ['pdf', 'png']
            _p._basic_dict['y_subplot_label'] = "Data/MC"
            _p._basic_dict['texts'].extend([r"$\\bf{CMS}$", r"$\\it{Preliminary}$"])
            _p._basic_dict['texts_size'].extend([25, 20])
            _p._basic_dict['texts_x'].extend([0.04, 0.04])
            _p._basic_dict['texts_y'].extend([0.94, 0.84])

        _phs.append(_ph)

    for _ph in _phs:
        _ph.make_plots()

if __name__ == "__main__":
    _jecv_mc = "V6"
    for _jecv in ("V6",):
        for _channel in ("mm", "ee"):
            _workflow(sample_data=SAMPLES['Data_Z{}_BCDEFGH_Summer16_JEC{}'.format(_channel, _jecv)],
                      sample_mc=SAMPLES['MC_Z{}_DYNJ_Summer16_JEC{}'.format(_channel, _jecv_mc)],
                      jecv=_jecv)
