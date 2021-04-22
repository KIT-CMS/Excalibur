import os

import configtools

JEC_BASE = 'Summer19UL16'
JEC_VERSION = 'V5'

# set JER to 'None' to turn JER smearing off
JER = {
    "APV": "Summer20UL16APV_JRV2",
    "nonAPV": "Summer20UL16_JRV2"
    }

SE_PATH_PREFIXES = dict(
    srm_gridka_nrg="srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user",
    # srm_desy_dcache="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user",
    local_gridka_nrg="/storage/gridka-nrg",
    xrootd_gridka_nrg="root://cmsxrootd-redirectors.gridka.de//store/user"
)

def config(ch, run, jec):

    _jsonFiles = []

    if "B" in run:
        _jsonFiles.append("B")
    if "C" in run:
        _jsonFiles.append("C")
    if "D" in run:
        _jsonFiles.append("D")
    if "E" in run:
        _jsonFiles.append("E")
    if "Fearly" in run:
        _jsonFiles.append("F_part1")
    if "Flate" in run:
        _jsonFiles.append("F_part2")
    if "G" in run:
        _jsonFiles.append("G")
    if "H" in run:
        _jsonFiles.append("H")

    if run in "BCDEFearly":
        APV=True
        IOVS = ['BCD', 'EFearly']
        postfix = 'preVFP_v8'
        inputfiles = "{}/dsavoiu/Skimming/ZJet_DYJetsToLL_Summer20-amcatnloFXFX_mcRun2_asymptotic_preVFP_v8/*.root"
    else:
        APV=False
        runs = 'FlateGH'
        IOVS = ['Flate', 'G', 'H']
        postfix = 'v13'
        inputfiles = "{}/dsavoiu/Skimming/ZJet_DYJetsToLL_Summer20-amcatnloFXFX_mcRun2_asymptotic_v13/*.root"

    _jer = JER["APV" if APV else "nonAPV"]
    cfg = configtools.getConfig('mc', 2016, ch, bunchcrossing='25ns', IOV=run, JER=_jer, JEC=jec)

    cfg["InputFiles"].set_input(path=inputfiles.format(SE_PATH_PREFIXES["xrootd_gridka_nrg"]))

    cfg['JsonFiles'] =  [
        os.path.join(configtools.getPath(),'data/json/Collision16/Cert_{}_13TeV_Legacy2016_Collisions16_JSON.txt'.format(_run))
        for _run in _jsonFiles
        ]

    lheWeightNames = ['nominal','isrDefup','isrDefdown','fsrDefup','fsrDefdown']

    cfg['Processors'] += ['producer:ZJetGenWeightProducer']
    cfg['ZJetGenWeightNames'] = lheWeightNames
    cfg['JetEtaPhiCleanerFile'] = os.path.join(configtools.getPath(), "data/cleaning/jec16ul/Summer19UL16_V0/hotjets-UL16.root")
    cfg['JetEtaPhiCleanerHistogramNames'] = ["h2hot_ul16_plus_hbm2_hbp12_qie11", "h2hot_mc"]


    cfg['PileupWeightFile'] = os.path.join(
        configtools.getPath() ,
        'data/pileup/mc_weights/mc16ul_DYJets_amcatnlo/PUWeights_{}_DYJetsToLL_Summer20-amcatnloFXFX_mcRun2_asymptotic_{}.root'.format(run, postfix)
    )

    cfg['Processors'] += ['producer:ZJetPUWeightProducer']
    cfg['ZJetPUWeightFiles'] = [os.path.join(configtools.getPath(), 'data/pileup/mc_weights/mc16ul_DYJets_amcatnlo/PUWeights_{}_DYJetsToLL_Summer20-amcatnloFXFX_mcRun2_asymptotic_{}.root'.format(runperiod, postfix)) for runperiod in IOVS]
    cfg['ZJetPUWeightSuffixes'] = ['{}'.format(runperiod) for runperiod in IOVS]

    cfg['Processors'] += ['producer:ZJetGenWeightProducer']
    cfg['ZJetGenWeightNames'] = ['nominal', 'isrDefup', 'isrDefdown', 'fsrDefup', 'fsrDefdown']

    cfg['Pipelines']['default']['Quantities'] += ['puWeight{}'.format(runperiod) for runperiod in IOVS]
    cfg['Pipelines']['default']['Quantities'] += ['genWeight_{}'.format(lheWeightName) for lheWeightName in lheWeightNames]
    cfg['Pipelines']['default']['Quantities'] += ['jet1chf', 'jet1nhf', 'jet1ef', 'jet1mf', 'jet1hfhf', 'jet1hfemf', 'jet1pf']
    cfg['Pipelines']['default']['Quantities'] += ['jnpf', 'rawjnpf', 'mpflead', 'rawmpflead', 'mpfjets', 'rawmpfjets', 'mpfunclustered', 'rawmpfunclustered']

    cfg = configtools.expand(cfg, ['basiccuts'], ['None', 'L1', 'L1L2L3'])

    cfg['JERMethod'] = "hybrid"  # options: "hybrid" or "stochastic"
    # cfg['ProvideL2ResidualCorrections'] = True
    # cfg['ProvideL2L3ResidualCorrections'] = True

    cfg['MPFSplittingJetPtMin'] = 15.
    cfg['JNPFJetPtMin'] = 15.

    cfg['CutBackToBack'] = 0.44

    cfg['CutJetID'] = 'tightlepveto'  # choose event-based CutJetID (Excalibur) selection, alternatively use JetID (Artus)
    cfg['CutJetIDVersion'] = '2016UL'  # for event-based JetID
    cfg['CutJetIDFirstNJets'] = 2

    cfg['NumberGeneratedEvents'] = 92353657 if APV else 95237235
    cfg['GeneratorWeight'] = 1.0
    # https://cms-gen-dev.cern.ch/xsdb/?columns=67108863&currentPage=0&pageSize=10&searchQuery=DAS%3DDYJetsToLL_M-50_TuneCP5
    cfg['CrossSection'] = 6077.22

    if ch == 'ee':
        cfg['ApplyElectronVID'] = True
        cfg['ElectronVIDName'] = "Fall17-94X-V2"
        cfg['ElectronVIDType'] = "cutbased"
        cfg['ElectronVIDWorkingPoint'] = "tight"
        cfg['HltPaths']= ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ']


    if ch == 'mm':
        cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
        cfg['MuonRochesterCorrectionsFile'] = os.path.join(configtools.getPath(),'../Artus/KappaAnalysis/data/rochcorr/RoccoR2016{}UL.txt'.format('a' if APV else 'b'))
        cfg['MuonEnergyCorrection'] = 'rochcorr2016ul'
        cfg['HltPaths']= ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ']


    return cfg

