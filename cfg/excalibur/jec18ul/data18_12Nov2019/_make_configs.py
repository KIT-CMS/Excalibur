"""
Quick and dirty script to generate config files for all channels, JEC versions, etc,
which can then be edited manually. Note: existing configs with matching names will
be overwritten!
"""

INPUT_TEMPLATE = '"{{}}/{userpath}/ZJet_{pd}_Run2018{run}_12Nov2019_UL2018-{version_suffix}/*.root".format(SE_PATH_PREFIXES["xrootd_gridka_nrg"])'

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
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Collisions18/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt')]

    cfg['Pipelines']['default']['Quantities'] += ['jet1chf', 'jet1nhf', 'jet1ef', 'jet1mf', 'jet1hfhf', 'jet1hfemf', 'jet1pf']
    cfg['Pipelines']['default']['Quantities'] += ['jnpf', 'rawjnpf', 'mpflead', 'rawmpflead', 'mpfjets', 'rawmpfjets', 'mpfunclustered', 'rawmpfunclustered']

    cfg['Pipelines']['default']['Processors'].insert(cfg['Processors'].index('filter:HltFilter') + 1, 'filter:METFiltersFilter')
    cfg['METFilterNames'] = ["Flag_goodVertices", "Flag_globalSuperTightHalo2016Filter", "Flag_HBHENoiseFilter", "Flag_HBHENoiseIsoFilter",
        "Flag_EcalDeadCellTriggerPrimitiveFilter", "Flag_BadPFMuonFilter", "Flag_ecalBadCalibReducedMINIAODFilter"]

    cfg = configtools.expand(cfg, ['basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res'])

    cfg['MPFSplittingJetPtMin'] = 15.
    cfg['JNPFJetPtMin'] = 15.

    cfg['CutBackToBack'] = 0.44

    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    cfg['ProvideL2ResidualCorrections'] = True

    cfg['ApplyElectronVID'] = True
    cfg['ElectronVIDName'] = "Fall17-94X-V2"
    cfg['ElectronVIDType'] = "cutbased"
    cfg['ElectronVIDWorkingPoint'] = "tight"

    if CH == 'ee':
        cfg['Processors'].insert(cfg['Processors'].index('producer:ZJetValidElectronsProducer'), 'producer:ElectronCorrectionsProducer',)
        cfg['ApplyElectronEnergyCorrections'] = True
        cfg['ElectronEnergyCorrectionTags'] = ["electronCorrection:ecalTrkEnergyPostCorr"]
    # TODO: Update to 2018
    # elif CH == 'mm':
    #     cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
    #     cfg['MuonRochesterCorrectionsFile'] = os.path.join(configtools.getPath(),'../Artus/KappaAnalysis/data/rochcorr/RoccoR2017UL.txt')
    #     cfg['MuonEnergyCorrection'] = 'rochcorr2017ul'

    cfg['CutJetID'] = 'tightlepveto'  # choose event-based JetID selection
    cfg['CutJetIDVersion'] = '2018UL'  # for event-based JetID
    cfg['CutJetIDFirstNJets'] = 2

    cfg['EnableTypeIModification'] = False

    cfg['JetEtaPhiCleanerFile'] = os.path.join(configtools.getPath(), 'data/cleaning/jec18ul/Summer19UL18_V1/hotjets-UL18.root')
    cfg['JetEtaPhiCleanerHistogramNames'] = ["h2hot_ul18_plus_hem1516_and_hbp2m1"]

    cfg['HltPaths'] = {{
        'ee': ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'],
        'mm': ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ', 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8']
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
          userpath='mhorzela/Skimming',
          version_suffix='v2' if run != 'D' else ('v3' if ch == 'mm' else 'v4')
        ),
      )
      _fname = "data18_{ch}_{run}_12Nov2019.py".format(
        run=run,
        ch=ch,
      )
      with open(_fname, 'w') as _f:
        _f.write(_cfg)

if __name__ == '__main__':
    make()
