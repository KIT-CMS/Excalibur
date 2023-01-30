"""
Quick and dirty script to generate config files for all channels, JEC versions, etc,
which can then be edited manually. Note: existing configs with matching names will
be overwritten!
"""

INPUT_TEMPLATE = '"{{}}/{userpath}/ZJet_DYJetsToLL_Summer20_MiniAODv2-amcatnloFXFX_realistic_v16_L1v1-v2/*.root".format(SE_PATH_PREFIXES["xrootd_gridka_nrg"])'

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

    ### general things
    cfg['DebugVerbosity'] = 0
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Collisions18/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt')]

    ### Piplelines and quantities
    cfg['Pipelines']['default']['Quantities'] += ['puWeight{{}}'.format(runperiod) for runperiod in {runs}]
    cfg['Pipelines']['default']['Quantities'] += ['genWeight_{{}}'.format(lheWeightName) for lheWeightName in {lheWeightNames}]
    cfg['Pipelines']['default']['Quantities'] += ['jet1chf', 'jet1nhf', 'jet1ef', 'jet1mf', 'jet1hfhf', 'jet1hfemf', 'jet1pf']
    cfg['Pipelines']['default']['Quantities'] += ['jnpf', 'rawjnpf', 'mpflead', 'rawmpflead', 'mpfjets', 'rawmpfjets', 'mpfunclustered', 'rawmpfunclustered']

    ### filters
    # to avoid config problems: from now on we use the nocuts pipeline and apply the filters in correct ordering manually ...
    if CH == 'mm':
        cfg['Pipelines']['default']['Processors'] += [
            "filter:MinNMuonsCut",
            "filter:MaxNMuonsCut",
            "filter:ValidZCut",
            "filter:MuonPtCut",
            "filter:MuonEtaCut",
            "filter:LeadingJetPtCut",
            "filter:JetEtaPhiCleanerCut",
            "filter:BackToBackCut",
            "filter:JetIDCut",
        ]
    elif CH == 'ee':
        cfg['Pipelines']['default']['Processors'] += [
            "filter:MinNElectronsCut",
            "filter:MaxNElectronsCut",
            "filter:ValidZCut",
            "filter:ElectronPtCut",
            "filter:ElectronEtaCut",
            "filter:LeadingJetPtCut",
            "filter:JetEtaPhiCleanerCut",
            "filter:BackToBackCut",
            "filter:JetIDCut",
        ]

    cfg = configtools.expand(cfg, ['nocuts'], ['None', 'L1', 'L1L2L3'])

    ### cuts
    cfg['MPFSplittingJetPtMin'] = 15.
    cfg['JNPFJetPtMin'] = 15.
    cfg['CutBackToBack'] = 0.44

    ### other flags
    cfg['JERMethod'] = 'hybrid'
    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'
    cfg['ApplyElectronVID'] = True
    cfg['ElectronVIDName'] = "Fall17-94X-V2"
    cfg['ElectronVIDType'] = "cutbased"
    cfg['ElectronVIDWorkingPoint'] = "tight"
    cfg['EnableTypeIModification'] = False

    ### weights
    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/mc_weights/mc18ul_DYJets_amcatnlo/PUWeights_' + ''.join({runs}) + '_DYJetsToLL_Summer20-amcatnlo_realistic_v16_L1v1-v2.root')
    cfg['NumberGeneratedEvents'] = 104017741
    cfg['GeneratorWeight'] = 1.0
    cfg['CrossSection'] = 6529.0  # from XSDB: https://cms-gen-dev.cern.ch/xsdb/?searchQuery=DAS=DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8
    cfg['Processors'] += ['producer:ZJetPUWeightProducer']
    cfg['ZJetPUWeightFiles'] = [os.path.join(configtools.getPath() ,'data/pileup/mc_weights/mc18ul_DYJets_amcatnlo/PUWeights_{{}}_DYJetsToLL_Summer20-amcatnlo_realistic_v16_L1v1-v2.root'.format(runperiod)) for runperiod in {runs}]
    cfg['ZJetPUWeightSuffixes'] = ['{{}}'.format(runperiod) for runperiod in {runs}]
    cfg['Processors'] += ['producer:ZJetGenWeightProducer']
    cfg['ZJetGenWeightNames'] = {lheWeightNames}

    ### ee | mm
    if CH == 'ee':
        cfg['Processors'].insert(cfg['Processors'].index('producer:ZJetValidElectronsProducer'), 'producer:ElectronCorrectionsProducer',)
        cfg['ApplyElectronEnergyCorrections'] = True
        cfg['ElectronEnergyCorrectionTags'] = ["electronCorrection:ecalTrkEnergyPostCorr"]
        cfg["CutElectronSubPtMin"] = 15.0
        cfg['HltPaths']=['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL']
    elif CH == 'mm':
        cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
        cfg['MuonRochesterCorrectionsFile'] = os.path.join(configtools.getPath(),'../Artus/KappaAnalysis/data/rochcorr/RoccoR2018UL.txt')
        cfg['MuonEnergyCorrection'] = 'rochcorr2018ul'
        cfg["CutMuonSubPtMin"] = 10.0
        cfg['HltPaths']=['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8']

    ### IDs
    cfg['CutJetID'] = 'tightlepveto'  # choose event-based CutJetID (Excalibur) selection, alternatively use JetID (Artus)
    cfg['CutJetIDVersion'] = '2018UL'  # for event-based JetID
    cfg['CutJetIDFirstNJets'] = 1

    ### JetEtaPhi Cleaner
    cfg['Processors'].insert(cfg['Processors'].index("producer:ZJetCorrectionsProducer") + 1, "producer:JetEtaPhiCleaner")
    cfg['JetEtaPhiCleanerFile'] = os.path.join(configtools.getPath(), "data/cleaning/jec18ul/Summer19UL18_V1/hotjets-UL18.root")
    cfg['JetEtaPhiCleanerHistogramNames'] = ["h2hot_ul18_plus_hem1516_and_hbp2m1"]
    cfg['JetEtaPhiCleanerHistogramValueMaxValid'] = 9.9   # >=10 means jets should be invalidated

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
        userpath='rhofsaess/Skimming',
      )
    )
    _fname = "mc18_{ch}_{runs}_DYJets_amcatnlo_JEC.py".format(
      ch=ch,
      runs=''.join(runs),
    )
    with open(_fname, 'w') as _f:
      _f.write(_cfg)

if __name__ == '__main__':
    make()
