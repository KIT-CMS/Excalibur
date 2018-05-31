from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D, CutSet, Sample
from Excalibur.JEC_Plotter.definitions.Fall17.samples_17Nov2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
)
from Excalibur.JEC_Plotter.utilities.plot import plot_flavors, plot_flavor_fractions

from copy import deepcopy

_CORR_FOLDER = "L1L2L3"

_QUANTITIES = [
    'zpt_log',
    'jet1pt', 'jet1eta', 'jet1phi',
    'mpf', 'ptbalance', 'alpha',
    'npv', 'rho', 'jet1res'
]

_QUANTITY_PAIRS = [
    ('zpt_log', 'jet1pt_over_jet1ptraw'),
    ('zpt_log', 'mpf'),
    ('zpt_log', 'ptbalance'),
    ('zpt_log', 'jet1pt_log'),
    ('alpha', 'ptbalance'),
    ('alpha', 'mpf'),
]

_SAMPLES = [
    SAMPLES["MC_Zmm_DYNJ_Fall17_JECV4"],
]

_SELECTION_CUTS = [
    SELECTION_CUTS['finalcuts'],
    #SELECTION_CUTS['nocuts'],
]

if __name__ == "__main__":
    for _sample in _SAMPLES:
        # plot_flavors(
        #     sample=_sample,
        #     corrections_folder=_CORR_FOLDER,
        #     quantities_or_quantity_pairs=_QUANTITIES +_QUANTITY_PAIRS,
        #     selection_cuts=_SELECTION_CUTS,
        #     www_folder_label="{}".format(_sample['source_label']),
        #     flavors_to_include=('ud', 's', 'c', 'b', 'g', 'undef'),
        #     flavor_definition='miniAOD',
        # )
        _pc = plot_flavor_fractions(
            sample=_sample,
            jec_correction_string=_CORR_FOLDER,
            quantities=_QUANTITIES,
            selection_cuts=_SELECTION_CUTS,
            www_folder_label="{}".format(_sample['source_label']),
            flavors_to_include=('ud', 's', 'c', 'b', 'g', 'undef'),
            flavor_definition='miniAOD',
        )

        _pc.make_plots()
