from Excalibur.JEC_Plotter.core.plot import _Plot1D
from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D, QUANTITIES, BinSpec, CutSet
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
    RUN_PERIOD_CUT_DICTS,
)

from copy import deepcopy

_eta_binspec = BinSpec.make_from_bin_edges([
    -5.191, -3.839, -3.489, -3.139, -2.964,
    -2.853, -2.650, -2.500, -2.322, -2.172,
    -1.930, -1.653, -1.479, -1.305, -1.044,
    -0.783, -0.522, -0.261,
    0.000, 0.261, 0.522, 0.783, 1.044, 1.305,
    1.479, 1.653, 1.930, 2.172, 2.322, 2.500,
    2.650, 2.853, 2.964, 3.139, 3.489, 3.839,
    5.191]
)

_jet1_eta_binspec = BinSpec.make_from_bin_edges([
    -1.305, -1.044, -0.783, -0.522, -0.261,
    0.000, 0.261, 0.522, 0.783, 1.044, 1.305,
])

_abs_eta_binspec = BinSpec.make_from_bin_edges([
  0.000, 0.261, 0.522, 0.783, 1.044, 1.305,
  1.479, 1.653, 1.930, 2.172, 2.322, 2.500,
  2.650, 2.853, 2.964, 3.139, 3.489, 3.839,
  5.191
])

_CORR_FOLDER = "L1L2L3"

QUANTITIES['absjet1eta_narrow'] = deepcopy(QUANTITIES['jet1eta'])
QUANTITIES['absjet1eta_narrow'].name = 'absjet1eta_narrow'
QUANTITIES['absjet1eta_narrow'].expression = 'abs(jet1eta)'
QUANTITIES['absjet1eta_narrow'].label = r"$|\\eta^{Jet1}|$"
QUANTITIES['absjet1eta_narrow'].bin_spec = _abs_eta_binspec

for _obj_name in ('jet1', 'jet2', 'jet3', 'z'):
    if '{}eta'.format(_obj_name) not in QUANTITIES:
        continue
    QUANTITIES['{}eta_narrow'.format(_obj_name)] = deepcopy(QUANTITIES['{}eta'.format(_obj_name)])
    QUANTITIES['{}eta_narrow'.format(_obj_name)].name = '{}eta_narrow'.format(_obj_name)
    QUANTITIES['{}eta_narrow'.format(_obj_name)].bin_spec = _eta_binspec

QUANTITIES['jet1eta_narrow'.format(_obj_name)].bin_spec = _jet1_eta_binspec

QUANTITIES['zpt_400'] = deepcopy(QUANTITIES['zpt'])
QUANTITIES['zpt_400'].name = 'zpt_400'
QUANTITIES['zpt_400'].bin_spec = BinSpec.make_equidistant(50, (0, 500))

#QUANTITIES['zeta_narrow'] = deepcopy(QUANTITIES['zeta'])
#QUANTITIES['zeta_narrow'].name = 'zeta_narrow'
#QUANTITIES['zeta_narrow'].expression = 'zeta'
#QUANTITIES['zeta_narrow'].label = r"$\\eta^Z$"
#QUANTITIES['zeta_narrow'].bin_spec = _eta_binspec

QUANTITIES['abszeta_narrow'] = deepcopy(QUANTITIES['zeta'])
QUANTITIES['abszeta_narrow'].name = 'abszeta_narrow'
QUANTITIES['abszeta_narrow'].expression = 'abs(zeta)'
QUANTITIES['abszeta_narrow'].label = r"$|\\eta^Z|$"
QUANTITIES['abszeta_narrow'].bin_spec = _abs_eta_binspec

QUANTITIES['abszeta_wide'] = deepcopy(QUANTITIES['zeta'])
QUANTITIES['abszeta_wide'].name = 'abszeta_wide'
QUANTITIES['abszeta_wide'].expression = 'abs(zeta)'
QUANTITIES['abszeta_wide'].label = r"$|\\eta^Z|$"
QUANTITIES['abszeta_wide'].bin_spec = BinSpec.make_from_bin_edges([0.000, 1.305,
                                                                   2.172, 2.500,
                                                                   3.139, 5.191])
_QUANTITIES = [
    #'alpha',
    'mpf', 'ptbalance',
    'rho', 'npv',
    #'npumean',
    'zpt_log', 'zpt_400', #'zphi',
    'zmass',
    #'abszeta_narrow',
    'jet1pt', 'jet2pt', 'jet3pt',
    #'jet1phi', 'jet2phi', 'jet3phi',
    'absjet1eta_narrow',
    'met', #'metphi',
]

_QUANTITIES = [
    #'muminuspt', 'mupluspt',
    #'eminuspt', 'epluspt',
    #'muminuseta', 'mupluseta',
    #'eminuseta', 'epluseta',
    #'zeta_narrow',
    #'zpt_400',
    'jet1pt', 'jet2pt', 'jet3pt',
    'jet1eta_narrow',
    #'jet2eta_narrow',
    #'jet3eta_narrow',
]

_QUANTITY_PAIRS = [
    ("mpf", "ptbalance"),
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
    #SELECTION_CUTS['basiccuts'] + _cut_final_no_eta,
    #SELECTION_CUTS['nocuts'],
]

_ADDITIONAL_CUTS_ZPT = [
    {
        'cut': CutSet(
            '{:0>2d}_{}'.format(_i_z_cut, _z_cut.name),  # for sorting,
            weights=_z_cut.weights_list, labels=[]
        ),
        #'label': r"${} < p_\\mathrm{T}^\\mathrm{Z} / GeV \\leq {}$".format(_z_cut.range[0], _z_cut.range[1]),
        'label': _z_cut.texts[0]
    }
    for _i_z_cut, _z_cut in enumerate(QUANTITIES['zpt'].make_cutsets_from_binspec())
]

_ADDITIONAL_CUTS_ALPHA = [
    {
        'cut': CutSet(
            '{:0>2d}_{}'.format(_i_a_cut, _a_cut.name),  # for sorting,
            weights=_a_cut.weights_list, labels=[]
        ),
        #'label': r"${} < p_\\mathrm{T}^\\mathrm{Z} / GeV \\leq {}$".format(_z_cut.range[0], _z_cut.range[1]),
        'label': _a_cut.texts[0]
    }
    for _i_a_cut, _a_cut in enumerate(QUANTITIES['alpha'].make_cutsets_from_binspec(
        BinSpec.make_from_bin_edges([0.0, 0.05, 0.1, 0.15, 0.2, 0.3])
    ))
]

_ADDITIONAL_CUTS_ETA = [
    {
        'cut': CutSet(
            '{:0>2d}_{}'.format(_i_cut, _cut.name),  # for sorting,
            weights=_cut.weights_list, labels=[]
        ),
        #'label': r"${} < p_\\mathrm{T}^\\mathrm{Z} / GeV \\leq {}$".format(_z_cut.range[0], _z_cut.range[1]),
        'label': _cut.texts[0]
    }
    for _i_cut, _cut in enumerate(QUANTITIES['absjet1eta_narrow'].make_cutsets_from_binspec())
]


def _workflow(sample_data, sample_mc, jecv):
    _phs = []

    #_add_cuts = [_ac['cut'] for _ac in RUN_PERIOD_CUT_DICTS]
    #_add_cuts.insert(0, None)

    _SAMPLES = []

    _SAMPLES.append(deepcopy(sample_mc))
    _SAMPLES[-1]['color'] = '#7293cb' #'royalblue'
    _SAMPLES[-1]['marker'] = 'bar'
    _SAMPLES[-1]['step_flag'] = False
    _SAMPLES[-1]['source_label'] = sample_mc['source_label']

    _SAMPLES.append(deepcopy(sample_data))
    _SAMPLES[-1]['color'] = 'k'
    _SAMPLES[-1]['marker'] = '.'
    _SAMPLES[-1]['step_flag'] = False
    _SAMPLES[-1]['source_label'] = sample_data['source_label']


    #for _corr_level in ('L1L2L3', 'L1L2L3Res'):
    for _corr_level in ('L1L2L3',):
        _ph = PlotHistograms1D(
            basename="data_mc_hist_allData_07Aug2017_JEC{}".format(jecv),
            # there is one subplot per sample and cut in each plot
            samples=_SAMPLES,
            jec_correction_string=_corr_level,
            additional_cuts=None, #[None]*len(_SAMPLES),
            # each quantity cut generates a different plot
            quantities=_QUANTITIES,
            # each selection cut generates a new plot
            selection_cuts=_SELECTION_CUTS,
            normalize_to_first_histo=True,
            show_ratio_to_first=True,
            show_cut_info_text=True,  
            show_corr_folder_text=False,
            plot_label="Run2016, 35.82 fb$^{-1}$ (13 TeV)",
            y_subplot_label="Data/MC",
            y_subplot_range=[0.78, 1.22],
        )
        _phs.append(_ph)

        # add cut labels as text
        for _p in _ph._plots:
            if _p._qs[0].name in ('zpt_400', 'jet1pt', 'jet2pt', 'jet3pt'):
                _p._basic_dict['y_log'] = True
            _p._basic_dict['formats'] = ['pdf', 'png']
            _p._basic_dict['texts'].extend([r"$\\bf{CMS}$", r"$\\it{Preliminary}$"])
            _p._basic_dict['texts_size'].extend([25, 20])
            _p._basic_dict['texts_x'].extend([0.04, 0.04])
            _p._basic_dict['texts_y'].extend([0.94, 0.84])

    for _ph in _phs:
        _ph.make_plots()


if __name__ == "__main__":
    for _jecv in ("V6",):
        for _channel in ("mm", "ee"):
            _workflow(sample_data=SAMPLES['Data_Z{}_BCDEFGH_Summer16_JEC{}'.format(_channel, _jecv)],
                      sample_mc=SAMPLES['MC_Z{}_DYNJ_Summer16_JEC{}'.format(_channel, _jecv)],
                      jecv=_jecv)
