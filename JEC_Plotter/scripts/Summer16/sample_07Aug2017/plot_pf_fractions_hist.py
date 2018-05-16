from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D, QUANTITIES, BinSpec, CutSet
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
)

from copy import deepcopy

_CORR_FOLDER = "L1L2L3"

_QUANTITIES = [
    #'jet1ef',
    #'jet1mf',
    'jet1chf',
    'jet1nhf',
    'jet1pf',
]

_ABSETA_CUTS = QUANTITIES['absjet1eta'].make_cutsets_from_binspec(
        BinSpec.make_from_bin_edges([0.0, 1.3, 2.0, 2.5, 3.0, 5.0])
)

_ETA_CUTS = QUANTITIES['jet1eta'].make_cutsets_from_binspec(
        BinSpec.make_from_bin_edges([-5.0, -3.0, -2.5, -2.0, -1.3, 0.0, 1.3, 2.0, 2.5, 3.0, 5.0])
)

_PT_CUTS = QUANTITIES['jet1pt'].make_cutsets_from_binspec(
        BinSpec.make_from_bin_edges([0, 50, 100, 200, 1000])
)

_jetid_cut = CutSet(name='jet1idtight',
                    weights=['jet1nhf<0.9',
                             'jet1pf<0.9',
                             'jet1ef<0.9',
                             'jet1mf<0.8',
                             'jet1chf>0',
                             ],
                    labels=[])

_SELECTION_CUTS = []
for _pt_cut in _PT_CUTS:
    #for _eta_cut in _ETA_CUTS:
    for _abseta_cut in _ABSETA_CUTS:
        #_SELECTION_CUTS.append(SELECTION_CUTS['nocuts'] + _jetid_cut + _eta_cut + _pt_cut)
        #_SELECTION_CUTS.append(SELECTION_CUTS['nocuts'] + _eta_cut + _pt_cut)
        _SELECTION_CUTS.append(SELECTION_CUTS['basiccuts'] + _abseta_cut + _pt_cut)
        _SELECTION_CUTS.append(SELECTION_CUTS['basiccuts'] + _abseta_cut)

_ADDITIONAL_CUTS = [
    {
        'cut': ADDITIONAL_CUTS['jec_iovs']['BCD'],
        'label': r"RunBCD",
        'color': 'red'
    },
    {
        'cut': ADDITIONAL_CUTS['jec_iovs']['EFearly'],
        'label': r"RunEFearly",
        'color': 'royalblue'
    },
    {
        'cut': ADDITIONAL_CUTS['jec_iovs']['FlateGH'],
        'label': r"RunFlateGH",
        'color': 'darkgoldenrod'
    },
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
            basename="pf_fractions_hist_07Aug2017_JEC{}".format(jecv),
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
            jec_version_label="Summer16 JEC {}".format(jecv),
            y_log_scale=True
        )

        _phs.append(_ph)

        for _ph in _phs:
            _ph.make_plots()

if __name__ == "__main__":
    for _jecv in ("V6",):
        #for _channel in ("mm", "ee"):
        for _channel in ("mm",):
            _workflow(sample_data=SAMPLES['Data_Z{}_BCDEFGH_Summer16_JEC{}'.format(_channel, _jecv)],
                      sample_mc=SAMPLES['MC_Z{}_DYNJ_Summer16_JEC{}'.format(_channel, _jecv)],
                      jecv=_jecv)

