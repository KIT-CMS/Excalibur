import configtools
import os

JEC = 'Summer16_07Aug2017_V11'

def config():
    cfg = configtools.getConfig('mc', 2016, 'mm', JEC=JEC)
    cfg["InputFiles"].set_input(
        bmspath="root://cmsxrootd-kit.gridka.de//pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16/*.root",
        nafpath="root://cmsxrootd-kit.gridka.de//pnfs/gridka.de/cms/disk-only/store/user/tberger/Skimming/ZJet_WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16/*.root",
        )
    cfg = configtools.expand(cfg, 
                                ['nocuts','zjetcuts','genzjetcuts','allzjetcuts'],
                                ['None','L1L2L3'],
                                False)
    configtools.remove_quantities(cfg, [
        'jet1rc','npv', 'rho','njets', 'njetsinv', 'njets30','njets10',
        'jet1chf', 'jet1nhf', 'jet1ef','jet1mf', 'jet1hfhf', 'jet1hfemf', 'jet1pf','jet1area',
        'jet1l1', 'jet1l2','jet1ptraw', 'jet1ptl1', 
        'jet2pt', 'jet2eta', 'jet2y', 'jet2phi','jet3pt', 'jet3eta', 'jet3y', 'jet3phi',
        'mpf', 'rawmpf', 'met', 'metphi', 'rawmet', 'rawmetphi', 'sumet', 'mettype1vecpt', 'mettype1pt',
        'jetHT','jetrecoilpt', 'jetrecoilphi', 'jetrecoileta', 'jetrpf',
        'jet1idtightlepveto', 'jet1idtight', 'jet1idloose','jet2idtightlepveto', 'jet2idtight', 'jet2idloose','jet3idtightlepveto', 'jet3idtight', 'jet3idloose',
        'genjet2pt','genjet2eta','genjet2y','genjet2phi','genjet3pt','genjet3eta','genjet3y','genjet3phi',
        'jet1flavor','ngenjets','ngenjets10','ngenjets30','genHT',
        'matchedgenparton1pt','matchedgenparton1flavour','matchedgenparton2pt','matchedgenjet2pt','matchedgenjet2eta','matchedgenjet2phi',
        'genzfound','validgenzfound','deltarzgenz','ngenneutrinos',
        'mu1iso', 'mu1sumchpt', 'mu1sumnhet', 'mu1sumpet', 'mu1sumpupt',
        'mu1idloose','mu1idmedium','mu1idtight','matchedgenmuon1pt',#'matchedgenmuon1eta','matchedgenmuon1phi',
        'mu2idloose','mu2idmedium','mu2idtight','matchedgenmuon2pt',#'matchedgenmuon2eta','matchedgenmuon2phi',
        ])
    configtools.add_quantities(cfg, [   #'mu1IDSFWeight','mu1IsoSFWeight','mu1TrackingSFWeight','mu1TriggerSFWeight',
                                        #'mu2IDSFWeight','mu2IsoSFWeight','mu2TrackingSFWeight','mu2TriggerSFWeight',
                                        'leptonIDSFWeight','leptonIsoSFWeight','leptonTrackingSFWeight','leptonTriggerSFWeight',     
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
    cfg['MinPUJetID'] = -0.2
    cfg['HltPaths'] = ['HLT_IsoMu24', 'HLT_IsoTkMu24']
    cfg["MuonTriggerFilterNames"] = ['HLT_IsoMu24_v2:hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09','HLT_IsoTkMu24_v3:hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09']
##### LeptonSF files: #####
    cfg['LeptonIDSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/ID_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonIsoSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Iso_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonTriggerSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Trigger_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonTrackingSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Tracking_EfficienciesAndSF_BCDEFGH.root")
##### MC specific properties: #####
    cfg['NumberGeneratedEvents'] = 29705748
    cfg['GeneratorWeight'] =  1.0
    cfg['CrossSection'] = 50260.0
    cfg['PileupWeightFile'] = os.path.join(configtools.getPath() , 'data/pileup/PUWeights_BCDEFGH_13TeV_23Sep2016ReReco_WJetsToLNu_madgraphMLM-pythia8_RunIISummer16.root')
    return cfg
