from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D, CutSet, QUANTITIES, BinSpec
from Excalibur.JEC_Plotter.definitions.Fall17.samples_17Nov2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
)
from Excalibur.JEC_Plotter.utilities.plot import plot_time_dependence

from copy import deepcopy

_SAMPLE_NAME = "17Nov2017"

_CORR_FOLDER = "L1L2L3"

_QUANTITIES = [
    'mpf', 'ptbalance',
    'npv', 'rho',
    'met'
    'zpt', 'zphi', 'zmass',
    'jet1pt', 'jet2pt', 'jet3pt',
    'jet1phi', 'jet2phi', 'jet3phi',
    'jet1pt_over_jet1ptraw'
]

# redefine binning and plot range to values more meaningful for profiles
QUANTITIES['mpf'].bin_spec = BinSpec.make_equidistant(n_bins=50, range=(0.8, 1.2))
QUANTITIES['ptbalance'].bin_spec = BinSpec.make_equidistant(n_bins=50, range=(0.7, 1.2))
QUANTITIES['jet1pt'].bin_spec = BinSpec.make_equidistant(n_bins=50, range=(50., 150.))
QUANTITIES['jet2pt'].bin_spec = BinSpec.make_equidistant(n_bins=50, range=(10., 40.))
QUANTITIES['jet3pt'].bin_spec = BinSpec.make_equidistant(n_bins=50, range=(10., 25.))
QUANTITIES['npv'].bin_spec = BinSpec.make_equidistant(n_bins=50, range=(10, 70))
QUANTITIES['zmass'].bin_spec = BinSpec.make_equidistant(n_bins=50, range=(90., 95.))
QUANTITIES['zpt'].bin_spec = BinSpec.make_equidistant(n_bins=50, range=(50., 200.))

_TIME_QUANTITY = 'run2017'

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
    SELECTION_CUTS['finalcuts']
    #SELECTION_CUTS['basiccuts'] + ADDITIONAL_CUTS['user']['basicToFinal'],
    #SELECTION_CUTS['basiccuts'] + _cut_final_no_alpha
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
#    {
#        'cut': ADDITIONAL_CUTS['run_periods']['runG'],
#        'label': r"RunG",
#        'color': 'green'
#    },
#    {
#        'cut': ADDITIONAL_CUTS['run_periods']['runH'],
#        'label': r"RunH",
#        'color': 'orange'
#    }
]

if __name__ == "__main__":
    for _corr_folder in ["L1L2L3"]:
        plot_time_dependence(sample=SAMPLES['Data_Zmm_BCDEF_Fall17_V3'],
                             corrections_folder=_corr_folder,
                             quantities=_QUANTITIES,
                             selection_cuts=_SELECTION_CUTS,
                             additional_cuts=_ADDITIONAL_CUTS,
                             www_folder_label="{}".format(_SAMPLE_NAME),
                             time_quantity=_TIME_QUANTITY)

        plot_time_dependence(sample=SAMPLES['Data_Zee_BCDEF_Fall17_V3'],
                             corrections_folder=_corr_folder,
                             quantities=_QUANTITIES,
                             selection_cuts=_SELECTION_CUTS,
                             additional_cuts=_ADDITIONAL_CUTS,
                             www_folder_label="{}".format(_SAMPLE_NAME),
                             time_quantity=_TIME_QUANTITY)
