"""
Quick and dirty script to generate config files for all channels, JEC versions, etc,
which can then be edited manually. Note: existing configs with matching names will
be overwritten!
"""

INPUT_TEMPLATE = '"{{}}/{userpath}/ZJet_DYJetsToLL_Summer19-amcatnlo_realistic_v6-v2/*.root".format(SE_PATH_PREFIXES["xrootd_gridka_nrg"])'

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
    cfg = configtools.getConfig('mc', 2017, CH, JEC=JEC, JER=JER)
    cfg["InputFiles"].set_input(
        path={input_path},
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Collisions17/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt')]

    cfg['Pipelines']['default']['Quantities'] += ['puWeight{{}}'.format(runperiod) for runperiod in {runs}]
    cfg['Pipelines']['default']['Quantities'] += ['genWeight_{{}}'.format(lheWeightName) for lheWeightName in {lheWeightNames}]
    cfg['Pipelines']['default']['Quantities'] += ['jet1chf', 'jet1nhf', 'jet1ef', 'jet1mf', 'jet1hfhf', 'jet1hfemf', 'jet1pf']
    cfg['Pipelines']['default']['Quantities'] += ['jnpf', 'rawjnpf', 'mpflead', 'rawmpflead', 'mpfjets', 'rawmpfjets', 'mpfunclustered', 'rawmpfunclustered']

    cfg = configtools.expand(cfg, ['basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3'])

    cfg['JERMethod'] = 'hybrid'

    cfg['MPFSplittingJetPtMin'] = 15.
    cfg['JNPFJetPtMin'] = 15.

    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/mc_weights/mc17ul_DYJets_amcatnlo/PUWeights_' + ''.join({runs}) + '_DYJetsToLL_Summer19-amcatnlo_realistic_v6-v2.root')
    cfg['NumberGeneratedEvents'] = 101077576
    cfg['GeneratorWeight'] = 1.0
    cfg['CrossSection'] = 6529.0  # from XSDB: https://cms-gen-dev.cern.ch/xsdb/?searchQuery=DAS=DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8

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
    elif CH == 'mm':
        cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
        cfg['MuonRochesterCorrectionsFile'] = os.path.join(configtools.getPath(),'../Artus/KappaAnalysis/data/rochcorr/RoccoR2017UL.txt')
        cfg['MuonEnergyCorrection'] = 'rochcorr2017ul'

    cfg['CutJetID'] = 'tightlepveto'  # choose event-based CutJetID (Excalibur) selection, alternatively use JetID (Artus)
    cfg['CutJetIDVersion'] = '2017UL'  # for event-based JetID
    cfg['CutJetIDFirstNJets'] = 2

    cfg['EnableTypeIModification'] = False

    cfg['Processors'] += ['producer:ZJetPUWeightProducer']
    cfg['ZJetPUWeightFiles'] = [os.path.join(configtools.getPath() ,'data/pileup/mc_weights/mc17ul_DYJets_amcatnlo/PUWeights_{{}}_DYJetsToLL_Summer19-amcatnlo_realistic_v6-v2.root'.format(runperiod)) for runperiod in {runs}]
    cfg['ZJetPUWeightSuffixes'] = ['{{}}'.format(runperiod) for runperiod in {runs}]

    cfg['Processors'] += ['producer:ZJetGenWeightProducer']
    cfg['ZJetGenWeightNames'] = {lheWeightNames}

    cfg['Processors'].insert(cfg['Processors'].index("producer:ZJetCorrectionsProducer") + 1, "producer:JetEtaPhiCleaner")
    cfg['JetEtaPhiCleanerFile'] = os.path.join(configtools.getPath(), "data/cleaning/jec17ul/Summer19UL17_V2/hotjets-UL17_v2.root")
    cfg['JetEtaPhiCleanerHistogramNames'] = ["h2hot_ul17_plus_hep17_plus_hbpw89"]
    cfg['JetEtaPhiCleanerHistogramValueMaxValid'] = 9.9   # >=10 means jets should be invalidated

    return cfg
"""

def make():
  runs = ['B','C','D','E','F']
  lheWeightNames = ['nominal','isrDefup','isrDefdown','fsrDefup','fsrDefdown']

  for ch in ["mm", "ee"]:
    _cfg = TEMPLATE.format(
      runs=runs,
      lheWeightNames=lheWeightNames,
      ch=ch,
      input_path=INPUT_TEMPLATE.format(
        userpath='rvoncube/Skimming',
      )
    )
    _fname = "mc17_{ch}_{runs}_DYJets_amcatnlo_JEC.py".format(
      ch=ch,
      runs=''.join(runs),
    )
    with open(_fname, 'w') as _f:
      _f.write(_cfg)

if __name__ == '__main__':
    make()
