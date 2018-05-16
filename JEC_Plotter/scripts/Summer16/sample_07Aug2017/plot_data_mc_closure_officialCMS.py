from Excalibur.JEC_Plotter.core.plot import _Plot1D
from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D, QUANTITIES, BinSpec, CutSet
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
)

from copy import deepcopy

_Plot1D.Y_SUBPLOT_LABEL = "Data/MC"
_Plot1D.Y_SUBPLOT_LIMS = [0.95, 1.05]


_CORR_FOLDER = "L1L2L3"

#QUANTITIES['zmass'].bin_spec = BinSpec.make_equidistant(50, (90.3, 93.3))
QUANTITIES['zmass'].bin_spec = BinSpec.make_equidistant(50, (88.3, 93.3))
QUANTITIES['mpf'].bin_spec = BinSpec.make_equidistant(50, (0.8, 1.2))
QUANTITIES['ptbalance'].bin_spec = BinSpec.make_equidistant(50, (0.8, 1.2))
##QUANTITIES['ptbalance'].bin_spec = BinSpec.make_equidistant(50, (0.5, 0.9))
QUANTITIES['alpha'].bin_spec = BinSpec.make_from_bin_edges([0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.5])

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
QUANTITIES['zeta_wide'] = deepcopy(QUANTITIES['zeta'])
QUANTITIES['zeta_wide'].name = 'zeta_wide'
QUANTITIES['zeta_wide'].expression = 'abs(zeta)'
QUANTITIES['zeta_wide'].label = r"$|\\eta^Z|$"
QUANTITIES['zeta_wide'].bin_spec = BinSpec.make_from_bin_edges([0.000, 1.305,
                                                                2.172, 2.500,
                                                                3.139, 5.191])

#QUANTITIES['absjet1eta_wide'] = deepcopy(QUANTITIES['absjet1eta'])
#QUANTITIES['absjet1eta_wide'].name = 'absjet1eta_wide'
#QUANTITIES['absjet1eta_wide'].bin_spec = BinSpec.make_from_bin_edges([0, 0.783, 1.305, 1.93, 2.5, 2.964, 3.2, 5.191])

_QUANTITY_PAIRS = [
    ('zpt_log', 'ptbalance'),
    ('zpt_log', 'mpf'),
    ##('alpha', 'ptbalance'),
    ##('alpha', 'mpf'),
    ##('zpt_log', 'zmass'),
    #('zeta_wide', 'zmass'),
    ##('abszeta_narrow', 'zmass'),
    #('absjet1eta_wide', 'ptbalance'),
    #('absjet1eta_wide', 'mpf'),
    ##('absjet1eta_narrow', 'ptbalance'),
    ##('absjet1eta_narrow', 'mpf'),
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
        _ph = PlotHistograms2D(
            basename="data_mc_closure_CMS_07Aug2017_JEC{}".format(jecv),
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
            show_cut_info_text=False,
            show_corr_folder_text=False,
            jec_version_label="Run2016 36 fb$^{-1}$ (13 TeV)"
        )

        for _zpt_cut in _ADDITIONAL_CUTS_ZPT:
            break
            _ph2 = PlotHistograms2D(
                basename="data_mc_closure_CMS_07Aug2017_JEC{}".format(jecv),
                # there is one subplot per sample and cut in each plot
                samples=_SAMPLES,
                corrections=_corr_level,
                additional_cuts=_add_cuts,
                # each quantity cut generates a different plot
                quantity_pairs=_QUANTITY_PAIRS,
                # each selection cut generates a new plot
                selection_cuts=[_sel_cut + _zpt_cut['cut'] for _sel_cut in _SELECTION_CUTS],
                show_as_profile=True,
                show_ratio_to_first=True,
                show_cut_info_text=False,
                show_corr_folder_text=False,
                jec_version_label="Run2016 36 fb$^{-1}$ (13 TeV)"
            )
            #_phs.append(_ph2)

        # add cut labels as text
        for _p in _ph._plots:
            _p._basic_dict['texts'].extend([r"$\\bf{CMS}$", r"$\\it{Preliminary}$"])
            _p._basic_dict['texts_size'].extend([25, 20])
            _p._basic_dict['texts_x'].extend([0.04, 0.04])
            _p._basic_dict['texts_y'].extend([0.94, 0.84])

        _phs.append(_ph)

        for _ph in _phs:
            _ph.make_plots()

if __name__ == "__main__":
    for _jecv in ("V6",):
        for _channel in ("mm", "ee"):
            _workflow(sample_data=SAMPLES['Data_Z{}_BCDEFGH_Summer16_JEC{}'.format(_channel, _jecv)],
                      sample_mc=SAMPLES['MC_Z{}_DYNJ_Summer16_JEC{}'.format(_channel, _jecv)],
                      jecv=_jecv)
