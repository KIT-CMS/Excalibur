from Excalibur.JEC_Plotter.core import CombinationDirect, ETA_BIN_EDGES_WIDE, ETA_BIN_EDGES_NARROW, ETA_BIN_EDGES_BARREL, ALPHA_UPPER_BIN_EDGES
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
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
    Create a combination file.
    """)

    p.add_argument("--channels", "-c", nargs="+", default=['mm', 'ee'],
                   help="Z boson decay channel ('ee' or 'mm')")
    p.add_argument("--eta-binning", "-e", default='all', choices=['wide', 'narrow', 'barrel', 'all'],
                   help="Eta binning ('wide', 'narrow', 'barrel', 'all')")
    args = p.parse_args()


    for _ch in args.channels: #('mm', 'ee'):
        _ebd = _ETA_BINNING_DICTS[args.eta_binning]
        _eta_binning_label = _ebd['label']
        _eta_binnings = _ebd['binnings']

        if _eta_binning_label is not None:
            _basename="zjet_combination_Summer16_JECV5_{}".format(_eta_binning_label)
        else:
            _basename="zjet_combination_Summer16_JECV5"

        _c = CombinationDirect(
            sample_data=SAMPLES['Data_Z{}_BCDEFGH'.format(_ch, _runperiod)],
            sample_mc=SAMPLES['MC_Z{}_DYNJ_Madgraph'.format(_ch)],
            global_selection=SELECTION_CUTS['extendedeta'],
            alpha_upper_bin_edges=ALPHA_UPPER_BIN_EDGES,
            eta_binnings=_eta_binnings,
            basename=_basename,
        )
        _c.run(require_confirmation=False)
