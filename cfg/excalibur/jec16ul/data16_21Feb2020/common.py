import os

import configtools

JEC_BASE = 'Summer19UL16'
JEC_VERSION = 'V7'

JER = 'Summer20UL16_JRV3'  # set this to 'None' to turn JER smearing off

SE_PATH_PREFIXES = dict(
    srm_gridka_nrg="srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user",
    # srm_desy_dcache="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user",
    local_gridka_nrg="/storage/gridka-nrg",
    xrootd_gridka_nrg="root://cmsxrootd-redirectors.gridka.de//store/user"
)

def config(ch, run, jec):
    cfg = configtools.getConfig('data', 2016, ch, JEC=jec, IOV=run)

    _inputRuns = []
    _jsonFiles = []

    APV = run in "BCDEFearly"

    if "B" in run:
        _inputRuns.append("B_ver1")
        _inputRuns.append("B_ver2")
        _jsonFiles.append("B")
    if "C" in run:
        _inputRuns.append("C")
        _jsonFiles.append("C")
    if "D" in run:
        _inputRuns.append("D")
        _jsonFiles.append("D")
    if "E" in run:
        _inputRuns.append("E")
        _jsonFiles.append("E")
    if "Fearly" in run:
        _inputRuns.append("F_part1")
        _jsonFiles.append("Fearly")
    if "Flate" in run:
        _inputRuns.append("F_part2")
        _jsonFiles.append("Flate")
    if "G" in run:
        _inputRuns.append("G")
        _jsonFiles.append("G")
    if "H" in run:
        _inputRuns.append("H")
        _jsonFiles.append("H")

    cfg["InputFiles"].set_input(**{
        'path'+_run: "{}/rvoncube/Skimming/ZJet_{}_Run2016{}_21Feb2020_UL2016/*.root".format(
            SE_PATH_PREFIXES['xrootd_gridka_nrg'],
            {'ee': 'DoubleEG', 'mm': 'DoubleMuon'}[ch],
            _run
        ) for _run in _inputRuns}
    )

    cfg['JsonFiles'] =  [
        os.path.join(configtools.getPath(),'data/json/Collisions16/Cert_{}_13TeV_Legacy2016_Collisions16_JSON.txt'.format(
            ''.join(_jsonFiles)))
        ]

    # cfg['Processors'].insert(cfg['Processors'].index("producer:ZJetCorrectionsProducer") + 1, "producer:JetEtaPhiCleaner")
    # cfg['NPUFile'] = os.path.join(configtools.getPath(),'data/pileup/pumean_data2016_13TeV.txt')
    cfg['JetEtaPhiCleanerFile'] = os.path.join(configtools.getPath(), "data/cleaning/jec16ul/Summer19UL16_V0/hotjets-UL16.root")
    cfg['JetEtaPhiCleanerHistogramNames'] = ["h2hot_ul16_plus_hbm2_hbp12_qie11", "h2hot_mc"]

    cfg['CutJetID'] = 'tightlepveto'  # choose event-based CutJetID (Excalibur) selection, alternatively use JetID (Artus)
    cfg['CutJetIDVersion'] = 'UL2016'  # for event-based JetID
    cfg['CutJetIDFirstNJets'] = 1

    cfg['ApplyElectronVID'] = True
    cfg['ElectronVIDName'] = "Fall17-94X-V2"
    cfg['ElectronVIDType'] = "cutbased"
    cfg['ElectronVIDWorkingPoint'] = "tight"

    print cfg['Pipelines']
    cfg['Pipelines']['default']['Quantities'] += ['jet1chf', 'jet1nhf', 'jet1ef', 'jet1mf', 'jet1hfhf', 'jet1hfemf', 'jet1pf']
    cfg['Pipelines']['default']['Quantities'] += ['jnpf', 'rawjnpf', 'mpflead', 'rawmpflead', 'mpfjets', 'rawmpfjets', 'mpfunclustered', 'rawmpfunclustered']

    cfg['Pipelines']['default']['Processors'].insert(cfg['Processors'].index('filter:HltFilter') + 1, 'filter:METFiltersFilter')
    cfg['METFilterNames'] = ["Flag_goodVertices", "Flag_globalSuperTightHalo2016Filter", "Flag_HBHENoiseFilter", "Flag_HBHENoiseIsoFilter",
        "Flag_EcalDeadCellTriggerPrimitiveFilter", "Flag_BadPFMuonFilter"]


    cfg['CutBackToBack'] = 0.44

    cfg['MPFSplittingJetPtMin'] = 15.
    cfg['JNPFJetPtMin'] = 15.

    cfg['ProvideL2ResidualCorrections'] = True
    cfg['EnableTypeIModification'] = False

    # cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'  # above skims do not contain 'goodOfflinePrimaryVerticesSummary'
    cfg['ProvideL2ResidualCorrections'] = True
    cfg['ProvideL2L3ResidualCorrections'] = True

    cfg = configtools.expand(cfg, ['basiccuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2Res', 'L1L2L3Res'])

    cfg['JERMethod'] = "hybrid"  # options: "hybrid" or "stochastic"

    if ch == 'ee':
        cfg['Processors'].insert(cfg['Processors'].index('producer:ZJetValidElectronsProducer'), 'producer:ElectronCorrectionsProducer',)
        cfg['ApplyElectronEnergyCorrections'] = True
        cfg['ElectronEnergyCorrectionTags'] = ["electronCorrection:ecalTrkEnergyPostCorr"]
        cfg['HltPaths']= ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ']
        cfg["CutElectronSubPtMin"] = 15.0


    if ch == 'mm':
        cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
        cfg['MuonRochesterCorrectionsFile'] = os.path.join(configtools.getPath(),'../Artus/KappaAnalysis/data/rochcorr/RoccoR2016{}UL.txt'.format('a' if APV else 'b'))
        cfg['MuonEnergyCorrection'] = 'rochcorr2016ul'
        cfg['HltPaths']= ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ']
        cfg["CutMuonSubPtMin"] = 10.0


    return cfg
