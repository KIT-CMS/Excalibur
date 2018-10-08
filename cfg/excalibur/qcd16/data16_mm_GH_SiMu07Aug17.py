import configtools
import os

#cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/Summer16_07Aug2017GH_V11_DATA/Summer16_07Aug2017GH_V11_DATA')
RUN = 'GH'
JEC = 'Summer16_07Aug2017'+RUN+'_V11'

def config():
    cfg = configtools.getConfig('data', 2016, 'mm', JEC=JEC, IOV=RUN)
    cfg["InputFiles"].set_input(
        #ekppath='/storage/c/tberger/testfiles/skimming_output/data/ZJet_SingleMuon_Run2016D-Legacy-07Aug2017-v1_testfile.root',
        bmspathF ='root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016F-07Aug17-v1/*.root',
        bmspathG ='root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016G-07Aug17-v1/*.root',
        bmspathH ='root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016H-07Aug17-v1/*.root',
        nafpathF ='root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016F-07Aug17-v1/*.root',
        nafpathG ='root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016G-07Aug17-v1/*.root',
        nafpathH ='root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016H-07Aug17-v1/*.root',
        #nafpath='/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/testfiles/ZJet_SingleMuon_Run2016G-Legacy-07Aug2017-v1_testfile.root',
    )
    cfg = configtools.expand(cfg, 
                                ['nocuts','zjetcuts'],
                                ['None','L1L2L3Res'],
                                False)
    configtools.remove_quantities(cfg, [
        'jet1rc','npv', 'rho','njets', 'njetsinv', 'njets30','njets10',
        'jet1chf', 'jet1nhf', 'jet1ef','jet1mf', 'jet1hfhf', 'jet1hfemf', 'jet1pf','jet1area',
        'jet1l1', 'jet1l2','jet1ptraw', 'jet1ptl1', 
        'jet2pt', 'jet2eta', 'jet2y', 'jet2phi','jet3pt', 'jet3eta', 'jet3y', 'jet3phi',
        'mpf', 'rawmpf', 'met', 'metphi', 'rawmet', 'rawmetphi', 'sumet', 'mettype1vecpt', 'mettype1pt',
        'jetHT','jetrecoilpt', 'jetrecoilphi', 'jetrecoileta', 'jetrpf',
        'jet1idtightlepveto', 'jet1idtight', 'jet1idloose','jet2idtightlepveto', 'jet2idtight', 'jet2idloose','jet3idtightlepveto', 'jet3idtight', 'jet3idloose',
        'mu1iso', 'mu1sumchpt', 'mu1sumnhet', 'mu1sumpet', 'mu1sumpupt',
        'mu1idloose','mu1idmedium','mu1idtight',
        'mu2idloose','mu2idmedium','mu2idtight',
        ])
    configtools.add_quantities(cfg, [   #'mu1IDSFWeight','mu1IsoSFWeight','mu1TrackingSFWeight','mu1TriggerSFWeight',
                                        #'mu2IDSFWeight','mu2IsoSFWeight','mu2TrackingSFWeight','mu2TriggerSFWeight',
                                        'leptonIDSFWeight','leptonIsoSFWeight','leptonTrackingSFWeight','leptonTriggerSFWeight',     
                                        #'jet1puidraw',
                                        ])
##### Add Producers: #####
    cfg['Processors'] = [  'producer:MuonTriggerMatchingProducer',
                            ] + cfg['Processors']
    cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
    #cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:PFCandidatesProducer',)
    #cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer')+1, 'producer:ZJetDressedMuonsProducer',)
##### Specify input sources for Jets & Muons: #####
    #cfg['PackedPFCandidates'] = 'pfCandidates'
    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'
    cfg['ValidMuonsInput'] = "corrected"
    cfg['UseObjectJetYCut'] = True
    cfg['TaggedJets'] = 'ak4PFJetsCHS'
    cfg['JetID'] = 'loose'
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
    cfg['LeptonIDSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/ID_EfficienciesAndSF_GH.root")
    cfg['LeptonIsoSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Iso_EfficienciesAndSF_GH.root")
    cfg['LeptonTriggerSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Trigger_EfficienciesAndSF_GH.root")
    cfg['LeptonTrackingSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Tracking_EfficienciesAndSF_BCDEFGH.root")
##### Json & JEC #####
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(),'data/json/Cert_GH_13TeV_23Sep2016ReReco_Collisions16_JSON.txt')]
    return cfg
