from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D, CutSet, QUANTITIES
from Excalibur.JEC_Plotter.definitions.Test18.samples_18Oct2018 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
)

from copy import deepcopy

_CORR_FOLDER = "L1L2L3"

_QUANTITY_PAIRS = [
    ('jet1phi', 'jet1eta_narrow'),
    ('jet1phi', 'jet1eta'),
    ('jet2phi', 'jet2eta'),
    ('jet3phi', 'jet3eta'),
    #('jet2phi', 'jet2eta_narrow'),
    #('jet3phi', 'jet3eta_narrow'),
    #('zphi', 'zeta'),
    #('metphi', 'met'),
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
    #SELECTION_CUTS['finalcuts'],
    #SELECTION_CUTS['basiccuts'] + _cut_final_no_eta,
    SELECTION_CUTS['basiccuts'],
    #SELECTION_CUTS['nocuts']
]

def _workflow(sample):
    _phs = []
    for _run_period_cut_name, _run_period_cut in ADDITIONAL_CUTS['run_periods'].iteritems():

        _ph = PlotHistograms2D(
            basename="eta_phi_occupancy_2D_18Oct2018_{}".format(_run_period_cut_name),
            # there is one subplot per sample and cut in each plot
            sample=sample,
            jec_correction_string=_CORR_FOLDER,
            # each quantity cut generates a different plot
            quantity_pairs=_QUANTITY_PAIRS,
            # each selection cut generates a new plot
            selection_cuts=[_sel_cut + _run_period_cut for _sel_cut in _SELECTION_CUTS],
            # show_ratio_to_first=True
        )

        _phs.append(_ph)

    for _ph in _phs:
        _ph.make_plots()

if __name__ == "__main__":
    for _jecv in ('V10',):
        for _channel in ('mm',):
            for _run_period in ('E',):
                #_workflow(SAMPLES['Data_Z{}_{}_Fall17_JEC{}'.format(_channel, _jecv)])
                _ph = PlotHistograms2D(
                    basename="eta_phi_occupancy_2D_18Oct2018_JEC{}_run{}".format(_jecv, _run_period),
                    # there is one subplot per sample and cut in each plot
                    sample=SAMPLES['Data_Z{}_{}_Test18_JEC{}'.format(_channel, _run_period, _jecv)],
                    jec_correction_string=_CORR_FOLDER,
                    # each quantity cut generates a different plot
                    quantity_pairs=_QUANTITY_PAIRS,
                    # each selection cut generates a new plot
                    #selection_cuts=[_sel_cut + _run_period_cut for _sel_cut in _SELECTION_CUTS],
                    selection_cuts=_SELECTION_CUTS,
                    # show_ratio_to_first=True
                    plot_label="Run2018{} (JEC {})".format(_run_period, _jecv)
                )
                _ph.make_plots()
