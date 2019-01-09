import configtools
import os

JEC = 'Summer16_07Aug2017_V11'

def config():
    cfg = configtools.getConfig('mc', 2016, 'mm', JEC=JEC)
    cfg["InputFiles"].set_input(
        bmspathtW="root://cmsxrootd-redirectors.gridka.de//store/user/tberger/Skimming/ZJet_ST_tW_top_inclusiveDecays_13TeV-powheg-pythia8_RunIISummer16/*.root",
        bmspathtbarW="root://cmsxrootd-redirectors.gridka.de//store/user/tberger/Skimming/ZJet_ST_tW_antitop_inclusiveDecays_13TeV-powheg-pythia8_RunIISummer16/*.root",
        #bmspaths="root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_ST_s-channel_inclusiveDecays_13TeV-amcatnlo-pythia8_RunIISummer16_noJTB/*.root",
        #bmspathtt="root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_ST_t-channel_top_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_RunIISummer16_noJTB/*.root",
        #bmspathttbar="root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_ST_t-channel_antitop_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_RunIISummer16_noJTB/*.root",
        nafpathtW="root://cmsxrootd-redirectors.gridka.de//store/user/tberger/Skimming/ZJet_ST_tW_top_inclusiveDecays_13TeV-powheg-pythia8_RunIISummer16/*.root",
        nafpathtbarW="root://cmsxrootd-redirectors.gridka.de//store/user/tberger/Skimming/ZJet_ST_tW_antitop_inclusiveDecays_13TeV-powheg-pythia8_RunIISummer16/*.root",
        #nafpaths="root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_ST_s-channel_inclusiveDecays_13TeV-amcatnlo-pythia8_RunIISummer16_noJTB/*.root",
        #nafpathtt="root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_ST_t-channel_top_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_RunIISummer16_noJTB/*.root",
        #nafpathttbar="root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_ST_t-channel_antitop_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_RunIISummer16_noJTB/*.root",
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
        'jet1flavor','matchedgenparton1pt','matchedgenparton2pt',
        ])
    configtools.add_quantities(cfg, [   #'mu1IDSFWeight','mu1IsoSFWeight','mu1TrackingSFWeight','mu1TriggerSFWeight',
                                        #'mu2IDSFWeight','mu2IsoSFWeight','mu2TrackingSFWeight','mu2TriggerSFWeight',
                                        'leptonIDSFWeight','leptonIDSFWeightUp','leptonIDSFWeightDown',
                                        'leptonIsoSFWeight','leptonIsoSFWeightUp','leptonIsoSFWeightDown',
                                        #'leptonTrackingSFWeight','leptonTrackingSFWeightUp','leptonTrackingSFWeightDown',
                                        'leptonTriggerSFWeight','leptonTriggerSFWeightUp','leptonTriggerSFWeightDown',
                                        #'jet1puidraw',
                                        ])
##### Add Producers: #####
    cfg['Processors'] = [  'producer:MuonTriggerMatchingProducer',] + cfg['Processors']
    cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
    #cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:PFCandidatesProducer',)
    #cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer')+1, 'producer:ZJetDressedMuonsProducer',)
    #cfg['Processors'].insert(cfg['Processors'].index('producer:GenZmmProducer'), 'producer:ZJetGenPhotonsProducer',)
    #cfg['Processors'].insert(cfg['Processors'].index('producer:GenZmmProducer'), 'producer:ZJetDressedGenMuonsProducer',)
    #cfg['Processors'].insert(cfg['Processors'].index('producer:GenZmmProducer'), 'producer:ZJetTrueGenMuonsProducer',)
##### Specify input sources for Jets & Muons: #####
    #cfg['PackedPFCandidates'] = 'pfCandidates'
    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'
    cfg['ValidMuonsInput'] = "corrected"
    cfg['GenJets'] = 'ak4GenJets'   # JTB switched off
    cfg['TaggedJets'] = 'ak4PFJetsCHS'
    cfg['UseObjectJetYCut'] = True
    cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/Summer16_07Aug2017_V11_MC/Summer16_07Aug2017_V11_MC')
    cfg['JetID'] = 'loose'
##### Change selection: (see also http://cms.cern.ch/iCMS/analysisadmin/cadilines?line=SMP-17-002&tp=an&id=1891&ancode=SMP-17-002) #####
    cfg['MuonIso'] = 'loose_2016'
    cfg['MuonID'] = 'tight'
    cfg['CutMuonPtMin'] = 25.0
    cfg['CutMuonEtaMax'] = 2.4
    cfg['ZMassRange'] = 20.0
    cfg['CutLeadingJetPtMin'] = 10.0
    #cfg['MinPUJetID'] = -0.2
    cfg['HltPaths'] = ['HLT_IsoMu24', 'HLT_IsoTkMu24']
    cfg["MuonTriggerFilterNames"] = ['HLT_IsoMu24_v2:hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09','HLT_IsoTkMu24_v3:hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09']
##### LeptonSF files: #####
    cfg['LeptonSFVariation'] = True
    cfg['LeptonIDSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/ID_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonIsoSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Iso_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonTriggerSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Trigger_EfficienciesAndSF_BCDEF.root")
    #cfg['LeptonTrackingSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Tracking_EfficienciesAndSF_BCDEFGH.root")
##### MC specific properties: #####
    cfg['NumberGeneratedEvents'] = 6952830+6933094 #+2989199+67240808+38811017 
    cfg['GeneratorWeight'] = 1.0 ## 0.624375 for s-channel +10.12*2989199+0.0*67240808+0.0*38811017
    cfg['CrossSection'] = (38.09*6952830+38.06*6933094)/(6952830+6933094) ###### no xsec for last two sets available
    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/PUWeights_BCDEFGH_13TeV_23Sep2016ReReco_TTJets_madgraphMLM-pythia8_RunIISummer16.root')
    return cfg
