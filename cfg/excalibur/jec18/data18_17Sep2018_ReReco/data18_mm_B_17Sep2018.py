import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, SE_PATH_PREFIXES, GOLDEN_JSON

#RUN='B'
RUN='F'  # use Run2017F here because we are testing 'Fall17' JECs with 2018 data
CH='mm'
JEC='{}{}_{}'.format(JEC_BASE, RUN, JEC_VERSION)


def config():
    cfg = configtools.getConfig('data', 2018, CH, JEC=JEC)
    cfg["InputFiles"].set_input(
        bmspathA="{}/dsavoiu/Skimming/ZJet_DoubleMuon_Run2018B-17Sep2018-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        ekppathA="{}/dsavoiu/Skimming/ZJet_DoubleMuon_Run2018B-17Sep2018-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        sg0pathA="{}/dsavoiu/Skimming/ZJet_DoubleMuon_Run2018B-17Sep2018-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/{}'.format(GOLDEN_JSON))]

    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    cfg['ProvideL2ResidualCorrections'] = True
    cfg = configtools.expand(cfg, ['basiccuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res', 'L1L2L3Res'])

    return cfg
