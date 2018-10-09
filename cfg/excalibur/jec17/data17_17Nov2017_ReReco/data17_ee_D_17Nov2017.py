import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, SE_PATH_PREFIXES

RUN='D'
CH='ee'
JEC='{}{}_{}'.format(JEC_BASE, RUN, JEC_VERSION)


def config():
    cfg = configtools.getConfig('data', 2017, CH)
    cfg["InputFiles"].set_input(
        bmspathD="{}/dsavoiu/Skimming/ZJet_DoubleEG_Run2017D-17Nov2017-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        ekppathD="{}/dsavoiu/Skimming/ZJet_DoubleEG_Run2017D-17Nov2017-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt')]
    cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/'+JEC+'_DATA/'+JEC+'_DATA')
    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    cfg['ProvideL2ResidualCorrections'] = True
    cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res', 'L1L2L3Res'])

    return cfg
