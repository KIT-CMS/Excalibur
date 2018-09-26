import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, SE_PATH_PREFIXES

RUN='BCDEFGH'
CH='mm'
JEC='{}_{}'.format(JEC_BASE, JEC_VERSION)


def config():
    cfg = configtools.getConfig('mc', 2017, CH)
    cfg["InputFiles"].set_input(
        bmspathB="{}/dsavoiu/Skimming/ZJet_DY2JetsToLL_Fall17-madgraphMLM_realistic_v10-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        #bmspathB="/storage/gridka-nrg/dsavoiu/Skimming/ZJet_DY2JetsToLL_Fall17-madgraphMLM_realistic_v10-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt')]
    cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/'+JEC+'_MC/'+JEC+'_MC')
    cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3'])
    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/mc_weights/mc17_DYJets_madgraph/PUWeights_BCDEF_17Nov2017_DY2JetsToLL_Fall17-madgraphMLM_realistic_v10-v1.root')
    cfg['NumberGeneratedEvents'] = 11623646
    cfg['GeneratorWeight'] = 1.0
    cfg['CrossSection'] = 332.8*1.23  # from mc16 config

    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    return cfg


