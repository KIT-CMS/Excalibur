from Excalibur.JEC_Plotter.core.plot import _Plot1D
from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotProfiles, QUANTITIES, BinSpec, CutSet
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
    RUN_PERIOD_CUT_DICTS,
)
from Excalibur.JEC_Plotter.utilities.plot import plot_data_mc_profiles

from copy import deepcopy


_CORR_FOLDER = "L1L2L3"

#QUANTITIES['zmass'].bin_spec = BinSpec.make_equidistant(50, (90.3, 93.3))
QUANTITIES['zmass'].bin_spec = BinSpec.make_equidistant(50, (88.3, 93.3))
QUANTITIES['mpf'].bin_spec = BinSpec.make_equidistant(50, (0.8, 1.2))
QUANTITIES['ptbalance'].bin_spec = BinSpec.make_equidistant(50, (0.8, 1.2))
##QUANTITIES['ptbalance'].bin_spec = BinSpec.make_equidistant(50, (0.5, 0.9))
QUANTITIES['alpha'].bin_spec = BinSpec.make_from_bin_edges([0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.5])

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
]


if __name__ == "__main__":
    for _jecv in ("V6",):
        for _channel in ("mm", "ee"):
            for _corr_level in ("L1L2L3",):
                _pc = plot_data_mc_profiles(
                    sample_data=SAMPLES['Data_Z{}_BCDEFGH_Summer16_JEC{}'.format(_channel, _jecv)],
                    sample_mc=SAMPLES['MC_Z{}_DYNJ_Summer16_JEC{}'.format(_channel, _jecv)],
                    selection_cuts=_SELECTION_CUTS,
                    subplot_cuts=RUN_PERIOD_CUT_DICTS,
                    jec_correction_string=_corr_level,
                    quantity_pairs=_QUANTITY_PAIRS,
                    sample_label="07Aug2017",
                    jec_campaign_label="Summer16",
                    jec_version=_jecv,
                    y_subplot_label="Data/MC",
                    y_subplot_range=[0.95, 1.05],
                    plot_label="Run2016, 36 fb$^{-1}$ (13 TeV)"
                )

                # add CMS Preliminary label  
                _pc.add_text(text=r"$\\bf{CMS}$", size=25, xy=(.04, .94))
                _pc.add_text(text=r"$\\it{Preliminary}$", size=20, xy=(.04, .84))

                _pc.make_plots()
