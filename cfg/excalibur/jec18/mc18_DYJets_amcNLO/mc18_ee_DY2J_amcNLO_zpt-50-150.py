import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES

CH='ee'
JEC='{}_{}'.format(JEC_BASE, JEC_VERSION)


def config():
    cfg = configtools.getConfig('mc', 2018, CH, JEC=JEC, JER=JER)
    cfg["InputFiles"].set_input(
        path1="{}/cheideck/Skimming/ZJet_DY2JetsToLL_Autumn18_LHEZpT_50-150_amcnloFXFX-pythia8_upgrade2018_realistic_v15-v1/*.root".format(SE_PATH_PREFIXES['xrootd_gridka_nrg']),
    )

    cfg = configtools.expand(cfg, ['basiccuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])

    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/mc_weights/mc18_DYJets_madgraph/PUWeights_ABCD_17Sep2018_DY1JetsToLL_Autumn18-madgraphMLM_realistic_v15-v2.root')

    cfg['NumberGeneratedEvents'] = 24255781  # originally: 24323940, one miniAOD file is missing, was not available!
    cfg['GeneratorWeight'] = 0.305609578187
    cfg['CrossSection'] = 169.6  # from XSDB: https://cms-gen-dev.cern.ch/xsdb/?searchQuery=DAS=DY2JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8

    cfg['VertexSummary'] = 'goodOfflinePrimaryVerticesSummary'

    # for testing JetID differences
    cfg['JetIDVersion'] = 2018  # for object-based JetID
    cfg['CutJetIDVersion'] = 2018  # for event-based JetID

    cfg['PUJetIDModuleName'] = 'pileupJetId'

    return cfg

# python getGeneratorWeight.py -n NONE /storage/gridka-nrg/cheideck/Skimming/ZJet_DY2JetsToLL_Autumn18_LHEZpT_50-150_amcnloFXFX-pythia8_upgrade2018_realistic_v15-v1/*.root
# ...processing file 0 (nickname: *)
#         weighted entries =  1342.0
#         entries =  4650.0
# ...processing file 100 (nickname: *)
#         weighted entries =  1591523.0
#         entries =  5210053.0
# ...processing file 200 (nickname: *)
#         weighted entries =  3268985.0
#         entries =  10693507.0
# ...processing file 300 (nickname: *)
#         weighted entries =  4907927.0
#         entries =  16068249.0
# ...processing file 400 (nickname: *)
#         weighted entries =  6201751.0
#         entries =  20298963.0
#         n_events_generated: 24255781
#         generatorWeight: 0.305609578187
# }

