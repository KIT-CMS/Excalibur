import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, SE_PATH_PREFIXES

RUN='F'
CH='ee'
JEC='{}{}_{}'.format(JEC_BASE, RUN, JEC_VERSION)


def config():
    cfg = configtools.getConfig('data', 2017, CH, JEC=JEC)
    cfg["InputFiles"].set_input(
        pathF="{}/dsavoiu/Skimming/ZJet_DoubleEG_Run2017F-17Nov2017-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        # bmspathF="{}/dsavoiu/Skimming/ZJet_DoubleEG_Run2017F-17Nov2017-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        # ekppathF="{}/dsavoiu/Skimming/ZJet_DoubleEG_Run2017F-17Nov2017-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt')]

    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    cfg['ProvideL2ResidualCorrections'] = True
    cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res', 'L1L2L3Res'])

    return cfg
