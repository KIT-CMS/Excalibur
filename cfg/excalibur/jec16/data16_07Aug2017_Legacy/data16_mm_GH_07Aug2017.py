import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, SE_PATH_PREFIXES

RUN='GH'
CH='mm'
JEC='{}{}_{}'.format(JEC_BASE, RUN, JEC_VERSION)


def config():
    cfg = configtools.getConfig('data', 2016, CH, JEC=JEC, IOV=RUN)
    cfg["InputFiles"].set_input(
        bmspathF="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016F-Legacy-07Aug2017-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        bmspathG="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016G-Legacy-07Aug2017-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        bmspathH="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016H-Legacy-07Aug2017-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        ekppathF="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016F-Legacy-07Aug2017-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        ekppathG="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016G-Legacy-07Aug2017-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
        ekppathH="{}/tberger/Skimming/ZJet_DoubleMuon_Run2016H-Legacy-07Aug2017-v1/*.root".format(SE_PATH_PREFIXES['srm_gridka_nrg']),
    )
    cfg['JsonFiles'] =  [os.path.join(configtools.getPath(),'data/json/Cert_{}_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'.format(RUN))]

    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'  # above skims do not contain 'goodOfflinePrimaryVerticesSummary'
    cfg['ProvideL2ResidualCorrections'] = True
    cfg = configtools.expand(cfg, ['nocuts', 'basiccuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res', 'L1L2L3Res'])

    return cfg
