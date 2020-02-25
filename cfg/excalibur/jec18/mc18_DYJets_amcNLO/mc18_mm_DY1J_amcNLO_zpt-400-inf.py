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
        path1="{}/cheideck/Skimming/ZJet_DY1JetsToLL_Autumn18_LHEZpT_400-inf_amcnloFXFX-pythia8_upgrade2018_realistic_v15-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
    )

    cfg = configtools.expand(cfg, ['basiccuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])

    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/mc_weights/mc18_DYJets_madgraph/PUWeights_ABCD_17Sep2018_DY1JetsToLL_Autumn18-madgraphMLM_realistic_v15-v2.root')

    cfg['NumberGeneratedEvents'] = 1245138
    cfg['GeneratorWeight'] = 0.689517145891
    cfg['CrossSection'] = 0.1193  # from XSDB: https://cms-gen-dev.cern.ch/xsdb/?searchQuery=DAS=DY1JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8

    cfg['VertexSummary'] = 'goodOfflinePrimaryVerticesSummary'

    # for testing JetID differences
    cfg['JetIDVersion'] = 2018  # for object-based JetID
    cfg['CutJetIDVersion'] = 2018  # for event-based JetID

    return cfg

# python getGeneratorWeight.py -n NONE /storage/gridka-nrg/cheideck/Skimming/ZJet_DY1JetsToLL_Autumn18_LHEZpT_400-inf_amcnloFXFX-pythia8_upgrade2018_realistic_v15-v1/*.root
# ...processing file 0 (nickname: *)
#         weighted entries =  3118.0
#         entries =  4552.0
#         n_events_generated: 1245138
#         generatorWeight: 0.689517145891
# }

