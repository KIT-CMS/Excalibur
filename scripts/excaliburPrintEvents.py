#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ROOT

import numpy as np
import os
import pandas as pd

from argparse import ArgumentParser
from array import array as arr
from collections import OrderedDict

DEFAULT_FIELD_DATA_TYPE = 'f'
FIELD_DATA_TYPE_MAP = {'run': 'i', 'lumi': 'i', 'event': 'l'}

if __name__ == "__main__":

    p = ArgumentParser(description="""
    Print event data stored in Excalibur output files (flat ROOT TTrees) as a plain text table.
    (Similar to TTree::Scan(), but more flexible)

    Note: this script needs pandas to work.
""")

    p.add_argument("--input-file", "-i", required=True,
                   help="Excalibur output ROOT file")
    p.add_argument("--output-file", "-o", default=None,
                   help="File to which to write the event data. Can be omitted, in which case "
                        "the (possibly truncated) DataFrame will only be written to stdout.")
    p.add_argument("--overwrite", action="store_true", default=False,
                   help="Overwrite the output file if it exists (default: False)")
    p.add_argument("--folders", "-F", nargs='+', default=None,
                   help="folders containing the TTree for which events should be printed "
                        "(default: all). Note that the TTree itself must be called 'ntuple'")
    p.add_argument("--cuts", "-c", nargs='+', default=None,
                   help="cuts to apply before printing events (default: no cuts)")
    p.add_argument("--number", "-n", default=None,
                   help="Number of events to print (per folder).")
    p.add_argument("--fields", "-f", nargs='+', required=False,
                   help="Fields (ntuple branches) to print for each event. "
                        "(Apart from 'run', 'lumi' and 'event', which are always written out.")
    p.add_argument("--compact", action="store_true", default=False,
                   help="Interpret 'run:lumi:event' as a structured index, and omit these "
                        "fields for rows where they appear in consecutive repetition (default: False)")
    p.add_argument("--random", action="store_true", default=False,
                   help="Pick random events (default: False).")
    p.add_argument("--random-seed", required=False, default=None,
                   help="Set the seed of the random number generator (same seed across runs "
                        "will ensure identical choice of events). If not given, a new seed is "
                        "determined for each run.")
    
    args = p.parse_args()

    # input file
    _file = ROOT.TFile(args.input_file)

    # output file (if given, otherwise None)
    _output_file = args.output_file
    if _output_file is not None and os.path.exists(_output_file) and not args.overwrite:
        print "[ERROR] Specified output file '{}' already exists: will not overwrite".format(_output_file,)
        exit(1)

    # folders in ROOT file containing TTrees called 'ntuple' 
    _root_folders = args.folders

    # selection cuts to apply
    _cuts = args.cuts
    if _cuts is not None:
        _cut_string = "&&".join(['({})'.format(_cut) for _cut in args.cuts])
    else:
        _cut_string = "1.0"

    # no. of events to read out
    _n_events = None
    if args.number is not None:
        _n_events = int(args.number)

    # fields to read out
    _fields = args.fields

    # set the random seed
    if args.random_seed:
        np.random.seed(int(args.random_seed))

    # -- begin main method

    # -- define column headers (cuts)
    _fields = ["run", "lumi", "event"] + _fields
    _field_string = ":".join(_fields)

    # -- reserve memory for TTree readout
    _field_readout_vars = dict()
    ##_field_arrays_for_df = OrderedDict(folder=[], ntuple_idx=[])
    _field_arrays_for_df = OrderedDict(folder=[])
    for _f in _fields:
        _field_data_type = FIELD_DATA_TYPE_MAP.get(_f, DEFAULT_FIELD_DATA_TYPE)
        _field_readout_vars[_f] = arr(_field_data_type, [0])
        _field_arrays_for_df[_f] = []

    # -- obtain folder names
    _folder_ntuple_pairs = []
    _all_folders = _file.GetListOfKeys()
    for _ifolder, _ in enumerate(_all_folders):
        _folder_name = _all_folders[_ifolder].GetName()
        _ntuple = _file.Get("{}/ntuple".format(_folder_name))
        if _root_folders is None or (_root_folders is not None and _folder_name in _root_folders):
            if isinstance(_ntuple, ROOT.TTree):
                _folder_ntuple_pairs.append(
                    dict(
                        folder=_folder_name,
                        ntuple=_ntuple,
                    )
                )
                print "Added folder: {}".format(_folder_name)

    # -- go through the folder-ntuple pairs
    ROOT.gROOT.cd()  # change to in-memory scope (outside read-only input file)
    for _i_fnp, _fnp in enumerate(_folder_ntuple_pairs):
        _folder_name = _fnp['folder']
        _ntuple = _fnp['ntuple']

        # apply the cuts
        _filtered_ntuple = _ntuple.CopyTree(_cut_string)
        
        # determine the row indices
        _max_rows = _filtered_ntuple.GetEntries()
        if _n_events is not None:
            if args.random and _n_events < _max_rows:
                # note: sorting doesn't help because TTree::CopyTree() destroys the ordering (?)
                _entry_list = np.sort(np.random.choice(range(_max_rows), _n_events, replace=False))
            else:
                _entry_list = range(min(_max_rows, _n_events))

        # wire the readout variables
        for _field_name, _field_readout_var in _field_readout_vars.iteritems():
            _filtered_ntuple.SetBranchAddress(_field_name, _field_readout_var)

        # populate the lists that will be used for filling the DataFrame
        for _i_row in _entry_list:
            _filtered_ntuple.GetEntry(_i_row)
            for _field in _fields:
                _field_arrays_for_df[_field].append(_field_readout_vars[_field][0])
            _field_arrays_for_df['folder'].append(_folder_name)
            ##_field_arrays_for_df['ntuple_idx'].append(_i_fnp)

    # -- make pandas DataFrame
    _results_frame = pd.DataFrame(data=_field_arrays_for_df)
    ##_index_fields = ['folder', 'ntuple_idx']
    _index_fields = ['folder']
    if args.compact:
        _index_fields += ['run', 'lumi', 'event']
    _results_frame = _results_frame.set_index(_index_fields)

    # -- write to file
    if _output_file is not None:
        with open(_output_file, "w") as _f:
            _results_frame.to_string(_f)
            _f.write('\n')

    # -- show on stdout
    print _results_frame
