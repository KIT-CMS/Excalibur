from Excalibur.JEC_Plotter.core import FlavorFractionsFile, ETA_BIN_EDGES_WIDE, ETA_BIN_EDGES_NARROW, ETA_BIN_EDGES_BARREL, ALPHA_UPPER_BIN_EDGES
from Excalibur.JEC_Plotter.definitions.Test18.samples_18Oct2018 import (
    SAMPLES,
    SELECTION_CUTS
)


_ETA_BINNING_DICTS = dict(
    wide=dict(
        binnings=[ETA_BIN_EDGES_WIDE],
        label='wideEta'
    ),
    narrow=dict(
        binnings=[ETA_BIN_EDGES_NARROW],
        label='narrowEta',
    ),
    barrel=dict(
        binnings=[ETA_BIN_EDGES_BARREL],
        label='barrel',
    ),
    all=dict(
        binnings=[ETA_BIN_EDGES_NARROW, ETA_BIN_EDGES_WIDE, ETA_BIN_EDGES_BARREL],
        label=None,
    ),
)

if __name__ == "__main__":

    from argparse import ArgumentParser

    p = ArgumentParser(description="""
    Create a flavor fractions file.
    """)

    p.add_argument("--channels", "-c", nargs="+", default=['mm', 'ee'],
                   help="Z boson decay channel ('ee' or 'mm')")
    p.add_argument("--run-periods", "-r", nargs="+", default=['B', 'C', 'D', 'E', 'F', 'BCDEF'],
                   choices=['B', 'C', 'D', 'E', 'F', 'BCDEF'],
                   help="2017 run period ('B', 'C', 'D', 'E', 'F' or 'BCDEF')")
    p.add_argument("--eta-binning", "-e", default='all', choices=['wide', 'narrow', 'barrel', 'all'],
                   help="Eta binning ('wide', 'narrow', 'barrel', 'all')")
    args = p.parse_args()

    _JECV_MC = 'V10'
    for _ch in ('mm',): ##args.channels: #('mm', 'ee'):
        for _runperiod in ('E',): ##args.run_periods: #('B', 'C', 'D', 'E', 'F', 'BCDEF'):
            _ebd = _ETA_BINNING_DICTS[args.eta_binning]
            _eta_binning_label = _ebd['label']
            _eta_binnings = _ebd['binnings']

            if _eta_binning_label is not None:
                _basename="flavor_fractions_Test18_JEC{}_{}".format(_JECV_MC, _eta_binning_label)
            else:
                _basename="flavor_fractions_Test18_JEC{}".format(_JECV_MC)

            _c = FlavorFractionsFile(
                sample_mc=SAMPLES['MC_Z{}_DYNJ_Test18_JEC{}'.format(_ch, _JECV_MC)],
                global_selection=SELECTION_CUTS['noalphanoetacuts'],
                alpha_upper_bin_edges=ALPHA_UPPER_BIN_EDGES,
                eta_binnings=_eta_binnings,
                basename=_basename,
            )
            _c.run(require_confirmation=True)
