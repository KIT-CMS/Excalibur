import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, SE_PATH_PREFIXES

RUN='ABCD'
CH='mm'
JEC='{}{}_{}'.format(JEC_BASE, RUN, JEC_VERSION)


def config():
    cfg = configtools.getConfig('data', 2018, CH)
    cfg["InputFiles"].set_input(
        #bmspathE="{}/mschnepf/Skimming/ZJet_DoubleMuon_RUN2018D_13TeV-PromptReco-v2/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        #bmspathE="{}/mschnepf/Skimming/ZJet_DoubleMuon_RUN2018D_13TeV-PromptReco-v2/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        sg0path1="{}/mschnepf/Skimming/ZJet_DoubleMuon_RUN2018A_13TeV-PromptReco-v3/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        sg0path2="{}/mschnepf/Skimming/ZJet_DoubleMuon_RUN2018B_13TeV-PromptReco-v2/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        sg0path3="{}/mschnepf/Skimming/ZJet_DoubleMuon_RUN2018C_13TeV-PromptReco-v3/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        sg0path4="{}/mschnepf/Skimming/ZJet_DoubleMuon_RUN2018D_13TeV-PromptReco-v2/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt')]
    cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/'+JEC+'_DATA/'+JEC+'_DATA')
    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    cfg['ProvideL2ResidualCorrections'] = True
    cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res', 'L1L2L3Res'])
    return cfg

