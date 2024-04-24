#!/usr/bin/env python
"""
Based on https://root.cern.ch/doc/master/hadd_8C_source.html
Instead of adding TTrees to the TChain and merging it, add the files,
so that we only create a proxy file.
The original files need to be kept at the same path for this to work.
"""

import ROOT
import argparse

try:
    from xrootdglob import glob
except ImportError:
    print("Importing xrootd failed. Can't access files via xrootd.")
    from glob import glob


def MergeRootFiles(target, sourcefiles, check=False):
    path = target.GetPath().split(':')[-1]
    path = path[1:]

    first_source = ROOT.TFile.Open(sourcefiles[0], "READ")
    first_source.cd(path)
    current_sourcedir = ROOT.gDirectory
    # gain time, do not add the objects in the list in memory
    status = ROOT.TH1.AddDirectoryStatus()
    ROOT.TH1.AddDirectory(ROOT.kFALSE)
    keys = current_sourcedir.GetListOfKeys()

    for key in keys:
        # read object from first source file
        first_source.cd(path)
        obj = key.ReadObj()

        if isinstance(obj, ROOT.TObjString):
            for fname in sourcefiles:
                f = ROOT.TFile.Open(fname, "READ")
                if not f:
                    raise IOError('[ERROR] Failed to open file: {}'.format(fname))
                f.cd(path)
                key2 = ROOT.gDirectory.GetListOfKeys().FindObject(key.GetName())
                string = key2.ReadObj().Clone()
                f.Close()
                target.cd()
                string.Write(key.GetName())

        elif isinstance(obj, ROOT.TH1):
            # descendant of TH1 -> merge it
            print("[INFO] Merging histogram {}/{}".format(path, obj.GetName()))
            h1 = obj.Clone()
            # loop over all source files and add the content of the
            # corresponding histogram to the one pointed to by "h1"
            for fname in sourcefiles[1:]:
                f = ROOT.TFile.Open(fname, "READ")
                if not f:
                    raise IOError('[ERROR] Failed to open file: {}'.format(fname))
                # make sure we are at the correct directory level by cd'ing to path
                f.cd(path)
                key2 = ROOT.gDirectory.GetListOfKeys().FindObject(h1.GetName())
                if key2:
                    h2 = key.ReadObj()
                    h1.Add(h2)
                    del h2
                f.Close()
            target.cd()
            h1.Write(key.GetName())

        elif isinstance(obj, ROOT.TTree):
            tree_name = obj.GetName()
            tchain = ROOT.TChain(tree_name)
            full_tree_path = "{}/{}".format(path, tree_name)
            print("[INFO] Linking trees in {} files under '{}'...".format(len(sourcefiles), full_tree_path))
            for fname in sourcefiles:
                if not tchain.AddFile(fname, ROOT.TTree.kMaxEntries, full_tree_path):
                    raise RuntimeError('[ERROR] Could not connect tree {} in file {} to TChain!'.format(full_tree_path, fname))
                # test the links
                if check:
                    num_entries = tchain.GetEntries()
                    print("[INFO] Linking successful. Combined TChain yielded {} entries.".format(num_entries))
            target.cd()
            tchain.Write()

        elif isinstance(obj, ROOT.TDirectory):
            # it's a subdirectory
            print("[INFO] Found subdirectory " + obj.GetName())
            # create a new subdir of same name and title in the target file
            target.cd()
            newdir = target.mkdir(obj.GetName(), obj.GetTitle())
            # newdir is now the starting point of another round of merging
            # newdir still knows its depth within the target file via
            # GetPath(), so we can still figure out where we are in the recursion
            MergeRootFiles(newdir, sourcefiles, check=check)
        else:
            print("[WARNING] Unknown object type, name: " + obj.GetName() + " title: " + obj.GetTitle())
    target.SaveSelf(ROOT.kTRUE)
    ROOT.TH1.AddDirectory(status)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("TARGET", help="output root file", type=str)
    parser.add_argument("INPUT", help="Input root files or XRootD path e.g. root://cmsdcache-kit-disk.gridka.de//store/user/myuser/*.root", type=str, nargs='+')

    parser.add_argument('-c', '--check', help="check that the linking was successful by calling GetEntries on the resulting TChain", action='store_true')
    parser.add_argument('-f', '--overwrite', help="overwrite an existing output file", action='store_true')

    args = parser.parse_args()
    output_file = args.TARGET
    input_paths = args.INPUT
    filelist = []
    for path in input_paths:
        filelist += glob(path)
    print("pseudo_hadd Target file: {}".format(output_file))
    for i, filename in enumerate(filelist):
        print("pseudo_hadd Source file {}: {}".format(i, filename))

    mode = "RECREATE" if args.overwrite else "NEW"
    target = ROOT.TFile.Open(output_file, mode)
    if not target:
        raise IOError("Target file '{}' already exists!".format(output_file))
    MergeRootFiles(target, filelist, args.check)
    target.Close()
