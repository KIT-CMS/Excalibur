#!/usr/bin/env python
import ROOT
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description="Merge ROOT folders from multiple input files into one output file.")
    parser.add_argument("output", help="Output ROOT file")
    parser.add_argument("inputs", nargs='+', help="Input ROOT files")
    args = parser.parse_args()

    output_filename = args.output
    input_files = args.inputs

    output = ROOT.TFile(output_filename, "RECREATE")
    if not output or output.IsZombie():
        raise RuntimeError("Error: could not create output file '{}'".format(output_filename))

    for filename in input_files:
        if not os.path.exists(filename):
            raise IOError("File '{}' does not exist".format(filename))

        infile = ROOT.TFile.Open(filename)
        if not infile or infile.IsZombie():
            raise RuntimeError("Could not open '{}'".format(filename))

        keys = infile.GetListOfKeys()
        if keys.GetSize() == 0:
            raise RuntimeError("No keys found in '{}'".format(filename))

        for i in range(keys.GetSize()):
            top_key = keys.At(i)
            name = top_key.GetName()
            obj = infile.Get(name)

            output.cd()

            if obj.InheritsFrom("TDirectory"):
                print("Merging directory '{}' from file '{}'".format(name, filename))
                if output.GetDirectory(name):
                    raise RuntimeError("Directory '{}' already exists in output file".format(name))

                out_dir = output.mkdir(name)
                out_dir.cd()

                for key in obj.GetListOfKeys():
                    sub_obj = key.ReadObj()
                    sub_name = key.GetName()
                    sub_obj.Write(sub_name)
            else:
                print("Copying top-level object '{}' from file '{}'".format(name, filename))
                obj.Write(name)

        infile.Close()

    output.Close()
    print("Successfully created '{}'".format(output_filename))


if __name__ == "__main__":
    main()
