from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotProfiles, QUANTITIES, BinSpec, CutSet, Quantity
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
    RUN_PERIOD_CUT_DICTS,
)

from copy import deepcopy

_CORR_FOLDER = "L1L2L3"

QUANTITIES["npumean"].bin_spec = BinSpec.make_from_bin_edges(range(0, 64, 4))
QUANTITIES["delta_zpt_jet1pt"] = Quantity(
    name="delta_zpt_jet1pt",
    expression="zpt-jet1pt",
    label=r"$p_{T}^{Z} - p_{T}^{Jet1}$",
    bin_spec=BinSpec.make_equidistant(n_bins=50, range=(0, 65))
)


_QUANTITY_PU = 'npumean'
_QUANTITIES = [
    'delta_zpt_jet1pt',
    #'jet1pt', 'jet2pt', 'jet3pt', 'zpt',
    #'alpha', 'mpf', 'ptbalance'
]
_QUANTITY_PAIRS = [(_QUANTITY_PU, _q) for _q in _QUANTITIES]

_cut_final_no_eta = CutSet("basicToBarrel",
    weights=[
        "abs(jet1eta)<1.3",
    ],
    labels=[
        r"$|\\eta^{Jet1}|<1.3$",
    ]
)

_SELECTION_CUTS = [
    SELECTION_CUTS['finalcuts'],
    SELECTION_CUTS['basiccuts'] + _cut_final_no_eta,
]

_z_cut_colors = [
    "k",
    "red",
    "blue",
    "green",
    "violet",
    "orange",
    "cyan",
    "magenta",
    "yellow",
    "brown",
    "olive",
    "lightsteelblue",
]

_ADDITIONAL_CUTS_ZPT = [
    {
        'cut': CutSet(
            '{:0>2d}_{}'.format(_i_z_cut, _z_cut.name),  # for sorting,
            weights=_z_cut.weights_list, labels=[]
        ),
        #'label': r"${} < p_\\mathrm{T}^\\mathrm{Z} / GeV \\leq {}$".format(_z_cut.range[0], _z_cut.range[1]),
        'label': _z_cut.texts[0],
        'color': _z_cut_colors[_i_z_cut]
    }
    for _i_z_cut, _z_cut in enumerate(QUANTITIES['zpt'].make_cutsets_from_binspec(BinSpec.make_from_bin_edges([30, 50, 85, 105, 130, 250, 1500])))
]

def _workflow(sample_mc, jecv):
    _phs = []

    _zpt_cuts = [_ac['cut'] for _ac in _ADDITIONAL_CUTS_ZPT]
    #_era_cuts = [_ac['cut'] for _ac in RUN_PERIOD_CUT_DICTS]
    #_era_cuts.insert(0, None)

    _SAMPLES_ZPT_MC = []
    for _ac in _ADDITIONAL_CUTS_ZPT:
        _SAMPLES_ZPT_MC.append(deepcopy(sample_mc))
        _SAMPLES_ZPT_MC[-1]['color'] = _ac['color']
        _SAMPLES_ZPT_MC[-1]['source_label'] = '{}'.format(_ac['label'])

    for _corr_level in ('', 'L1', 'L1L2L3'):
        _ph = PlotProfiles(
                basename="pileup_mc_zptseries_07Aug2017_JEC{}".format(jecv),
                # there is one subplot per sample and cut in each plot
                samples=_SAMPLES_ZPT_MC,
                jec_correction_string=_corr_level,
                additional_cuts=_zpt_cuts,
                # each quantity cut generates a different plot
                quantity_pairs=_QUANTITY_PAIRS,
                # each selection cut generates a new plot
                selection_cuts=_SELECTION_CUTS,
                show_ratio_to_first=False,
                show_cut_info_text=True,
                plot_label="Summer16 JEC {}".format(jecv),
                legend_position="upper left",
                cut_info_text_topleft_xy=(0.73, 1.08),
        )
        _phs.append(_ph)

        for _ph in _phs:
           for _i in range(6):
               _ph.add_fit(
                   input_nick='nick{}'.format(_i),
                   output_nick='fit_nick{}'.format(_i),
                   formula="[0]+[1]*x",
                   initial_parameters=(1, 1),
                   range="10,50",
                   show_info=True,
                   info_xy=(1.02, 0.55 - _i*0.06),
               )
           for _p in _ph._plots:
               _p._init_basic_dict()
               _p._basic_dict['fit_text_parameter_names'] = [None, 'slope']
               _p._basic_dict['alphas'] = 0.3
           _ph.make_plots()

if __name__ == "__main__":
    for _jecv in ("V6",):
        for _channel in ("mm", "ee"):
            _workflow(
                sample_mc=SAMPLES['MC_Z{}_DYNJ_Summer16_JEC{}'.format(_channel, _jecv)],
                jecv=_jecv)
