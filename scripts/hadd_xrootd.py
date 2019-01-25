#!/usr/bin/env python
import subprocess
import sys
import argparse


def convert_srm_to_xrootd_path(path):
    sites = { "srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/": "root://cmsxrootd-redirectors.gridka.de//"}
    for site in sites.keys():
        if path.find(site) is 0:
            return sites[site]+path[len(site):]
    return path


def get_filelist(xrootd_path):
    print("Use pyxrootd tools")
    print("xrootd path: %s" % xrootd_path)
    gridpath = xrootd_path.replace("*.root", "")
        
    gridserver = 'root://' + gridpath.split("//")[1]
    gridpath = '/' + gridpath.split("//")[2]
    gridpath = gridpath.replace('\n', '')
    print("server: %s"% gridserver)
    print("path: %s"% gridpath)
    from XRootD import client
    from XRootD.client.flags import DirListFlags, OpenFlags, MkDirFlags, QueryCode
    myclient = client.FileSystem(gridserver)
    print('Getting file list from XRootD server')
    status, listing = myclient.dirlist(gridpath, DirListFlags.LOCATE, timeout=10)
    out_files = []
    if listing is not None:
            for entry in listing:
                if entry.name.endswith('.root') and not entry.name == '':
                        out_files.append(gridserver + '/' + gridpath + '/' + entry.name)
            print("Successfully queried")
    else:
        print("XRootD path not accessable: %s", xrootd_path)
    return out_files


def main(xrootd_path, output):
    filelist = get_filelist(convert_srm_to_xrootd_path(xrootd_path))
    print("Filelist:\n")
    for filename in filelist:
        print("file: %s"% filename)
    try:
        subprocess.call(['hadd', output] + filelist)
        print(['hadd', output] + filelist)
    except KeyboardInterrupt:                                                   
        sys.exit(0) 
    except subprocess.CalledProcessError:                                       
        print "hadd failed"                                        
        sys.exit(1)  
 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="output root file", default="out.root")
    parser.add_argument("-i", "--input", help="XRootD path e.g.  root://cmsxrootd-kit.gridka.de//store/user/mschnepf/Skimming/*.root", type=str)
    args = parser.parse_args()
    output = args.output
    path = args.input
    #path = "root://cmsxrootd-redirectors.gridka.de//store/user/mschnepf/Skimming/WJets_TuneCP5_13TeV-pythia8_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/*.root"
    main(xrootd_path=path, output=output)

