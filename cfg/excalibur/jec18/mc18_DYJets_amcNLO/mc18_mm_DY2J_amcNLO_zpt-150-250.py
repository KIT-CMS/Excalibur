import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES

CH='mm'
JEC='{}_{}'.format(JEC_BASE, JEC_VERSION)


def config():
    cfg = configtools.getConfig('mc', 2018, CH, JEC=JEC, JER=JER)
    cfg["InputFiles"].set_input(
        path1="{}/cheideck/Skimming/ZJet_DY2JetsToLL_Autumn18_LHEZpT_150-250_amcnloFXFX-pythia8_upgrade2018_realistic_v15-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
    )

    cfg = configtools.expand(cfg, ['basiccuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])

    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/mc_weights/mc18_DYJets_madgraph/PUWeights_ABCD_17Sep2018_DY1JetsToLL_Autumn18-madgraphMLM_realistic_v15-v2.root')

    cfg['NumberGeneratedEvents'] = 42787613
    cfg['GeneratorWeight'] = 0.332794516955
    cfg['CrossSection'] = 15.65  # from XSDB: https://cms-gen-dev.cern.ch/xsdb/?searchQuery=DAS=DY2JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8

    cfg['VertexSummary'] = 'goodOfflinePrimaryVerticesSummary'

    # for testing JetID differences
    cfg['JetIDVersion'] = 2018  # for object-based JetID
    cfg['CutJetIDVersion'] = 2018  # for event-based JetID

    return cfg

# python getGeneratorWeight.py -n NONE /storage/gridka-nrg/cheideck/Skimming/ZJet_DY2JetsToLL_Autumn18_LHEZpT_150-250_amcnloFXFX-pythia8_upgrade2018_realistic_v15-v1/*.root
# ...processing file 0 (nickname: *)
#         weighted entries =  13763.0
#         entries =  42353.0
# ...processing file 100 (nickname: *)
#         weighted entries =  1390425.0
#         entries =  4181121.0
# ...processing file 200 (nickname: *)
#         weighted entries =  2613541.0
#         entries =  7864331.0
# ...processing file 300 (nickname: *)
#         weighted entries =  3850393.0
#         entries =  11581617.0
# ...processing file 400 (nickname: *)
#         weighted entries =  5247297.0
#         entries =  15777775.0
# ...processing file 500 (nickname: *)
#         weighted entries =  6519635.0
#         entries =  19596377.0
# ...processing file 600 (nickname: *)
#         weighted entries =  7794517.0
#         entries =  23428245.0
# ...processing file 700 (nickname: *)
#         weighted entries =  9044559.0
#         entries =  27184031.0
# ...processing file 800 (nickname: *)
#         weighted entries =  10187533.0
#         entries =  30608147.0
# ...processing file 900 (nickname: *)
#         weighted entries =  11461037.0
#         entries =  34438755.0
# ...processing file 1000 (nickname: *)
#         weighted entries =  12741888.0
#         entries =  38283102.0
# ...processing file 1100 (nickname: *)
#         weighted entries =  14016129.0
#         entries =  42117089.0
#         n_events_generated: 42787613
#         generatorWeight: 0.332794516955
# }

