#!/usr/bin/env python
import subprocess
import sys
import argparse

try:
    from xrootdglob import glob
except ImportError:
    print("Importing xrootd failed. Can't access files via xrootd.")
    from glob import glob


def merge(target, filelist, overwrite):
    command = ['hadd']
    if overwrite:
        command += ['-f']
    try:
        subprocess.check_call(command + [target] + filelist)
    except subprocess.CalledProcessError:                                       
        print "hadd failed!"                                        
        sys.exit(1) 
 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("TARGET", help="Output root file", type=str)
    parser.add_argument("INPUT", help="Input root files or XRootD path e.g. root://cmsxrootd-kit.gridka.de//store/user/myuser/*.root", type=str, nargs='+')
    parser.add_argument('-f', '--overwrite', help="overwrite an existing output file", action='store_true')
    
    args = parser.parse_args()
    
    target = args.TARGET
    input_paths = args.INPUT
    filelist = []
    for path in input_paths:
        filelist += glob(path)
    merge(target, filelist, args.overwrite)

