
import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES

RUNS=['B', 'C', 'D', 'E', 'F']
CH='mm'
JEC='{0}_{1}_SimpleL1'.format(JEC_BASE, JEC_VERSION)


def config():
    cfg = configtools.getConfig('mc', 2017, CH, JEC=JEC, JER=JER)
    cfg["InputFiles"].set_input(
        path="{}/mhorzela/Skimming/ZJet_DYJetsToLL_Summer19-madgraphMLM_realistic_v6-v3/*.root".format(SE_PATH_PREFIXES["xrootd_gridka_nrg"]),
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Collisions17/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt')]

    cfg['Pipelines']['default']['Quantities'] += ['puWeight{}'.format(runperiod) for runperiod in ['B', 'C', 'D', 'E', 'F']]
    cfg = configtools.expand(cfg, ['nocuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3'])

    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/mc_weights/mc17ul_DYJets_madgraph_data_15May18/PUWeights_' + ''.join(['B', 'C', 'D', 'E', 'F']) + '_15May2018_DYJetsToLL_madgraphMLM.root')
    cfg['NumberGeneratedEvents'] = 101077576
    cfg['GeneratorWeight'] = 1.0
    cfg['CrossSection'] = 6077.22  # from XSDB: https://cms-gen-dev.cern.ch/xsdb/?searchQuery=DAS=DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8

    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    cfg['ApplyElectronVID'] = True
    cfg['ElectronVIDName'] = "Fall17-94X-V2"
    cfg['ElectronVIDType'] = "cutbased"
    cfg['ElectronVIDWorkingPoint'] = "tight"

    cfg['Processors'] += ['producer:ZJetPUWeightProducer']
    cfg['ZJetPUWeightFiles'] = [os.path.join(configtools.getPath() ,'data/pileup/mc_weights/mc17_DYJets_madgraph/PUWeights_{}_17Nov2017_DY1JetsToLL_Fall17-madgraphMLM_realistic_v10-v1.root'.format(runperiod)) for runperiod in ['B', 'C', 'D', 'E', 'F']]
    cfg['ZJetPUWeightSuffixes'] = ['{}'.format(runperiod) for runperiod in ['B', 'C', 'D', 'E', 'F']]

    return cfg
