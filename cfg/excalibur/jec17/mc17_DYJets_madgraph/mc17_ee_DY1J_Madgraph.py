import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES

CH='ee'
JEC='{}_{}'.format(JEC_BASE, JEC_VERSION)


def config():
    cfg = configtools.getConfig('mc', 2017, CH, JEC=JEC, JER=JER)
    cfg["InputFiles"].set_input(
        path="{}/cheideck/Skimming/ZJet_DY1JetsToLL_Fall17-madgraphMLM_realistic_v10-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        # bmspath1="{}/dsavoiu/Skimming/ZJet_DY1JetsToLL_Fall17-madgraphMLM_realistic_v10-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        # ekppath1="{}/dsavoiu/Skimming/ZJet_DY1JetsToLL_Fall17-madgraphMLM_realistic_v10-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt')]

    cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3'])
    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/mc_weights/mc17_DYJets_madgraph/PUWeights_BCDEF_17Nov2017_DY1JetsToLL_Fall17-madgraphMLM_realistic_v10-v1.root')
    cfg['NumberGeneratedEvents'] = 32553254
    cfg['GeneratorWeight'] = 1.0
    cfg['CrossSection'] = 1012.5*1.23  # from mc16 config

    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    cfg['ElectronID'] = 'user'  # old ID no longer written out in new skim
    cfg['ApplyElectronVID'] = True
    cfg['ElectronVIDName'] = "Fall17-94X-V1"
    cfg['ElectronVIDType'] = "cutbased_v2"
    cfg['ElectronVIDWorkingPoint'] = "tight"

    return cfg
