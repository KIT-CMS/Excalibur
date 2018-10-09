import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, SE_PATH_PREFIX

RUN='BCD'
CH='mm'
JEC='{}{}_{}'.format(JEC_BASE, RUN, JEC_VERSION)


def config():
    cfg = configtools.getConfig('data', 2016, CH, JEC=JEC, IOV=RUN)
    cfg["InputFiles"].set_input(
        bmspathB1="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016B-Legacy-07Aug2017_ver1-v1/*.root".format(SE_PATH_PREFIX),
        bmspathB2="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016B-Legacy-07Aug2017_ver2-v1/*.root".format(SE_PATH_PREFIX),
        bmspathC="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016C-Legacy-07Aug2017-v1/*.root".format(SE_PATH_PREFIX),
        bmspathD="{}/tberger//Skimming/ZJet_DoubleMuon_Run2016D-Legacy-07Aug2017-v1/*.root".format(SE_PATH_PREFIX),
        ekppathB1="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016B-Legacy-07Aug2017_ver1-v1/*.root".format(SE_PATH_PREFIX),
        ekppathB2="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016B-Legacy-07Aug2017_ver2-v1/*.root".format(SE_PATH_PREFIX),
        ekppathC="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016C-Legacy-07Aug2017-v1/*.root".format(SE_PATH_PREFIX),
        ekppathD="{}/tberger//Skimming/ZJet_DoubleMuon_Run2016D-Legacy-07Aug2017-v1/*.root".format(SE_PATH_PREFIX),
        )
    cfg['JsonFiles'] =  [os.path.join(configtools.getPath(),'data/json/Cert_{}_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'.format(RUN))]

    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'  # above skims do not contain 'goodOfflinePrimaryVerticesSummary'
    cfg['ProvideL2ResidualCorrections'] = True
    cfg = configtools.expand(cfg, ['nocuts', 'basiccuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res', 'L1L2L3Res'])

    return cfg
