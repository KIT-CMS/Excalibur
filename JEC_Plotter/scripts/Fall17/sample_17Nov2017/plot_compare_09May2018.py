from Excalibur.JEC_Plotter.core import PlotProfiles, QUANTITIES, BinSpec, CutSet
from Excalibur.JEC_Plotter.definitions.Fall17.samples_17Nov2017 import (
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
    RUN_PERIOD_CUT_DICTS,
)
from Excalibur.JEC_Plotter.definitions.Fall17.samples_17Nov2017 import SAMPLES as SAMPLES_17Nov2017
from Excalibur.JEC_Plotter.definitions.Fall17.samples_09May2018 import SAMPLES as SAMPLES_09May2018
from Excalibur.JEC_Plotter.utilities.plot import plot_data_mc_profiles

from copy import deepcopy

QUANTITIES['zmass'].bin_spec = BinSpec.make_equidistant(50, (88.3, 93.3))
QUANTITIES['mpf'].bin_spec = BinSpec.make_equidistant(50, (0.8, 1.2))
QUANTITIES['ptbalance'].bin_spec = BinSpec.make_equidistant(50, (0.8, 1.2))
QUANTITIES['alpha'].bin_spec = BinSpec.make_from_bin_edges([0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.5])


_QUANTITY_PAIRS = [
    #('zpt_log', 'ptbalance'),
    #('zpt_log', 'mpf'),
    ##('alpha', 'ptbalance'),
    ##('alpha', 'mpf'),
    #('zpt_log', 'zmass'),
    #('zeta_wide', 'zmass'),
    #('abszeta_narrow', 'zmass'),
    #('zeta_narrow', 'zmass'),
    #('absjet1eta_narrow', 'ptbalance'),
    #('absjet1eta_narrow', 'mpf'),
    ('jet1eta_narrow', 'ptbalance'),
    ('jet1eta_narrow', 'mpf'),
    #('e1eta', 'e1pt'),
    #('e2eta', 'e2pt'),
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

#_SELECTION_CUTS = [
#    SELECTION_CUTS['finalcuts'],
#    SELECTION_CUTS['basiccuts'] + _cut_final_no_eta,
#]

_SELECTION_CUTS = [
    #SELECTION_CUTS['finalcuts'],
    SELECTION_CUTS['basiccuts'] + _cut_final_no_eta + _pt_cut for _pt_cut in QUANTITIES['zpt'].make_cutsets_from_binspec(
            BinSpec.make_from_bin_edges([30, 50, 200, 500, 1000])
        )
]


if __name__ == "__main__":
    for _jecv_mc, _jecv_data in [("V10", "V10")]:
        for _channel in ("mm", "ee"):
            #for _corr_level in ("L1L2L3", "L1L2L3Res", "L1L2Res"):
            for _corr_level in ("L1L2L3",):
                if _corr_level == "L1L2Res" and _jecv_data != "V10":
                    continue
                
                _sample1 = SAMPLES_17Nov2017['Data_Z{}_F_Fall17_JEC{}'.format(_channel, _jecv_data)]
                _sample2 = SAMPLES_09May2018['Data_Z{}_F_Fall17_JEC{}'.format(_channel, _jecv_data)]

                _sample1['source_label'] = 'Run2017F, 17Nov2017'
                _sample1['color'] = 'black'
                _sample2['source_label'] = 'Run2017F, 09May2018'
                _sample2['color'] = 'green'

                _plot_collection = PlotProfiles(
                        # there is one subplot per sample and cut in each plot
                        samples=[_sample1, _sample2],
                        selection_cuts=_SELECTION_CUTS,
                        jec_correction_string=_corr_level,
                        additional_cuts=None,
                        # each quantity cut generates a different plot
                        quantity_pairs=_QUANTITY_PAIRS,
                        # each selection cut generates a new plot
                        plot_label="Run2017 (JEC {})".format(_jecv_data),
                        show_ratio_to_first=True,
                        show_first_in_ratio=False,
                        cut_info_text_topleft_xy=(.35, .80)
                )

                _plot_collection.make_plots()
