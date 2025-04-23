#!/usr/bin/env python
import ROOT
import os
import argparse


def merge_trees(path, tree_list):
    if not tree_list:
        return None
    chain = ROOT.TChain(tree_list[0].GetName())
    for t in tree_list:
        file = t.GetCurrentFile()
        full_path = file.GetName() + "/" + path
        print("Adding TTree: {}".format(full_path))
        chain.Add(full_path)
    # Check if there are any entries
    if chain.GetEntries() == 0:
        print("Note: Tree has 0 entries, creating empty tree with structure preserved: {}".format(path))
        # Create empty clone that preserves the structure
        return chain.CloneTree(0)
    return chain.CloneTree(-1, "fast")


def merge_histograms(hist_list):
    if not hist_list:
        return None
    hsum = hist_list[0].Clone()
    for h in hist_list[1:]:
        hsum.Add(h)
    return hsum


def collect_objects(root_file, path="", obj_dict=None):
    print("Collecting objects from path: {}".format(path))
    if obj_dict is None:
        obj_dict = {}

    dir = root_file.GetDirectory(path) if path else root_file

    for key in dir.GetListOfKeys():
        name = key.GetName()
        obj = dir.Get(name).Clone()
        full_path = os.path.join(path, name)
        if isinstance(obj, ROOT.TDirectory):
            collect_objects(root_file, full_path, obj_dict)
        else:
            obj_dict.setdefault(full_path, []).append(obj)
    return obj_dict


def mkdir_recursive(output_file, path):
    parts = path.strip("/").split("/")
    current_dir = output_file
    for part in parts[:-1]:  # Don't create the object name as a directory
        if not current_dir.GetDirectory(part):
            current_dir.mkdir(part)
        current_dir = current_dir.GetDirectory(part)
    return current_dir


def hadd_recursive(output_filename, input_filenames):
    merged_objects = {}
    open_files = []  # Keep references to open files to prevent closure

    for fname in input_filenames:
        f = ROOT.TFile.Open(fname)
        if not f or f.IsZombie():
            raise IOError("Could not open {}".format(fname))
        open_files.append(f)
        objects = collect_objects(f)
        for path, objs in objects.items():
            merged_objects.setdefault(path, []).extend(objs)

    output = ROOT.TFile.Open(output_filename, "RECREATE")

    for path, obj_list in merged_objects.items():
        example_obj = obj_list[0]
        out_dir = mkdir_recursive(output, path)
        output.cd()
        out_dir.cd()

        merged_obj = None
        if isinstance(example_obj, ROOT.TTree):
            print("Merging tree at {}".format(path))
            merged_obj = merge_trees(path, obj_list)
        elif isinstance(example_obj, ROOT.TH1):
            print("Merging histogram at {}".format(path))
            merged_obj = merge_histograms(obj_list)
        else:
            print("Skipping unsupported object type at {} with type {}"
                  .format(path, type(example_obj)))
            continue

        if merged_obj:
            merged_obj.Write()

    output.Close()
    print("Done. Output written to {}".format(output_filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("TARGET", help="output root file", type=str)
    parser.add_argument("INPUT", help="Input root files or XRootD path e.g. root://cmsdcache-kit-disk.gridka.de//store/user/myuser/*.root", type=str, nargs='+')
    args = parser.parse_args()
    output_file = args.TARGET
    input_files = args.INPUT
    print("Merging {} files into: {}".format(len(input_files), output_file))
    hadd_recursive(output_file, input_files)
