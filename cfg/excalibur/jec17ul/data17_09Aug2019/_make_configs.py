"""
Quick and dirty script to generate config files for all channels, JEC versions, etc,
which can then be edited manually. Note: existing configs with matching names will
be overwritten!
"""

INPUT_TEMPLATE = '"{{}}/{userpath}/ZJet_{pd}_Run2017{run}_09Aug2019_UL2017-v1/*.root".format(SE_PATH_PREFIXES["xrootd_gridka_nrg"])'

TEMPLATE = """
import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES

RUN='{run}'
CH='{ch}'
#JEC='{{0}}_Run{{1}}_{{2}}_{jecv_suffix}'.format(JEC_BASE, RUN, JEC_VERSION)
JEC='{{0}}_Run{{1}}_{{2}}'.format(JEC_BASE, RUN, JEC_VERSION)



def config():
    cfg = configtools.getConfig('data', 2017, CH, JEC=JEC, JER=JER)
    cfg["InputFiles"].set_input(
        path={input_path},
    )
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Collisions17/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt')]

    cfg['Pipelines']['default']['Quantities'] += ['jet1chf', 'jet1nhf', 'jet1ef', 'jet1mf', 'jet1hfhf', 'jet1hfemf', 'jet1pf']
    cfg['Pipelines']['default']['Quantities'] += ['jnpf', 'rawjnpf', 'mpflead', 'rawmpflead', 'mpfjets', 'rawmpfjets', 'mpfunclustered', 'rawmpfunclustered']

    cfg['Pipelines']['default']['Processors'].insert(cfg['Processors'].index('filter:HltFilter') + 1, 'filter:METFiltersFilter')
    cfg['METFilterNames'] = ["Flag_goodVertices", "Flag_globalSuperTightHalo2016Filter", "Flag_HBHENoiseFilter", "Flag_HBHENoiseIsoFilter",
        "Flag_EcalDeadCellTriggerPrimitiveFilter", "Flag_BadPFMuonFilter", "Flag_ecalBadCalibReducedMINIAODFilter"]

    cfg = configtools.expand(cfg, ['basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res', 'L1L2L3Res'])

    cfg['CutBackToBack'] = 0.44

    cfg['MPFSplittingJetPtMin'] = 15.
    cfg['JNPFJetPtMin'] = 15.

    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'

    cfg['ProvideL2ResidualCorrections'] = True

    cfg['ApplyElectronVID'] = True
    cfg['ElectronVIDName'] = "Fall17-94X-V2"
    cfg['ElectronVIDType'] = "cutbased"
    cfg['ElectronVIDWorkingPoint'] = "tight"

    {comment_ee}cfg['Processors'].insert(cfg['Processors'].index('producer:ZJetValidElectronsProducer'), 'producer:ElectronCorrectionsProducer',)
    {comment_ee}cfg['ApplyElectronEnergyCorrections'] = True
    {comment_ee}cfg['ElectronEnergyCorrectionTags'] = ["electronCorrection:ecalTrkEnergyPostCorr"]

    cfg['CutJetID'] = 'tightlepveto'  # choose event-based CutJetID (Excalibur) selection, alternatively use JetID (Artus)
    cfg['CutJetIDVersion'] = 'UL2017'  # for event-based JetID
    cfg['CutJetIDFirstNJets'] = 2

    {comment_mm}cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
    {comment_mm}cfg['MuonRochesterCorrectionsFile'] = os.path.join(configtools.getPath(),'../Artus/KappaAnalysis/data/rochcorr/RoccoR2017UL.txt')
    {comment_mm}cfg['MuonEnergyCorrection'] = 'rochcorr2017ul'

    cfg['EnableTypeIModification'] = False

    cfg['Processors'].insert(cfg['Processors'].index("producer:ZJetCorrectionsProducer") + 1, "producer:JetEtaPhiCleaner")
    cfg['JetEtaPhiCleanerFile'] = os.path.join(configtools.getPath(), "data/cleaning/jec17ul/Summer19UL17_V2/hotjets-UL17_v2.root")
    cfg['JetEtaPhiCleanerHistogramNames'] = ["h2hot_ul17_plus_hep17_plus_hbpw89"]
    cfg['JetEtaPhiCleanerHistogramValueMaxValid'] = 9.9   # >=10 means jets should be invalidated

    return cfg
"""

def make():
    for jecv_suffix in ['SimpleL1']:
      for ch in ["mm", "ee"]:
        for run in ['B', 'C', 'D', 'E', 'F']:

          _cfg = TEMPLATE.format(
            run=run,
            jecv_suffix=jecv_suffix,
            ch=ch,
            input_path=INPUT_TEMPLATE.format(
              run=run,
              pd='DoubleMuon' if ch == 'mm' else 'DoubleEG',
              userpath='mhorzela/Skimming',
            ),
            comment_mm='' if ch == 'mm' else '#',
            comment_ee='' if ch == 'ee' else '#',
          )
          _fname = "data17_{ch}_{run}_09Aug2019_JEC{jecv_suffix}.py".format(
            run=run,
            jecv_suffix=jecv_suffix,
            ch=ch,
          )
          with open(_fname, 'w') as _f:
            _f.write(_cfg)

if __name__ == '__main__':
    make()
