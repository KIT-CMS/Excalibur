#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ROOT
import pandas as pd

from argparse import ArgumentParser
from collections import OrderedDict

if __name__ == "__main__":

    p = ArgumentParser(description="""
    Count events in Excalibur output.
""")

    p.add_argument("--input-file", "-i",
                   help="Excalibur output ROOT file")
    p.add_argument("--folders", "-f", nargs='+', default=None,
                   help="folders for which events should be counted (default: all)")
    p.add_argument("--cuts", "-c", nargs='+', default=None,
                   help="cuts to apply before counting events (default: no cuts)")
    
    args = p.parse_args()

    _file = ROOT.TFile(args.input_file)
    _root_folders = args.folders
    _cuts = args.cuts


    # -- begin main method

    # -- define column headers (cuts)
    _fields = ["folder", "no cuts"]
    if _cuts is not None:
        _fields += _cuts  # add cuts as fields

    # -- define row headers (folders)
    _results = OrderedDict(folder=[], no_cuts=[])
    if args.cuts is not None:
        for _cut in args.cuts:
            _results[_cut] = []

    _all_folders = _file.GetListOfKeys()
    for _ifolder, _ in enumerate(_all_folders):
        _folder_name = _all_folders[_ifolder].GetName()
        _ntuple = _file.Get("{}/ntuple".format(_folder_name))
        if _root_folders is None or (_root_folders is not None and _folder_name in _root_folders):
            if isinstance(_ntuple, ROOT.TTree):
                _results['folder'].append(_folder_name)


    for _folder_name in _results['folder']:
        _ntuple = _file.Get("{}/ntuple".format(_folder_name))
        _results['no_cuts'].append(_ntuple.GetEntries())
        if args.cuts is not None:
            for _cut in args.cuts:
                _n_after_cuts = _ntuple.Draw(">>elist", _cut, "goff")
                _results[_cut].append(_n_after_cuts)

    # -- make pandas DataFrame
    _results_frame = pd.DataFrame(data=_results)
    _results_frame = _results_frame.set_index(['folder'])

    print _results_frame
