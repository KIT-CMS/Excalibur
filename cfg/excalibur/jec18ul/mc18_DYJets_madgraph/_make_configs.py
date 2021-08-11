"""
Quick and dirty script to generate config files for all channels, JEC versions, etc,
which can then be edited manually. Note: existing configs with matching names will
be overwritten!
"""

INPUT_TEMPLATE = '"{{}}/{userpath}/ZJet_DYJetsToLL_Summer19-madgraphMLM_realistic_v11_L1v1-v1/*.root".format(SE_PATH_PREFIXES["xrootd_gridka_nrg"])'

TEMPLATE = """
import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES

RUNS={runs}
CH='{ch}'
JEC='{{0}}_{{1}}'.format(JEC_BASE, JEC_VERSION)


def config():
    cfg = configtools.getConfig('mc', 2018, CH, JEC=JEC, JER=JER)
    cfg["InputFiles"].set_input(
        path={input_path},
    )

    cfg['Pipelines']['default']['Quantities'] += ['puWeight{{}}'.format(runperiod) for runperiod in {runs}]
    cfg['Pipelines']['default']['Quantities'] += ['genWeight_{{}}'.format(lheWeightName) for lheWeightName in {lheWeightNames}]
    cfg['Pipelines']['default']['Quantities'] += ['jet1chf', 'jet1nhf', 'jet1ef', 'jet1mf', 'jet1hfhf', 'jet1hfemf', 'jet1pf']
    cfg['Pipelines']['default']['Quantities'] += ['jnpf', 'rawjnpf', 'mpflead', 'rawmpflead', 'mpfjets', 'rawmpfjets', 'mpfunclustered', 'rawmpfunclustered']

    cfg = configtools.expand(cfg, ['basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3'])

    cfg['MPFSplittingJetPtMin'] = 15.
    cfg['JNPFJetPtMin'] = 15.

    # cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/mc_weights/mc18ul_DYJets_madgraph_12Nov19/PUWeights_' + ''.join({runs}) + '_12Nov2019_DYJetsToLL_madgraphMLM.root')
    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/jec18ul/PUWeights_2018_Data_ABCD_12Nov2019_UL2018_MC_Summer19-madgraphMLM_realistic_v11_L1v1.root')
    cfg['NumberGeneratedEvents'] = 104017741
    cfg['GeneratorWeight'] = 1.0
    cfg['CrossSection'] = 6077.22  # from XSDB: https://cms-gen-dev.cern.ch/xsdb/?searchQuery=DAS=DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8

    cfg['CutBackToBack'] = 0.44

    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    cfg['ApplyElectronVID'] = True
    cfg['ElectronVIDName'] = "Fall17-94X-V2"
    cfg['ElectronVIDType'] = "cutbased"
    cfg['ElectronVIDWorkingPoint'] = "tight"

    if CH == 'ee':
        cfg['Processors'].insert(cfg['Processors'].index('producer:ZJetValidElectronsProducer'), 'producer:ElectronCorrectionsProducer',)
        cfg['ApplyElectronEnergyCorrections'] = True
        cfg['ElectronEnergyCorrectionTags'] = ["electronCorrection:ecalTrkEnergyPostCorr"]
        cfg["CutElectronSubPtMin"] = 15.0
    # TODO: Update to 2018
    # elif CH == 'mm':
    #     cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
    #     cfg['MuonRochesterCorrectionsFile'] = os.path.join(configtools.getPath(),'../Artus/KappaAnalysis/data/rochcorr/RoccoR2017UL.txt')
    #     cfg['MuonEnergyCorrection'] = 'rochcorr2017ul'
    #     cfg["CutMuonSubPtMin"] = 10.0

    cfg['CutJetID'] = 'tightlepveto'  # choose event-based JetID selection
    cfg['CutJetIDVersion'] = '2018UL'  # for event-based JetID
    cfg['CutJetIDFirstNJets'] = 2

    cfg['Processors'] += ['producer:ZJetPUWeightProducer']
    # cfg['ZJetPUWeightFiles'] = [os.path.join(configtools.getPath() ,'data/pileup/mc_weights/mc18ul_DYJets_madgraph_data_12Nov19/PUWeights_{{}}_12Nov2019_DYJetsToLL_madgraphMLM.root'.format(runperiod)) for runperiod in {runs}]
    cfg['ZJetPUWeightFiles'] = [os.path.join(configtools.getPath() ,'data/pileup/jec18ul/PUWeights_2018_Data_{{}}_12Nov2019_UL2018_MC_Summer19-madgraphMLM_realistic_v11_L1v1.root'.format(runperiod)) for runperiod in {runs}]

    cfg['ZJetPUWeightSuffixes'] = ['{{}}'.format(runperiod) for runperiod in {runs}]

    cfg['Processors'] += ['producer:ZJetGenWeightProducer']
    cfg['ZJetGenWeightNames'] = {lheWeightNames}

    cfg['JetEtaPhiCleanerFile'] = os.path.join(configtools.getPath(), 'data/cleaning/jec18ul/Summer19UL18_V1/hotjets-UL18.root')
    cfg['JetEtaPhiCleanerHistogramNames'] = ["h2hot_ul18_plus_hem1516_and_hbp2m1"]

    cfg['HltPaths'] = {{
        'ee': ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'],
        'mm': ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ', 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8']
    }}[CH]

    return cfg
"""

def make():
  runs = ['A', 'B', 'C', 'D']
  lheWeightNames = ['isrDefup', 'isrDefdown', 'fsrDefup', 'fsrDefdown']

  #for jecv_suffix in ['SimpleL1', 'ComplexL1']:
  for ch in ["mm", "ee"]:
    _cfg = TEMPLATE.format(
      runs=runs,
      lheWeightNames=lheWeightNames,
      ch=ch,
      input_path=INPUT_TEMPLATE.format(
        userpath='mhorzela/Skimming',
      ),
    )
    _fname = "mc18_{ch}_{runs}_DYJets_Madgraph.py".format(
      ch=ch,
      runs=''.join(runs),
    )
    with open(_fname, 'w') as _f:
      _f.write(_cfg)

if __name__ == '__main__':
    make()
