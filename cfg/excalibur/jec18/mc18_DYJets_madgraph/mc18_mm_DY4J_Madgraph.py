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
    cfg = configtools.getConfig('mc', 2017, CH, JEC=JEC, JER=JER)
    cfg["InputFiles"].set_input(
        # bmspath4="{}/dsavoiu/Skimming/ZJet_DY4JetsToLL_Fall17-madgraphMLM_realistic_v10-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        # ekppath4="{}/dsavoiu/Skimming/ZJet_DY4JetsToLL_Fall17-madgraphMLM_realistic_v10-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        sg0pathE="{}/mschnepf/Skimming/ZJet_DYJetsToLL_13TeV-madgraphMLM_upgrade2018_realistic_v10-v2/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_314472-322633_13TeV_PromptReco_Collisions18_JSON.txt')]
    cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3'])
    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/mc_weights/mc17_DYJets_madgraph/PUWeights_BCDEF_17Nov2017_DY4JetsToLL_Fall17-madgraphMLM_realistic_v10-v1.root')
    print("not definded!")
    exit(-1)
    cfg['NumberGeneratedEvents'] = ???
    cfg['GeneratorWeight'] = 1.0
    cfg['CrossSection'] = 54.8*1.23  # from mc16 config

    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    return cfg


