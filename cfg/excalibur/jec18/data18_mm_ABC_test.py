import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, SE_PATH_PREFIXES

RUN='ABCD'
CH='mm'
JEC='{}{}_{}'.format(JEC_BASE, "DE", JEC_VERSION)


def config():
    cfg = configtools.getConfig('data', 2018, CH, JEC=JEC)
    cfg["InputFiles"].set_input(
        #bmspathE="{}/mschnepf/Skimming/ZJet_DoubleMuon_RUN2018D_13TeV-PromptReco-v2/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        #bmspathE="{}/mschnepf/Skimming/ZJet_DoubleMuon_RUN2018D_13TeV-PromptReco-v2/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        sg0path1="{}/dsavoiu/Skimming/ZJet_DoubleMuon_Run2018A-17Sep2018-v2/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        sg0path2="{}/dsavoiu/Skimming/ZJet_DoubleMuon_Run2018B-17Sep2018-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        sg0path3="{}/dsavoiu/Skimming/ZJet_DoubleMuon_Run2018C-17Sep2018-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        bmspathA="{}/dsavoiu/Skimming/ZJet_DoubleMuon_Run2018A-17Sep2018-v2/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        bmspathB="{}/dsavoiu/Skimming/ZJet_DoubleMuon_Run2018B-17Sep2018-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        bmspathC="{}/dsavoiu/Skimming/ZJet_DoubleMuon_Run2018C-17Sep2018-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt')]
    cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/'+JEC+'_DATA/'+JEC+'_DATA')
    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    cfg['ProvideL2ResidualCorrections'] = True
    cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res', 'L1L2L3Res'])
    return cfg

