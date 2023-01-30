"""
Quick and dirty script to generate config files for all channels, JEC versions, etc,
which can then be edited manually. Note: existing configs with matching names will
be overwritten!
"""

INPUT_TEMPLATE = '"{{}}/{userpath}/ZJet_{pd}_Run2018{run}_UL2018_MiniAODv2-v[0-9]/*.root".format(SE_PATH_PREFIXES["xrootd_gridka_nrg"])'

TEMPLATE = """
import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES

RUN='{run}'
CH='{ch}'
JEC='{{0}}_Run{{1}}_{{2}}'.format(JEC_BASE, RUN, JEC_VERSION)



def config():
    cfg = configtools.getConfig('data', 2018, CH, JEC=JEC, JER=JER)
    cfg["InputFiles"].set_input(
        path={input_path},
    )

    ### general things
    cfg['DebugVerbosity'] = 0
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Collisions18/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt')]


    ### Piplelines and quantities
    cfg['Pipelines']['default']['Quantities'] += [
        'jet1chf',
        'jet1nhf',
        'jet1ef',
        'jet1mf',
        'jet1hfhf',
        'jet1hfemf',
        'jet1pf',
        ]

    cfg['Pipelines']['default']['Quantities'] += [
        'jnpf',
        'rawjnpf',
        'mpflead',
        'rawmpflead',
        'mpfjets',
        'rawmpfjets',
        'mpfunclustered',
        'rawmpfunclustered',
        ]


    ### filters
    # to avoid config problems: from now on we use the nocuts pipeline and apply the filters in correct ordering manually ...
    if CH == 'mm':
        cfg['Pipelines']['default']['Processors'] += [
          "filter:MinNMuonsCut",
          "filter:MaxNMuonsCut",
          "filter:ValidZCut",
          "filter:MuonPtCut",
          "filter:MuonEtaCut",
          "filter:ZPtCut",
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
          "filter:ZPtCut",
          "filter:LeadingJetPtCut",
          "filter:JetEtaPhiCleanerCut",
          "filter:BackToBackCut",
          "filter:JetIDCut",
        ]

    cfg = configtools.expand(cfg, ['nocuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res', 'L1L2L3Res'])


    ## JetEtaPhiCleaner
    cfg['JetEtaPhiCleanerFile'] = os.path.join(configtools.getPath(), 'data/cleaning/jec18ul/Summer19UL18_V1/hotjets-UL18.root')
    cfg['JetEtaPhiCleanerHistogramNames'] = ["h2hot_ul18_plus_hem1516_and_hbp2m1"]
    # cfg['JetEtaPhiCleanerHistogramValueMaxValid'] = 9.9   # >=10 means jets should be invalidated #TODO


    ## METFilters
    cfg['METFilterNames'] = [
        "Flag_goodVertices",
        "Flag_globalSuperTightHalo2016Filter",
        "Flag_HBHENoiseFilter",
        "Flag_HBHENoiseIsoFilter",
        "Flag_EcalDeadCellTriggerPrimitiveFilter",
        "Flag_BadPFMuonFilter",
        "Flag_BadPFMuonFilterUpdateDz",
        "Flag_eeBadScFilter",
        "Flag_ecalBadCalibFilter",
        ]

    ### Manual filters to reduce computing effort 
    # JsonFilter, HltProducer and HltFilter are added in the default config for data to the processors to skip rejected events directly
    cfg['Processors'].insert(cfg['Processors'].index('filter:HltFilter') + 1, 'filter:METFiltersFilter')

    ### Cuts
    cfg['CutBackToBack'] = 0.44
    cfg['ZMassRange'] = 20.0
    cfg['MPFSplittingJetPtMin'] = 15.  # deprecated
    cfg['JNPFJetPtMin'] = 15.  # deprecated
    cfg['CutVetoJetsAbove'] = 10.0  # JetEtaPhiCleaner: only apply on events were leading jet is above 10.0
    cfg['CutVetoNJets'] = 1  # apply eta phi cleaning only on leading jet 
    cfg['ZMassRange'] = 20.0
    cfg['CutZPtMin'] = 15.0  # applied later in postprocessing, only for synchronization

    if CH == 'ee':
        cfg['Processors'].insert(cfg['Processors'].index('producer:ZJetValidElectronsProducer'), 'producer:ElectronCorrectionsProducer',)
        cfg['ApplyElectronEnergyCorrections'] = True
        cfg['ElectronEnergyCorrectionTags'] = ["electronCorrection:ecalTrkEnergyPostCorr"]
        cfg["CutElectronSubPtMin"] = 15.0  # 25 and 15
    elif CH == 'mm':
        cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
        cfg['MuonRochesterCorrectionsFile'] = os.path.join(configtools.getPath(),'../Artus/KappaAnalysis/data/rochcorr/RoccoR2018UL.txt')
        cfg['MuonEnergyCorrection'] = 'rochcorr2018ul'
        cfg["CutMuonSubPtMin"] = 10.0  # 20 and 10

    ### IDs
    cfg['ApplyElectronVID'] = True
    cfg['ElectronVIDName'] = "Fall17-94X-V2"
    cfg['ElectronVIDType'] = "cutbased"
    cfg['ElectronVIDWorkingPoint'] = "tight"
    cfg['MuonID'] = "tight"
    cfg['MuonIso'] = "tight"
    cfg['MuonIsoType'] = "PF"
    cfg['CutJetID'] = 'tightlepveto'  # choose event-based CutJetID (Excalibur) selection, alternatively use JetID (Artus)
    cfg['CutJetIDVersion'] = 'UL2018'  # for event-based JetID
    cfg['CutJetIDFirstNJets'] = 1


    ### Other flags
    cfg['EnableTypeIModification'] = False
    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'
    cfg['ProvideL2ResidualCorrections'] = True
    cfg['OnlyCleanZLeptons'] = True  # lepton cleaning mode
    cfg['ProvideL2L3ResidualCorrections'] = True
    cfg['CutVetoCleanedEvents'] = True
    cfg['JERMethod'] = "hybrid"

    cfg['HltPaths']= {{
        'ee': ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'],
        'mm': ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8']
    }}[CH]

    return cfg
"""

def make():
  for ch in ["mm", "ee"]:
    for run in ['A', 'B', 'C', 'D']:

      _cfg = TEMPLATE.format(
        run=run,
        ch=ch,
        input_path=INPUT_TEMPLATE.format(
          run=run,
          pd='DoubleMuon' if ch == 'mm' else 'EGamma',
          userpath='rhofsaess/Skimming'
        ),
      )
      _fname = "data18_{ch}_{run}_MiniAODv2_JEC.py".format(
        run=run,
        ch=ch,
      )
      with open(_fname, 'w') as _f:
        _f.write(_cfg)

if __name__ == '__main__':
    make()
