import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES

CH='mm'
JEC='{}_{}'.format(JEC_BASE, JEC_VERSION)


def config():
    cfg = configtools.getConfig('mc', 2018, CH, JEC=JEC, JER=JER)
    cfg["InputFiles"].set_input(
        path2="{}/cheideck/Skimming/ZJet_DYJetsToLL_Autumn18-amcatnloFXFX-pythia8_upgrade2018_realistic_v15_ext2-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
    )

    cfg = configtools.expand(cfg, ['basiccuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])

    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/mc_weights/mc18_DYJets_madgraph/PUWeights_ABCD_17Sep2018_DY2JetsToLL_Autumn18-madgraphMLM_realistic_v15-v2.root')

    cfg['NumberGeneratedEvents'] = 193215674
    cfg['GeneratorWeight'] = 1.0
    cfg['CrossSection'] = 6435.0  # from XSDB (from RunIISpring18 instead of RunIIAutumn18, update if available!)

    cfg['VertexSummary'] = 'goodOfflinePrimaryVerticesSummary'

    return cfg


