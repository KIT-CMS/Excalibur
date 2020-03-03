import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common_simple import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES

RUN='B'
CH='ee'
JEC='{}_Run{}_{}'.format(JEC_BASE, RUN, JEC_VERSION)


def config():
    cfg = configtools.getConfig('data', 2017, CH, JEC=JEC, JER=JER)
    cfg["InputFiles"].set_input(
        #path="{}/rvoncube/Skimming/ZJet_DYJetsToLL_Summer19-madgraphMLM_mc2017_realistic_v6-v3_GT_106X_mc2017_realistic_v6/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
	path="/portal/ekpbms1/home/mhorzela/CMSSW_10_6_0_skimUL2017/src/Kappa/Skimming/zjet/configs/jec17ul/1060_DoubleMuon_Run2017_09Aug2019_UL2017-v1/test/106X_dataRun2_v20/testKappaSkim_out_106X_dataRun2_v20_numEvent100.root"    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt')]

    cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res'])#, 'L1L2L3Res'])

    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    cfg['ProvideL2ResidualCorrections'] = True
    
    cfg['ApplyElectronVID'] = True
    cfg['ElectronVIDName'] = "Fall17-94X-V2"
    cfg['ElectronVIDType'] = "cutbased"
    cfg['ElectronVIDWorkingPoint'] = "tight"

    return cfg
