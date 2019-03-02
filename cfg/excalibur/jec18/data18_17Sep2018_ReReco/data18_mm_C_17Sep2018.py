import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, SE_PATH_PREFIXES, GOLDEN_JSON

RUN='C'
CH='mm'
JEC='{}{}_{}'.format(JEC_BASE, RUN, JEC_VERSION)


def config():
    cfg = configtools.getConfig('data', 2018, CH, JEC=JEC)
    cfg["InputFiles"].set_input(
        bmspathC="{}/dsavoiu/Skimming/ZJet_DoubleMuon_Run2018C-17Sep2018-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        ekppathC="{}/dsavoiu/Skimming/ZJet_DoubleMuon_Run2018C-17Sep2018-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
        sg0pathC="{}/dsavoiu/Skimming/ZJet_DoubleMuon_Run2018C-17Sep2018-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/{}'.format(GOLDEN_JSON))]

    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    cfg['ProvideL2ResidualCorrections'] = True
    cfg = configtools.expand(cfg, ['basiccuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res', 'L1L2L3Res'])

    return cfg
