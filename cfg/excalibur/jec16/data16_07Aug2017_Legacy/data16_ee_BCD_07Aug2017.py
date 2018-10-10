import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, SE_PATH_PREFIXES

RUN='BCD'
CH='ee'
JEC='{}{}_{}'.format(JEC_BASE, RUN, JEC_VERSION)


def config():
    cfg = configtools.getConfig('data', 2016, CH, JEC=JEC, IOV=RUN)
    cfg["InputFiles"].set_input(
        bmspathB1="{}/dsavoiu/Skimming/ZJet_DoubleEG_Run2016B-Legacy-07Aug2017_ver1-v1_egmSSbackport/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        bmspathB2="{}/dsavoiu/Skimming/ZJet_DoubleEG_Run2016B-Legacy-07Aug2017_ver2-v2_egmSSbackport/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        bmspathC="{}/dsavoiu/Skimming/ZJet_DoubleEG_Run2016C-Legacy-07Aug2017-v1_egmSSbackport/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        bmspathD="{}/dsavoiu/Skimming/ZJet_DoubleEG_Run2016D-Legacy-07Aug2017-v1_egmSSbackport/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        ekppathB1="{}/dsavoiu/Skimming/ZJet_DoubleEG_Run2016B-Legacy-07Aug2017_ver1-v1_egmSSbackport/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        ekppathB2="{}/dsavoiu/Skimming/ZJet_DoubleEG_Run2016B-Legacy-07Aug2017_ver2-v2_egmSSbackport/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        ekppathC="{}/dsavoiu/Skimming/ZJet_DoubleEG_Run2016C-Legacy-07Aug2017-v1_egmSSbackport/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        ekppathD="{}/dsavoiu/Skimming/ZJet_DoubleEG_Run2016D-Legacy-07Aug2017-v1_egmSSbackport/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
    )
    cfg['JsonFiles'] =  [os.path.join(configtools.getPath(),'data/json/Cert_{}_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'.format(RUN))]

    cfg['ProvideL2ResidualCorrections'] = True
    cfg = configtools.expand(cfg, ['nocuts', 'basiccuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res', 'L1L2L3Res'])

    return cfg
