from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D, QUANTITIES, BinSpec, CutSet
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
)

from copy import deepcopy

_CORR_FOLDER = "L1L2L3"

QUANTITIES['absjet1eta_narrow'] = deepcopy(QUANTITIES['jet1eta'])
QUANTITIES['absjet1eta_narrow'].name = 'absjet1eta_narrow'
QUANTITIES['absjet1eta_narrow'].expression = 'abs(jet1eta)'
QUANTITIES['absjet1eta_narrow'].label = r"$|\\eta^{Jet1}|$"
QUANTITIES['absjet1eta_narrow'].bin_spec = BinSpec.make_from_bin_edges([0.000, 0.261, 0.522, 0.783, 1.044, 1.305,
                                                                        1.479, 1.653, 1.930, 2.172, 2.322, 2.500,
                                                                        2.650, 2.853, 2.964, 3.139, 3.489, 3.839,
                                                                        5.191])

QUANTITIES['abszeta_narrow'] = deepcopy(QUANTITIES['zeta'])
QUANTITIES['abszeta_narrow'].name = 'abszeta_narrow'
QUANTITIES['abszeta_narrow'].expression = 'abs(zeta)'
QUANTITIES['abszeta_narrow'].label = r"$|\\eta^Z|$"
QUANTITIES['abszeta_narrow'].bin_spec = BinSpec.make_from_bin_edges([0.000, 0.261, 0.522, 0.783, 1.044, 1.305,
                                                                     1.479, 1.653, 1.930, 2.172, 2.322, 2.500,
                                                                     2.650, 2.853, 2.964, 3.139, 3.489, 3.839,
                                                                     5.191])
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
    #'rho', 'npv',
    #'npumean',
    #'zpt_log', #'zphi',
    #'zmass',
    #'abszeta_narrow',
    #'jet1pt', 'jet2pt', 'jet3pt',
    #'jet1phi', 'jet2phi', 'jet3phi',
    #'absjet1eta_narrow',
    #'met', 'metphi',
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
    #SELECTION_CUTS['finalcuts'],
    SELECTION_CUTS['basiccuts'] + _cut_final_no_eta,
    #SELECTION_CUTS['nocuts'],
]

_ADDITIONAL_CUTS = [
    {
        'cut': ADDITIONAL_CUTS['jec_iovs']['BCD'],
        'color': 'red',
        'label': 'BCD'
    },
    {
        'cut': ADDITIONAL_CUTS['jec_iovs']['EFearly'],
        'color': 'royalblue',
        'label': 'EFearly'
    },
    {
        'cut': ADDITIONAL_CUTS['jec_iovs']['FlateGH'],
        'color': 'darkgoldenrod',
        'label': 'FlateGH'
    },
    # {
    #     'cut': ADDITIONAL_CUTS['jec_iovs']['H'],
    #     'color': 'orange',
    #     'label': 'H'
    # },
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
        _ph = PlotHistograms1D(
            basename="data_mc_hist_07Aug2017_JEC{}".format(jecv),
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
            show_cut_info_text=False,
            jec_version_label="Summer16 JEC {}".format(jecv)
        )
        #_phs.append(_ph)

        for _bin_cut in _ADDITIONAL_CUTS_ETA:
            break
            _ph2 = PlotHistograms1D(
                basename="data_mc_hist_etabins_07Aug2017_JEC{}".format(jecv),
                # there is one subplot per sample and cut in each plot
                samples=_SAMPLES,
                corrections=_corr_level,
                additional_cuts=_add_cuts,
                # each quantity cut generates a different plot
                quantities=_QUANTITIES,
                # each selection cut generates a new plot
                selection_cuts=[_sel_cut + _bin_cut['cut'] for _sel_cut in _SELECTION_CUTS],
                normalize_to_first=True,
                show_ratio_to_first=True,
                show_cut_info_text=False,
                jec_version_label="Summer16 JEC {}".format(jecv)
            )
            _phs.append(_ph2)

        for _bin_cut in _ADDITIONAL_CUTS_ZPT:
            break
            _ph2 = PlotHistograms1D(
                basename="data_mc_hist_zptbins_07Aug2017_JEC{}".format(jecv),
                # there is one subplot per sample and cut in each plot
                samples=_SAMPLES,
                corrections=_corr_level,
                additional_cuts=_add_cuts,
                # each quantity cut generates a different plot
                quantities=_QUANTITIES,
                # each selection cut generates a new plot
                selection_cuts=[_sel_cut + _bin_cut['cut'] for _sel_cut in _SELECTION_CUTS],
                normalize_to_first=True,
                show_ratio_to_first=True,
                show_cut_info_text=False,
                jec_version_label="Summer16 JEC {}".format(jecv)
            )
            _phs.append(_ph2)

        for _bin_cut_1 in _ADDITIONAL_CUTS_ETA[17:]:
            for _bin_cut_2 in _ADDITIONAL_CUTS_ZPT:
                _ph2 = PlotHistograms1D(
                    basename="data_mc_hist_zptbins_07Aug2017_JEC{}".format(jecv),
                    # there is one subplot per sample and cut in each plot
                    samples=_SAMPLES,
                    corrections=_corr_level,
                    additional_cuts=_add_cuts,
                    # each quantity cut generates a different plot
                    quantities=_QUANTITIES,
                    # each selection cut generates a new plot
                    selection_cuts=[_sel_cut + _bin_cut_1['cut'] + _bin_cut_2['cut'] for _sel_cut in _SELECTION_CUTS],
                    normalize_to_first=True,
                    show_ratio_to_first=True,
                    show_cut_info_text=False,
                    jec_version_label="Summer16 JEC {}".format(jecv)
                )
                _phs.append(_ph2)
                


        for _ph in _phs:
            _ph.make_plots()

if __name__ == "__main__":
    #for _jecv in ("V6_rawECAL", "V6", "V6_egmUpdate"):
    for _jecv in ("V6",):
        for _channel in ("mm", "ee"):
            _workflow(sample_data=SAMPLES['Data_Z{}_BCDEFGH_Summer16_JEC{}'.format(_channel, _jecv)],
                      sample_mc=SAMPLES['MC_Z{}_DYNJ_Summer16_JEC{}'.format(_channel, _jecv)],
                      jecv=_jecv)

    #_jecv = "V6"
    #_workflow(sample_data=SAMPLES['Data_Zmm_BCDEFGH_Summer16_JEC{}'.format(_jecv)],
    #          sample_mc=SAMPLES['MC_Zmm_DYNJ_Summer16_JEC{}'.format(_jecv)],
    #          jecv=_jecv)
