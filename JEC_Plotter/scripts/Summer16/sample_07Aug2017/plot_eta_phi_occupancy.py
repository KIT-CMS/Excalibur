from Excalibur.JEC_Plotter.core import PlotHistograms2D, CutSet, BinSpec, QUANTITIES
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
    RUN_PERIOD_CUT_DICTS,
)

from copy import deepcopy

QUANTITIES['jet1eta_zoom'] = deepcopy(QUANTITIES['jet1eta'])
QUANTITIES['jet1eta_zoom'].name = "jet1eta_zoom"
QUANTITIES['jet1eta_zoom'].bin_spec = BinSpec.make_equidistant(n_bins=50, range=(-4.0, -1.5))

QUANTITIES['jet1phi_zoom'] = deepcopy(QUANTITIES['jet1phi'])
QUANTITIES['jet1phi_zoom'].name = "jet1phi_zoom"
QUANTITIES['jet1phi_zoom'].bin_spec = BinSpec.make_equidistant(n_bins=50, range=(2.0, 2.7))

QUANTITIES['jet2eta_zoom'] = deepcopy(QUANTITIES['jet2eta'])
QUANTITIES['jet2eta_zoom'].name = "jet2eta_zoom"
QUANTITIES['jet2eta_zoom'].bin_spec = BinSpec.make_equidistant(n_bins=50, range=(-4.0, -1.5))

QUANTITIES['jet2phi_zoom'] = deepcopy(QUANTITIES['jet2phi'])
QUANTITIES['jet2phi_zoom'].name = "jet2phi_zoom"
QUANTITIES['jet2phi_zoom'].bin_spec = BinSpec.make_equidistant(n_bins=50, range=(2.0, 2.7))

QUANTITIES['jet3eta_zoom'] = deepcopy(QUANTITIES['jet3eta'])
QUANTITIES['jet3eta_zoom'].name = "jet3eta_zoom"
QUANTITIES['jet3eta_zoom'].bin_spec = BinSpec.make_equidistant(n_bins=50, range=(-4.0, -1.5))

QUANTITIES['jet3phi_zoom'] = deepcopy(QUANTITIES['jet3phi'])
QUANTITIES['jet3phi_zoom'].name = "jet3phi_zoom"
QUANTITIES['jet3phi_zoom'].bin_spec = BinSpec.make_equidistant(n_bins=50, range=(2.0, 2.7))

_CORR_FOLDER = "L1L2L3"

_QUANTITY_PAIRS = [
    ('jet1phi', 'jet1eta'),
    ('jet2phi', 'jet2eta'),
    ('jet3phi', 'jet3eta'),
    ('zphi', 'zeta'),
    # -- zoomed in plots
    ('jet1phi_zoom', 'jet1eta_zoom'),
    ('jet2phi_zoom', 'jet2eta_zoom'),
    ('jet3phi_zoom', 'jet3eta_zoom'),
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
    SELECTION_CUTS['basiccuts'],
    SELECTION_CUTS['nocuts']
]

def _workflow(sample, jecv):
    _phs = []
    for _run_period_cut_name, _run_period_cut in ADDITIONAL_CUTS['run_periods'].iteritems():

        _ph = PlotHistograms2D(
            basename="eta_phi_occupancy_2D_07Aug2017_{}".format(_run_period_cut_name),
            # there is one subplot per sample and cut in each plot
            sample=sample,
            jec_correction_string=_CORR_FOLDER,
            # each quantity cut generates a different plot
            quantity_pairs=_QUANTITY_PAIRS,
            # each selection cut generates a new plot
            selection_cuts=[_sel_cut + _run_period_cut for _sel_cut in _SELECTION_CUTS],
            # show_ratio_to_first=True
            plot_label="Summer16 JEC {}".format(jecv)
        )

        _phs.append(_ph)

    for _ph in _phs:
        _ph.make_plots()

if __name__ == "__main__":
    for _jecv in ("V6",):
        for _channel in ("mm", "ee"):
            _workflow(sample=SAMPLES['Data_Z{}_BCDEFGH_Summer16_JEC{}'.format(_channel, _jecv)], jecv=_jecv)

