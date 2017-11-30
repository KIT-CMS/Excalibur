from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D, CutSet
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
)
from Excalibur.JEC_Plotter.utilities.plot import plot_time_dependence

from copy import deepcopy

_SAMPLE_NAME = "07Aug2017"

_CORR_FOLDER = "L1L2L3"

_QUANTITIES = [
    'mpf', 'ptbalance',
    'npv',
    'zpt', 'zphi', 'zmass',
    'jet1pt', 'jet2pt', 'jet3pt',
    'jet1phi', 'jet2phi', 'jet3phi',
    'jet1pt_over_jet1ptraw'
]

_TIME_QUANTITY = 'run'

_cut_final_no_alpha = CutSet("basicToNoAlpha",
    weights=[
        "abs(jet1eta)<1.3",
        "zpt>30",
    ],
    labels=[
        r"$|\\eta^\\mathrm{Jet1}|<1.3$",
        r"$p_\\mathrm{T}^\\mathrm{Z}>30~GeV$",
    ]
)

_SELECTION_CUTS = [
    SELECTION_CUTS['basiccuts'] + ADDITIONAL_CUTS['user']['basicToFinal'],
    SELECTION_CUTS['basiccuts'] + _cut_final_no_alpha
]

_ADDITIONAL_CUTS = [
    {
        'cut': ADDITIONAL_CUTS['run_periods']['runB'],
        'label': r"RunB",
        'color': 'pink'
    },
    {
        'cut': ADDITIONAL_CUTS['run_periods']['runC'],
        'label': r"RunC",
        'color': 'red'
    },
    {
        'cut': ADDITIONAL_CUTS['run_periods']['runD'],
        'label': r"RunD",
        'color': 'darkred'
    },
    {
        'cut': ADDITIONAL_CUTS['run_periods']['runE'],
        'label': r"RunE",
        'color': 'blue'
    },
    {
        'cut': ADDITIONAL_CUTS['run_periods']['runF'],
        'label': r"RunF",
        'color': 'cyan'
    },
    {
        'cut': ADDITIONAL_CUTS['run_periods']['runG'],
        'label': r"RunG",
        'color': 'green'
    },
    {
        'cut': ADDITIONAL_CUTS['run_periods']['runH'],
        'label': r"RunH",
        'color': 'orange'
    }
]

if __name__ == "__main__":
    #for _corr_folder in ["L1L2L3", "L1L2L3Res"]:
    for _corr_folder in ["L1L2L3"]:
        plot_time_dependence(sample=SAMPLES['Data_Zmm_BCDEFGH'],
                             corrections_folder=_corr_folder,
                             quantities=_QUANTITIES,
                             selection_cuts=_SELECTION_CUTS,
                             additional_cuts=_ADDITIONAL_CUTS,
                             www_folder_label="{}".format(_SAMPLE_NAME),
                             time_quantity=_TIME_QUANTITY)
        
        plot_time_dependence(sample=SAMPLES['Data_Zee_BCDEFGH'],
                             corrections_folder=_corr_folder,
                             quantities=_QUANTITIES,
                             selection_cuts=_SELECTION_CUTS,
                             additional_cuts=_ADDITIONAL_CUTS,
                             www_folder_label="{}".format(_SAMPLE_NAME),
                             time_quantity=_TIME_QUANTITY)
