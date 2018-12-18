import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES

RUN='BCDEFGH'
CH='mm'
JEC='{}_{}'.format(JEC_BASE, JEC_VERSION)


def config():
    cfg = configtools.getConfig('mc', 2018, CH, JEC=JEC, JER=JER)
    cfg["InputFiles"].set_input(
        # bmspath3="{}/dsavoiu/Skimming/ZJet_DY3JetsToLL_Fall17-madgraphMLM_realistic_v10-v2/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        # ekppath3="{}/dsavoiu/Skimming/ZJet_DY3JetsToLL_Fall17-madgraphMLM_realistic_v10-v2/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        sg0pathE="{}/dsavoiu/Skimming/ZJet_DY3JetsToLL_Autumn18-madgraphMLM_realistic_v15-v2/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),    
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_314472-322633_13TeV_PromptReco_Collisions18_JSON.txt')]

    cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3'])
    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/mc_weights/mc17_DYJets_madgraph/PUWeights_BCDEF_17Nov2017_DY3JetsToLL_Fall17-madgraphMLM_realistic_v10-v2.root')
    cfg['NumberGeneratedEvents'] = 5647967
    cfg['GeneratorWeight'] = 1.0
    # cfg['CrossSection'] = 101.8*1.23  # from mc16 config
    cfg['CrossSection'] = 111.5 * 8.937 # from https://cms-gen-dev.cern.ch/xsdb/?searchQuery=DAS=DY3JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8

    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    return cfg


