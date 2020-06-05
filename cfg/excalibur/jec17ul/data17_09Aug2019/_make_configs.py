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

    cfg['CutJetID'] = 'tightlepveto'  # choose event-based JetID selection
    cfg['CutJetIDVersion'] = 'UL2017'  # for event-based JetID
    cfg['CutJetIDFirstNJets'] = 2

    cfg['EnableTypeIModification'] = False
    
    cfg['JetEtaPhiCleanerFile'] = os.path.join(configtools.getPath(), "data/cleaning/jec17ul/Summer19UL17_V1/hotjets-UL17.root")
    cfg['JetEtaPhiCleanerHistogramNames'] = ["h2hot_ul17_plus_hep17"]

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
