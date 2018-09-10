import configtools
import os

def config():
    cfg = configtools.getConfig('data', 2016, 'mm', bunchcrossing='25ns')
    cfg["InputFiles"].set_input(
        #ekppath='/storage/c/tberger/testfiles/skimming_output/data/ZJet_SingleMuon_Run2016D-Legacy-07Aug2017-v1_testfile.root',
        bmspathB1='root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016B-07Aug17_ver1-v1/*.root',
        bmspathB2='root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016B-07Aug17_ver2-v1/*.root',
        bmspathC ='root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016C-07Aug17-v1/*.root',
        bmspathD ='root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016D-07Aug17-v1/*.root',
        nafpathB1='root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016B-07Aug17_ver1-v1/*.root',
        nafpathB2='root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016B-07Aug17_ver2-v1/*.root',
        nafpathC ='root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016C-07Aug17-v1/*.root',
        nafpathD ='root://cmsxrootd-kit.gridka.de/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016D-07Aug17-v1/*.root',
        #nafpath='/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/testfiles/ZJet_SingleMuon_Run2016D-Legacy-07Aug2017-v1_testfile.root',
    )
    cfg = configtools.expand(cfg, 
                                ['nocuts','leptoncuts','zjetcuts'],
                                ['None','L1','L1L2L3','L1L2L3Res'])
    configtools.remove_quantities(cfg, ['jet1rc'])
    configtools.add_quantities(cfg, [   'mu1IDSFWeight', 'mu2IDSFWeight', 'leptonIDSFWeight',
                                        'mu1IsoSFWeight','mu2IsoSFWeight','leptonIsoSFWeight',
                                        'mu1TrackingSFWeight','mu2TrackingSFWeight','leptonTrackingSFWeight',  
                                        'mu1TriggerSFWeight','mu2TriggerSFWeight','leptonTriggerSFWeight',     
                                        'jet1puidraw',
                                        ])
##### Add Producers: #####
    cfg['Processors'] = [  'producer:MuonTriggerMatchingProducer',
                            ] + cfg['Processors'] + [
                            'producer:LeptonIDSFProducer',
                            'producer:LeptonIsoSFProducer',
                            'producer:LeptonTrackingSFProducer',
                            'producer:LeptonTriggerSFProducer',
                            'producer:LeptonSFProducer',
                            ]
    cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
##### Specify input sources for Jets & Muons: #####
    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'
    cfg['ValidMuonsInput'] = "corrected"
    cfg['TaggedJets'] = 'ak4PFJetsCHS'
##### Change selection: (see also http://cms.cern.ch/iCMS/analysisadmin/cadilines?line=SMP-17-002&tp=an&id=1891&ancode=SMP-17-002) #####
    cfg['MuonIso'] = 'loose_2016'
    cfg['MuonID'] = 'tight'
    cfg['CutMuonPtMin'] = 25.0
    cfg['CutMuonEtaMax'] = 2.4
    cfg['ZMassRange'] = 20.0
    cfg['CutLeadingJetPtMin'] = 15.0
    cfg['MinPUJetID'] = -0.4
    cfg['HltPaths'] = ['HLT_IsoMu24', 'HLT_IsoTkMu24']
    cfg["MuonTriggerFilterNames"] = ['HLT_IsoMu24_v2:hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09','HLT_IsoTkMu24_v3:hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09']
##### LeptonSF files: #####
    cfg['LeptonIDSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/ID_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonIsoSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Iso_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonTriggerSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Trigger_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonTrackingSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Tracking_EfficienciesAndSF_BCDEFGH.root")
##### Json & JEC #####
    cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/Summer16_07Aug2017BCD_V11_DATA/Summer16_07Aug2017BCD_V11_DATA')
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(),'data/json/Cert_BCD_13TeV_23Sep2016ReReco_Collisions16_JSON.txt')]
    return cfg
