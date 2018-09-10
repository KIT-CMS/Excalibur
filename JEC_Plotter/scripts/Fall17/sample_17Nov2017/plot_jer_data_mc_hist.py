from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D, QUANTITIES, BinSpec, CutSet,PlotProfiles
from Excalibur.JEC_Plotter.definitions.Fall17.samples_17Nov2017 import (
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
#    SELECTION_CUTS['basiccuts'] + _cut_final_no_eta,
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



if __name__ == "__main__":
    #for _jecv in ("V6_rawECAL", "V6", "V6_egmUpdate"):
    _jecv_mc = "V10"
    for _jecv in ("V10",):
        for _channel in ("mm", "ee"):
            for _corr_level in ("L1L2L3","L1L2L3Res"):
                _plot_collection = plot_data_mc_hist(
                    sample_data=SAMPLES['Data_Z{}_BCDEF_Fall17_JEC{}'.format(_channel, _jecv)],
                    sample_mc=SAMPLES['MC_Z{}_DYNJ_Fall17_JEC{}'.format(_channel, _jecv_mc)],
                    selection_cuts=_SELECTION_CUTS,
                    subplot_cuts=RUN_PERIOD_CUT_DICTS,
                    y_subplot_range=[0.8,1.2],
                    jec_correction_string=_corr_level,
                    quantities=_QUANTITIES,
                    sample_label="17Nov2017",
                    jec_campaign_label="Fall17",
                    jec_version=_jecv,
                    normalize_to_first_histo=True,
                )
                #for _i in range(0):
                _i=1
                _plot_collection.add_fit(
                  input_nick='nick{}'.format(_i),
                  output_nick='fit_nick{}'.format(_i),
                  formula="TMath::Exp(-0.5*((x-[1])/[0])*((x-[1])/[0]))",
                  #formula="[0]+[1]*x*x",
                  #formula="[0]*TMath::Exp(-0.5*((x-[1])/[2])*((x-[1])/[2]))",
                  initial_parameters=(1000, 1),
                  range="0,2",
                  show_info=True,
                  info_xy=(1.02, 0.55 - _i*0.06),
                  )
                
                for _p in _plot_collection._plots:
                  _p._init_basic_dict()
                  _p._basic_dict['fit_text_parameter_names'] = [None, 'Fit']
                  #_p._basic_dict['alphas'] = 0.3
                  _p._basic_dict['analysis_modules'] = ["Ratio", "FunctionPlot"]


                _plot_collection.make_plots()
