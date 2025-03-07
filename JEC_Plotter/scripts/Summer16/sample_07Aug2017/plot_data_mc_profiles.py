from Excalibur.JEC_Plotter.core import PlotProfiles, QUANTITIES, BinSpec, CutSet
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
    RUN_PERIOD_CUT_DICTS,
)
from Excalibur.JEC_Plotter.utilities.plot import plot_data_mc_profiles

from copy import deepcopy

QUANTITIES['zmass'].bin_spec = BinSpec.make_equidistant(50, (88.3, 93.3))
QUANTITIES['mpf'].bin_spec = BinSpec.make_equidistant(50, (0.8, 1.2))
QUANTITIES['ptbalance'].bin_spec = BinSpec.make_equidistant(50, (0.8, 1.2))
QUANTITIES['alpha'].bin_spec = BinSpec.make_from_bin_edges([0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.5])


_QUANTITY_PAIRS = [
    ('zpt_log', 'ptbalance'),
    ('zpt_log', 'mpf'),
    ##('alpha', 'ptbalance'),
    ##('alpha', 'mpf'),
    ('zpt_log', 'zmass'),
    #('zeta_wide', 'zmass'),
    ('abszeta_narrow', 'zmass'),
    ##('zeta_narrow', 'zmass'),
    ('absjet1eta_narrow', 'ptbalance'),
    ('absjet1eta_narrow', 'mpf'),
    ##('jet1eta_narrow', 'ptbalance'),
    ##('jet1eta_narrow', 'mpf'),
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


if __name__ == "__main__":
    #for _jecv in ("V6", "V12_noEGMss",):
    #for _jecv in ("V12_noEGMss", "V12_backportEGMss"):
    #for _jecv in ("V12_backportEGMss", "V12_backportEGMss_npvGood"):
    for _jecv in ("V15",):
        #for _channel in ("mm", "ee"):
        for _channel in ("mm",):
            for _corr_level in ("L1L2L3", "L1L2Res",):
                if _corr_level == "L1L2Res" and _jecv not in ("V12_noEGMss", "V12_backportEGMss", "V12_backportEGMss_npvGood", "V15"):
                    continue
                _plot_collection = plot_data_mc_profiles(
                    sample_data=SAMPLES['Data_Z{}_BCDEFGH_Summer16_JEC{}'.format(_channel, _jecv)],
                    sample_mc=SAMPLES['MC_Z{}_DYNJ_Summer16_JEC{}'.format(_channel, _jecv)],
                    selection_cuts=_SELECTION_CUTS,
                    subplot_cuts=RUN_PERIOD_CUT_DICTS,
                    jec_correction_string=_corr_level,
                    quantity_pairs=_QUANTITY_PAIRS,
                    sample_label="07Aug2017",
                    jec_campaign_label="Summer16",
                    jec_version=_jecv,
                )
 
                _plot_collection.make_plots()
