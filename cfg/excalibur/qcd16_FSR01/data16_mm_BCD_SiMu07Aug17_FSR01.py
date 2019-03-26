import configtools
import os

#cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/Summer16_07Aug2017BCD_V11_DATA/Summer16_07Aug2017BCD_V11_DATA')
RUN = 'BCD'
JEC = 'Summer16_07Aug2017'+RUN+'_V11'

def config():
    cfg = configtools.getConfig('data', 2016, 'mm', JEC=JEC, IOV=RUN)
    cfg["InputFiles"].set_input(
        #bmspath='/storage/gridka-nrg/tberger/Skimming/ZJet_SingleMuon_Run2016D-07Aug17-v1/*.root',
        bmspathB1='root://cmsxrootd-redirectors.gridka.de//store/user/tberger/Skimming/SingleMuon_Run2016B-07Aug17_ver1-v1/*.root',
        bmspathB2='root://cmsxrootd-redirectors.gridka.de//store/user/tberger/Skimming/SingleMuon_Run2016B-07Aug17_ver2-v1/*.root',
        bmspathC ='root://cmsxrootd-redirectors.gridka.de//store/user/tberger/Skimming/SingleMuon_Run2016C-07Aug17-v1/*.root',
        bmspathD ='root://cmsxrootd-redirectors.gridka.de//store/user/tberger/Skimming/SingleMuon_Run2016D-07Aug17-v1/*.root',
        nafpathB1='root://cmsxrootd-redirectors.gridka.de//store/user/tberger/Skimming/SingleMuon_Run2016B-07Aug17_ver1-v1/*.root',
        nafpathB2='root://cmsxrootd-redirectors.gridka.de//store/user/tberger/Skimming/SingleMuon_Run2016B-07Aug17_ver2-v1/*.root',
        nafpathC ='root://cmsxrootd-redirectors.gridka.de//store/user/tberger/Skimming/SingleMuon_Run2016C-07Aug17-v1/*.root',
        nafpathD ='root://cmsxrootd-redirectors.gridka.de//store/user/tberger/Skimming/SingleMuon_Run2016D-07Aug17-v1/*.root',
        #nafpath='/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/testfiles/ZJet_SingleMuon_Run2016D-Legacy-07Aug2017-v1_testfile.root',
    )
    cfg = configtools.expand(cfg, 
                                ['nocuts','zjetcuts'],
                                ['None','L1L2L3Res'],)
    configtools.remove_quantities(cfg, [
        'jet1area','jet1l1', 'jet1rc', 'jet1l2','jet1ptraw', 'jet1ptl1','jet1ptl1l2l3', 'jet1res',
        #'jet2pt', 'jet2eta', 'jet2y', 'jet2phi',
        #'jet3pt', 'jet3eta', 'jet3y', 'jet3phi',
        'mpf', 'rawmpf', 'met', 'metphi', 'rawmet', 'rawmetphi', 'sumet','mettype1vecpt', 'mettype1pt',
        ])
    configtools.add_quantities(cfg, [   #'mu1IDSFWeight','mu1IsoSFWeight','mu1TrackingSFWeight','mu1TriggerSFWeight',
                                        #'mu2IDSFWeight','mu2IsoSFWeight','mu2TrackingSFWeight','mu2TriggerSFWeight',
                                        'leptonIDSFWeight','leptonIDSFWeightUp','leptonIDSFWeightDown',
                                        'leptonIsoSFWeight','leptonIsoSFWeightUp','leptonIsoSFWeightDown',
                                        #'leptonTrackingSFWeight','leptonTrackingSFWeightUp','leptonTrackingSFWeightDown',
                                        'leptonTriggerSFWeight','leptonTriggerSFWeightUp','leptonTriggerSFWeightDown',
                                        ])
##### Add Producers: #####
    cfg['Processors'] = [  'producer:MuonTriggerMatchingProducer',
                            ] + cfg['Processors']
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
    cfg['LeptonSFVariation'] = True
    cfg['LeptonIDSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/ID_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonIsoSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Iso_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonTriggerSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Trigger_EfficienciesAndSF_BCDEF.root")
    #cfg['LeptonTrackingSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Tracking_EfficienciesAndSF_BCDEFGH.root")
##### Json & JEC #####
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(),'data/json/Cert_BCD_13TeV_23Sep2016ReReco_Collisions16_JSON.txt')]
    return cfg
