#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ArtusConfigBase provides the tools to make a valid artus config.

The most used functions are:
  - BaseConfig to generate a default configuration
  - CreateFileList to create a list of input files
  - Run to acutally call artus and run it
"""
import copy
import glob
import socket
import ConfigParser
import os
import stat
import getpass
import json
import sys
import ArtusConfigFunctions


def BaseConfig(inputtype, run='2012', analysis='mm', tagged=True,
                        rundepMC=False, lhe=False, flavourCorrections=False):
    """This functions is here for backward compatibility."""
    return getConfig(inputtype, run, analysis, tagged=tagged, rundep=rundepMC,
        addLHE=lhe, flavourCorrections=flavourCorrections)


def getConfig(inputtype, year, channel, **kwargs):
    """
        Main function to get a basic config.

        According to the three main categories (type, year, channel), the config
        is modified according to whats specified in ArtusConfigFunctions.
        All combinations of the categories are considered, if config functions are available.
    """

    # python class/function names cant start with a number -> add '_' to year
    l = [channel, inputtype, '_' + str(year)]
    print "Getting cfg for", channel, inputtype, year
    cfg = ArtusConfigFunctions.getBaseConfig(**kwargs)

    # iterate over all combinations and call updateConfig(single-entry tuples first):
    for i in l:
        updateConfig(cfg, (i), **kwargs)
    for i in l:
        for j in l:
            updateConfig(cfg, (i, j), **kwargs)
    for i in l:
        for j in l:
            for k in l:
                updateConfig(cfg, (i, j, k), **kwargs)

    return cfg


def updateConfig(conf, tupl, **kwargs):
    string = "".join(tupl)
    if string in dir(ArtusConfigFunctions):
        getattr(ArtusConfigFunctions, string)(conf, **kwargs)


def getPath(variable='EXCALIBUR_BASE', nofail=False):
    try:
        return os.environ[variable]
    except:
        print variable, "is not in shell variables:", os.environ.keys()
        print "Please source scripts/ini_excalibur and CMSSW!"
        if nofail:
            return None
        exit(1)


def addCHS(algorithms):
    """can be used as [algos =] addCHS(algos) or algos = addCHS([AK5, etc.])"""
    algorithms += [a.replace("PFJets", "PFJetsCHS") for a in algorithms
        if "PFJets" in a and "PFJetsCHS" not in a and a.replace("PFJets", "PFJetsCHS") not in algorithms]
    return algorithms


def setInputFiles(ekppath, nafpath=None):
    """Return ekppath if you're at EKP, nafpath if at NAF. """
    d = {'ekp': ekppath, 'naf': nafpath}
    host = socket.gethostname()[:3]
    if host in d:
        if d[host] in [None, '']:
            sys.exit("ERROR: You're at %s, but the path for this skim is not set here!" % host.upper())
        else:
            return d[host]
    else:
        sys.exit("ERROR: Cant determine input file location!")


def ApplySampleReweighting(conf, sample="herwig", referencelumi_fbinv=1.0):
    """Weights for pt hat binned samples"""
    picobarn2femtobarn = 1000
    d = {
        "herwig": {
            "weights":[
                0.0,  # 400.8834/6167020,# 0-15 (not existing, prep/das inconsistent)
                70.551230 / 200000,  # 15-20
                77.535330 / 150154,  # 20-30 (old sample)
                62.745670 / 150000,  # 30-50
                28.738060 / 100160,  # 50-80 (old sample)
                9.7459310 / 96000,   # 80-120
                2.8100250 / 98560,   # 120-170
                0.7702934 / 100000,  # 170-230
                0.2142680 / 96640,   # 230-300
                0.08858213 / 90517,  # 300-inf
            ],
            "names": [
                "0-15",
                "15-20",
                "20-30",
                "30-50",
                "50-80",
                "80-120",
                "120-170",
                "170-230",
                "230-300",
                "300_"
            ],
        },
        "herwigRD": {
            "weights": [
                0.0,  # 400.8834/6167020,# 0-15 (not existing, prep/das inconsistent)
                0.0, #70.551230 / 1,  # 15-20 (not existing for RD?)
                77.535330 / 141323,  # 20-30
                62.745670 / 150000,  # 30-50
                28.738060 / 100160,  # 50-80
                9.7459310 / 100000,   # 80-120
                2.8100250 / 100000,   # 120-170
                0.7702934 / 121460,  # 170-230
                0.2142680 / 100000,   # 230-300
                0.08858213 / 100000,  # 300-inf
            ],
            "names": [
                "0-15",
                "15-20",
                "20-30",
                "30-50",
                "50-80",
                "80-120",
                "120-170",
                "170-230",
                "230-300",
                "300_"
            ],
        },
    }

    if sample not in d:
        print "No sample weights for this dataset:", sample
        print "Weights are available for:", ", ".join(d.keys())
        print "Please add them in ArtusConfigBase or do not use ApplySampleReweighting."
        exit(0)

    result = [picobarn2femtobarn * referencelumi_fbinv * w for w in d[sample]['weights']]
    conf["EnableSampleReweighting"] = True
    conf["SampleWeights"] = result
    conf["SampleNames"] = d[sample]['names']
    return conf


def expand(config, variations=[], algorithms=[], default="default"):
    """create pipelines for each algorithm times each variation"""
    pipelines = config['Pipelines']
    p = config['Pipelines'][default]
    if p['JetAlgorithm'] not in algorithms:
        algorithms.append(p['JetAlgorithm'])
    if config['InputType'] == 'data' and "Res" not in p['JetAlgorithm']:
        algorithms.append(p['JetAlgorithm'] + "Res")

    #find global algorithms
    config["GlobalAlgorithms"] = []
    removelist = ["Jets", "L1", "L2", "L3", "Res", "Hcal", "Custom"]
    for algo in algorithms:
        for r in removelist:
            algo = algo.replace(r, "").replace("CHS", "chs")
        if algo not in config["GlobalAlgorithms"]:
            config["GlobalAlgorithms"].append(algo)

    # copy for variations
    for v in variations:
        if v == 'all':
            pipelines[v] = copy.deepcopy(p)
            pipelines[v]['Cuts'] = []
            if 'incut' in pipelines[v]['Filter']:
                    pipelines[v]['Filter'].remove('incut')
        elif v == 'zcuts':
            pipelines[v] = copy.deepcopy(p)
            removelist = ['leadingjet_pt', 'back_to_back']
            for cut in removelist:
                if cut in pipelines[v]['Cuts']:
                    pipelines[v]['Cuts'].remove(cut)
        elif v == 'fullcuts':
            pipelines[v] = copy.deepcopy(p)
            pipelines[v]['Cuts'].append('leadingjet_eta')
            pipelines[v]['Cuts'].append('secondleading_to_zpt')
            pipelines[v]['CutLeadingJetEta'] = 1.3
            pipelines[v]['CutSecondLeadingToZPt'] = 0.2
        elif v == 'incut':
            pipelines[v] = copy.deepcopy(p)

    # remove template pipeline
    pipelines.pop(default)

    # copy for algorithms, naming scheme: incut_algo
    for name, p in pipelines.items():
        for algo in algorithms:
            pipelines[name + "_" + algo] = copy.deepcopy(p)
            pipelines[name + "_" + algo]["JetAlgorithm"] = algo
        del pipelines[name]

    return config


def pipelinediff(config, to=None):
    print "Comparing", len(config['Pipelines']), "pipelines:"
    if to == None:
        to = filter(lambda x: 'incut' in x, config['Pipelines'].keys())[0]

    for name, p in config['Pipelines'].items():
        if name != to:
            print "- Compare", name, "to", to
            pipelinediff2(p, config['Pipelines'][to])
    print


def pipelinediff2(p1=None, p2=None):
    for k, v in p1.items():
        if k in p2.keys():
            if p1[k] != p2[k]:
                print "    different %s: %s != %s" % (k, str(p1[k]), str(p2[k]))

