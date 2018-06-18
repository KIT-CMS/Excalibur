import configtools
import os

def config():
    cfg = configtools.getConfig('data', 2016, 'mm', bunchcrossing='25ns')
    cfg["InputFiles"].set_input(
        #ekppath='/storage/c/tberger/testfiles/skimming_output/data/ZJet_SingleMuon_Run2016D-Legacy-07Aug2017-v1_testfile.root',
        ekppathF ='srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016F-07Aug17-v1_noJTB/*.root',
        ekppathG ='srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016G-07Aug17-v1_noJTB/*.root',
        ekppathH ='srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016H-07Aug17-v1_noJTB/*.root',
        nafpathF ='srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016F-07Aug17-v1_noJTB/*.root',
        nafpathG ='srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016G-07Aug17-v1_noJTB/*.root',
        nafpathH ='srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_SingleMuon_Run2016H-07Aug17-v1_noJTB/*.root',
        #nafpath='/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/testfiles/ZJet_SingleMuon_Run2016G-Legacy-07Aug2017-v1_testfile.root',
    )
    cfg = configtools.expand(cfg, ['nocuts', 'zcuts'], ['None'])#, True),'L1L2L3','L1L2L3Res'
    configtools.remove_quantities(cfg, ['jet1ptl1l2l3', 'jet1res', 'jet1rc'])
    configtools.add_quantities(cfg, [   'mu1IDSFWeight', 'mu2IDSFWeight', 'leptonIDSFWeight',
                                        'mu1IsoSFWeight','mu2IsoSFWeight','leptonIsoSFWeight',
                                        'mu1TrackingSFWeight','mu2TrackingSFWeight','leptonTrackingSFWeight',
                                        'mu1TriggerSFWeight','mu2TriggerSFWeight','leptonTriggerSFWeight',
                                        ])
 ##### Add Producers: #####
    cfg['Processors'] = [  'producer:MuonTriggerMatchingProducer',
                            ] + cfg['Processors'] + [
                            'producer:LeptonIDSFProducer',
                            'producer:LeptonIsoSFProducer',
                            'producer:LeptonTrackingSFProducer',
                            'producer:LeptonTriggerSFProducer',
                            ]
    cfg['Processors'].insert(cfg['Processors'].index('producer:ValidMuonsProducer'), 'producer:MuonCorrectionsProducer',)
##### Specify input sources for Jets & Muons: #####
    cfg['VertexSummary'] = 'offlinePrimaryVerticesSummary'
    cfg['ValidMuonsInput'] = "corrected"
    cfg['TaggedJets'] = 'ak4PFJets' # JTB switched off, non-CHS Jets
##### Change selection: (see also http://cms.cern.ch/iCMS/analysisadmin/cadilines?line=SMP-17-002&tp=an&id=1891&ancode=SMP-17-002) #####
    cfg['MuonIso'] = 'loose_2016'
    cfg['MuonID'] = 'tight'
    cfg['CutMuonPtMin'] = 20.0
    cfg['CutMuonEtaMax'] = 2.4
    cfg['ZMassRange'] = 20.0
    cfg['HltPaths'] = ['HLT_IsoMu24', 'HLT_IsoTkMu24']
    cfg["MuonTriggerFilterNames"] = ['HLT_IsoMu24_v2:hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09','HLT_IsoTkMu24_v3:hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09']
##### LeptonSF files: #####
    cfg['LeptonIDSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/ID_EfficienciesAndSF_GH.root")
    cfg['LeptonIsoSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Iso_EfficienciesAndSF_GH.root")
    cfg['LeptonTriggerSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Trigger_EfficienciesAndSF_GH.root")
    cfg['LeptonTrackingSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Tracking_EfficienciesAndSF_BCDEFGH.root")
##### Json & JEC #####
    cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/Summer16_07Aug2017GH_V7_DATA/Summer16_07Aug2017GH_V7_DATA')
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(),'data/json/Cert_GH_13TeV_23Sep2016ReReco_Collisions16_JSON.txt')]
    return cfg
