import configtools
import os

RUN = 'EF'
JEC = 'Summer16_07Aug2017'+RUN+'_V11'

def config():
    cfg = configtools.getConfig('data', 2016, 'mm', JEC=JEC, IOV=RUN)
    cfg["InputFiles"].set_input(
        pathE ='root://cmsxrootd-redirectors.gridka.de//store/user/tberger/Skimming_94X/SingleMuon_Run2016E-17Jul2018-v1/*.root',
        pathF ='root://cmsxrootd-redirectors.gridka.de//store/user/tberger/Skimming_94X/SingleMuon_Run2016F-17Jul2018-v1/*.root',
    )
    cfg = configtools.expand(cfg, 
                                ['nocuts','zjetcuts'],
                                ['None','L1L2L3Res'])
    configtools.remove_quantities(cfg, [
        'jet1area','jet1l1', 'jet1rc', 'jet1l2','jet1ptraw', 'jet1ptl1','jet1ptl1l2l3', 'jet1res',
        #'jet2pt', 'jet2eta', 'jet2y', 'jet2phi',
        #'jet3pt', 'jet3eta', 'jet3y', 'jet3phi',
        'mpf', 'rawmpf', 'met', 'metphi', 'rawmet', 'rawmetphi', 'sumet','mettype1vecpt', 'mettype1pt',
        ])
    configtools.add_quantities(cfg, ['lepton'+x+'SFWeight'+y for x in ['ID','Iso','Trigger'] for y in ['Up','Down']])
##### Add Producers: #####
    cfg['Processors'].remove("producer:JetEtaPhiCleaner")
    cfg['Processors'] = ['producer:MuonTriggerMatchingProducer'] + cfg['Processors']
    cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
    cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:PFCandidatesProducer',)
    cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer')+1, 'producer:ZJetDressedMuonsProducer',)
##### Specify input sources for Jets & Muons: #####
    cfg['PackedPFCandidates'] = 'pfCandidates'
    cfg['MaxZJetDressedMuonDeltaR'] = 0.1
    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'
    cfg['ValidMuonsInput'] = "corrected"
    cfg['UseObjectJetYCut'] = True
    cfg['TaggedJets'] = 'ak4PFJetsCHS'
    cfg['ProvideJECUncertainties'] = True
    cfg['JetEnergyCorrectionUncertaintyShift'] = 1
    cfg['JetID'] = 'loose'
    cfg['PUJetID'] = 'medium'
##### Change selection: (see also http://cms.cern.ch/iCMS/analysisadmin/cadilines?line=SMP-17-002&tp=an&id=1891&ancode=SMP-17-002) #####
    cfg['MuonIso'] = 'loose_2016'
    cfg['MuonID'] = 'tight'
    cfg['CutMuonPtMin'] = 25.0
    cfg['CutMuonEtaMax'] = 2.4
    cfg['ZMassRange'] = 20.0
    cfg['CutLeadingJetPtMin'] = 10.0
    cfg['MinPUJetID'] = -0.2
    cfg['HltPaths'] = ['HLT_IsoMu24', 'HLT_IsoTkMu24']
    cfg["MuonTriggerFilterNames"] = ['HLT_IsoMu24_v2:hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09','HLT_IsoTkMu24_v3:hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09']
##### LeptonSF files: #####
    cfg['LeptonSFVariation'] = True
    cfg['LeptonIDSFRootfile']      = os.path.join(configtools.getPath(),"data/scalefactors/2016/RunBCDEF_SF_ID.root")
    cfg['LeptonIsoSFRootfile']     = os.path.join(configtools.getPath(),"data/scalefactors/2016/RunBCDEF_SF_ISO.root")
    cfg['LeptonTriggerSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016/RunBCDEF_SF_Trigger.root")
##### Json & JEC #####
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(),'data/json/Cert_EF_13TeV_23Sep2016ReReco_Collisions16_JSON.txt')]
    return cfg
