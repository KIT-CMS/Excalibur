import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES

RUN='BCDEFGH'
CH='mm'
JEC='{}_{}'.format(JEC_BASE, JEC_VERSION)


def config():
    cfg = configtools.getConfig('mc', 2016, CH, JEC=JEC, JER=JER)
    cfg["InputFiles"].set_input(
        ekppath="{}/tberger/Skimming/MC-Summer16_metfix/Zll_DY1JetsToLL_M-50_madgraphMLM-pythia8_RunIISummer16/*.root".format(SE_PATH_PREFIXES['srm_desy_dcache']),
        bmspath="{}/tberger/Skimming/MC-Summer16_metfix/Zll_DY1JetsToLL_M-50_madgraphMLM-pythia8_RunIISummer16/*.root".format(SE_PATH_PREFIXES['srm_desy_dcache']),
        nafpath="{}/tberger/Skimming/MC-Summer16_metfix/Zll_DY1JetsToLL_M-50_madgraphMLM-pythia8_RunIISummer16/*.root".format(SE_PATH_PREFIXES['local_desy_dcache']),
    )

    cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3'])

    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/PUWeights_'+RUN+'_13TeV_23Sep2016ReReco_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16.root')
    cfg['NumberGeneratedEvents'] = 62627174
    cfg['GeneratorWeight'] = 1.0
    cfg['CrossSection'] = 1012.5*1.23 # for: 1Jet_madgraphMLM

    return cfg
