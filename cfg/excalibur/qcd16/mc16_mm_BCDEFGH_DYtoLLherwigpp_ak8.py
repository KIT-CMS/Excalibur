import configtools
import os

JEC = 'Summer16_07Aug2017_V11'

def config():
    cfg = configtools.getConfig('mc', 2016, 'mm', JEC=JEC)
    cfg["InputFiles"].set_input(
        path="root://cmsxrootd-redirectors.gridka.de//store/user/tberger/Skimming_94X/DYJetsToLL_madgraphMLM-herwigpp_RunIISummer16/*.root",
        )
    cfg = configtools.expand(cfg, 
                                ['nocuts','zjetcuts','genzjetcuts'],
                                ['None','L1L2L3'])
    configtools.remove_quantities(cfg, [
        'jet1area','jet1l1', 'jet1rc', 'jet1l2','jet1ptraw', 'jet1ptl1',
        #'jet2pt', 'jet2eta', 'jet2y', 'jet2phi',
        #'jet3pt', 'jet3eta', 'jet3y', 'jet3phi',
        'mpf', 'rawmpf', 'met', 'metphi', 'rawmet', 'rawmetphi', 'sumet','mettype1vecpt', 'mettype1pt',
        #'genjet2pt','genjet2eta','genjet2y','genjet2phi',
        #'genjet3pt','genjet3eta','genjet3y','genjet3phi',
        ])
##### Add Producers: #####
    cfg['Processors'] = ['producer:MuonTriggerMatchingProducer',] + cfg['Processors']
    cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
    cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:PFCandidatesProducer',)
    cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer')+1, 'producer:ZJetDressedMuonsProducer',)
    cfg['Processors'].insert(cfg['Processors'].index('producer:GenZmmProducer'), 'producer:ZJetGenPhotonsProducer',)
    cfg['Processors'].insert(cfg['Processors'].index('producer:GenZmmProducer'), 'producer:ZJetDressedGenMuonsProducer',)
    #cfg['Processors'].insert(cfg['Processors'].index('producer:GenZmmProducer'), 'producer:ZJetTrueGenMuonsProducer',)
##### Specify input sources for Jets & Muons: #####
    cfg['PackedPFCandidates'] = 'pfCandidates'
    cfg['MaxZJetDressedMuonDeltaR'] = 0.1
    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'
    cfg['ValidMuonsInput'] = "corrected"
    cfg['GenJets'] = 'ak8GenJetsNoNu'
    cfg['TaggedJets'] = 'ak8PFJetsCHS'
    cfg['UseObjectJetYCut'] = True
    cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/Summer16_07Aug2017_V11_MC/Summer16_07Aug2017_V11_MC')
    cfg['JetID'] = 'loose'
    cfg['PUJetID'] = 'none'
    cfg['DeltaRMatchingRecoJetGenJet'] = 0.4
##### Change selection: (see also http://cms.cern.ch/iCMS/analysisadmin/cadilines?line=SMP-17-002&tp=an&id=1891&ancode=SMP-17-002) #####
    cfg['MuonIso'] = 'loose_2016'
    cfg['MuonID'] = 'tight'
    cfg['CutMuonPtMin'] = 25.0
    cfg['CutMuonEtaMax'] = 2.4
    cfg['ZMassRange'] = 20.0
    cfg['CutLeadingJetPtMin'] = 10.0
    cfg['MinPUJetID'] = -9999
    cfg['HltPaths'] = ['HLT_IsoMu24', 'HLT_IsoTkMu24']
    cfg["MuonTriggerFilterNames"] = ['HLT_IsoMu24_v2:hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09','HLT_IsoTkMu24_v3:hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09']
##### MC specific properties: #####
    cfg['NumberGeneratedEvents'] = 19554896
    cfg['GeneratorWeight'] = 1.0
    cfg['CrossSection'] = 358.6
    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/PUWeights_BCDEFGH_13TeV_23Sep2016ReReco_DYJetsToLL_M-50_madgraphMLM-herwigpp_RunIISummer16.root')
    return cfg
