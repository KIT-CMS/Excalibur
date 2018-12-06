from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D, QUANTITIES, BinSpec, CutSet
from Excalibur.JEC_Plotter.definitions.Test18.samples_18Oct2018 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
    RUN_PERIOD_CUT_DICTS,
)
from Excalibur.JEC_Plotter.utilities.plot import plot_data_mc_hist

from copy import deepcopy

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
    SELECTION_CUTS['basiccuts'] + _cut_final_no_eta,
]

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

_ADDITIONAL_CUTS_ALPHA = [
    {
        'cut': CutSet(
            '{:0>2d}_{}'.format(_i_a_cut, _a_cut.name),  # for sorting,
            weights=_a_cut.weights_list, labels=[]
        ),
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
        'label': _cut.texts[0]
    }
    for _i_cut, _cut in enumerate(QUANTITIES['absjet1eta_narrow'].make_cutsets_from_binspec())
]


def _old_workflow(sample_data, sample_mc, jecv):
    _phs = []

    _add_cuts = [_ac['cut'] for _ac in RUN_PERIOD_CUT_DICTS]

    _add_cuts.insert(0, None)

    _SAMPLES = []

    _SAMPLES.append(deepcopy(sample_mc))
    _SAMPLES[-1]['color'] = 'k'
    _SAMPLES[-1]['source_label'] = sample_mc['source_label']

    for _ac in RUN_PERIOD_CUT_DICTS:
        _SAMPLES.append(deepcopy(sample_data))
        _SAMPLES[-1]['color'] = _ac['color']
        _SAMPLES[-1]['source_label'] = '{}'.format(_ac['label'])

    #for _corr_level in ('L1L2L3', 'L1L2L3Res'):
    for _corr_level in ('L1L2L3', 'L1L2Res'):
        _ph = PlotHistograms1D(
            basename="data_mc_hist_18Oct2018_JEC{}".format(jecv),
            # there is one subplot per sample and cut in each plot
            samples=_SAMPLES,
            jec_correction_string=_corr_level,
            additional_cuts=_add_cuts,
            # each quantity cut generates a different plot
            quantities=_QUANTITIES,
            # each selection cut generates a new plot
            selection_cuts=_SELECTION_CUTS,
            normalize_to_first=True,
            show_ratio_to_first=True,
            show_cut_info_text=False,
            plot_label="Fall18 JEC {}".format(jecv)
        )
        #_phs.append(_ph)

        for _bin_cut in _ADDITIONAL_CUTS_ETA:
            break
            _ph2 = PlotHistograms1D(
                basename="data_mc_hist_etabins_18Oct2018_JEC{}".format(jecv),
                # there is one subplot per sample and cut in each plot
                samples=_SAMPLES,
                jec_correction_string=_corr_level,
                additional_cuts=_add_cuts,
                # each quantity cut generates a different plot
                quantities=_QUANTITIES,
                # each selection cut generates a new plot
                selection_cuts=[_sel_cut + _bin_cut['cut'] for _sel_cut in _SELECTION_CUTS],
                normalize_to_first=True,
                show_ratio_to_first=True,
                show_cut_info_text=False,
                plot_label="Fall18 JEC {}".format(jecv)
            )
            _phs.append(_ph2)

        for _bin_cut in _ADDITIONAL_CUTS_ZPT:
            break
            _ph2 = PlotHistograms1D(
                basename="data_mc_hist_zptbins_18Oct18_JEC{}".format(jecv),
                # there is one subplot per sample and cut in each plot
                samples=_SAMPLES,
                jec_correction_string=_corr_level,
                additional_cuts=_add_cuts,
                # each quantity cut generates a different plot
                quantities=_QUANTITIES,
                # each selection cut generates a new plot
                selection_cuts=[_sel_cut + _bin_cut['cut'] for _sel_cut in _SELECTION_CUTS],
                normalize_to_first=True,
                show_ratio_to_first=True,
                show_cut_info_text=False,
                plot_label="Fall18 JEC {}".format(jecv)
            )
            _phs.append(_ph2)

        for _bin_cut_1 in _ADDITIONAL_CUTS_ETA[17:]:
            for _bin_cut_2 in _ADDITIONAL_CUTS_ZPT:
                break
                _ph2 = PlotHistograms1D(
                    basename="data_mc_hist_zptbins_18Oct2018_JEC{}".format(jecv),
                    # there is one subplot per sample and cut in each plot
                    samples=_SAMPLES,
                    jec_correction_string=_corr_level,
                    additional_cuts=_add_cuts,
                    # each quantity cut generates a different plot
                    quantities=_QUANTITIES,
                    # each selection cut generates a new plot
                    selection_cuts=[_sel_cut + _bin_cut_1['cut'] + _bin_cut_2['cut'] for _sel_cut in _SELECTION_CUTS],
                    normalize_to_first=True,
                    show_ratio_to_first=True,
                    show_cut_info_text=False,
                    plot_label="Fall18 JEC {}".format(jecv)
                )
                _phs.append(_ph2)
                


        for _ph in _phs:
            _ph.make_plots()

if __name__ == "__main__":
    #for _jecv in ("V6_rawECAL", "V6", "V6_egmUpdate"):
    for _jecv in ("V10", ):
        for _channel in ("mm",):
            for _corr_level in ("L1L2L3", "L1L2Res"):
                if _corr_level == 'L1L2Res' and _jecv != "V10":
                    continue
                _plot_collection = plot_data_mc_hist(
                    sample_data=SAMPLES['Data_Z{}_E_Test18_JEC{}'.format(_channel, _jecv)],
                    sample_mc=SAMPLES['MC_Z{}_DYNJ_Test18_JEC{}'.format(_channel, _jecv)],
                    selection_cuts=_SELECTION_CUTS,
                    subplot_cuts=RUN_PERIOD_CUT_DICTS,
                    jec_correction_string=_corr_level,
                    quantities=_QUANTITIES,
                    sample_label="18Oct2018",
                    jec_campaign_label="Test18",
                    jec_version=_jecv,
                    normalize_to_first_histo=True,
                )

                _plot_collection.make_plots()
