import configtools
import os

###
# base config
###
def getBaseConfig(tagged=False, **kwargs):
    cfg = {
        # Artus General Settings
        'ProcessNEvents': -1,
        'FirsEvent': 0,
        'Processors': [],
        'InputFiles': [],  # Overwritten by (data/mc).py, excalibur.py, json_modifier.py (if run in batch mode)
        'OutputPath': 'out', # Overwritten by excalibur.py
        # ZJetCorrectionsProducer Settings
        'Jec': '', # Path for JEC data, please set this later depending on input type
        'L1Correction': 'L1FastJet',
        'RC': True,  # Also provide random cone offset JEC, and use for type-I
        'FlavourCorrections': False,  # Calculate additional MC flavour corrections
        # ZProducer Settings
        'ZMassRange': 20.,
        'VetoMultipleZs' : False,
        # TypeIMETProducer Settings
        'Met' : 'met', # metCHS will be selected automaticly if CHS jets are requested in TaggedJets
        'TypeIJetPtMin': 15.,
        'EnableMetPhiCorrection': False,
        'MetPhiCorrectionParameters': [], # Please set this later depending on input type
        # JetRecoilProducer Settings
        'JetRecoilMinPtThreshold': 15.,
        # Valid Jet Selection	'ValidJetsInput': 'uncorrected',
        'JetID' : 'none', # object-based specification, 'none' if you want to use the event-based ID filter
        #'PuJetIDs' : ['2:puJetIDFullTight'],
        'JetMetadata' : 'jetMetadata',
        'TaggedJets' : 'ak4PFJetsCHS',
        # PU
        'PileupDensity' : 'pileupDensity',
        
        # Pipelines
        'Pipelines': {
            'default': {
                'CorrectionLevel': '', # Overwritten by expand function, set levels in data.py or mc.py
                                        # No correction at all equals 'None', not ''
                'Consumers': [
                    'ZJetTreeConsumer',
                    'cutflow_histogram',
                    ],
                'EventWeight': 'eventWeight',
                'Processors': [], # Overwritten/cleaned by expand function, set cuts in data.py or mc.py
                'Quantities': [
                    # General quantities
                    'npv', 'rho', 'weight', 'npumean',
                    'njets', 'njetsinv', 'njets30', # number of valid and invalid jets
                    'run', 'lumi', 'event',
                    # Z quantities
                    'zpt', 'zeta', 'zeta', 'zy', 'zphi', 'zmass',
                    'phistareta', 
                    'zl1pt', 'zl1eta', 'zl1phi',
                    'zl2pt', 'zl2eta', 'zl2phi',
                    # Leading jet
                    'njets10',#
                    'jet1pt', 'jet1eta', 'jet1y', 'jet1phi',
                    'jet1chf', 'jet1nhf', 'jet1ef',
                    'jet1mf', 'jet1hfhf', 'jet1hfemf', 'jet1pf',
                    'jet1area',
                    'jet1l1', 'jet1rc', 'jet1l2',
                    'jet1ptraw', 'jet1ptl1', 
                    #'jet1unc',  # Leading jet uncertainty
                    # Second jet
                    'jet2pt', 'jet2eta', 'jet2y', 'jet2phi',
                    # 3rd jet
                    'jet3pt', 'jet3eta', 'jet3y', 'jet3phi',
                    # MET and related
                    'mpf', 'rawmpf', 'met', 'metphi', 'rawmet', 'rawmetphi', 'sumet',
                    'mettype1vecpt', 'mettype1pt',
                    'jetHT',
                    'jetrecoilpt', 'jetrecoilphi', 'jetrecoileta', 'jetrpf',
                    'jet1idtightlepveto', 'jet1idtight', 'jet1idloose',
                    'jet2idtightlepveto', 'jet2idtight', 'jet2idloose',
                    'jet3idtightlepveto', 'jet3idtight', 'jet3idloose',
                    #'invalidjet1pt','invalidjet1idloose','invalidjet1eta', 'invalidjet1y', 'invalidjet1phi',
                    #'invalidjet2pt','invalidjet2idloose',
                    #'invalidjet3pt','invalidjet3idloose',
                    ],
                },
            },
        # Processors
        'Processors': [
            'producer:ValidTaggedJetsProducer',
            'producer:ValidZllJetsProducer',
            'producer:ZJetCorrectionsProducer',
            'producer:TypeIMETProducer',
            'producer:JetSorter',
            'producer:JetRecoilProducer',
            ],
        # Wire Kappa objects
        'EventMetadata' : 'eventInfo',
        'LumiMetadata' : 'lumiInfo',
        'VertexSummary': 'offlinePrimaryVerticesSummary', # What is the difference to 'goodOfflinePrimaryVerticesSummary'?
    }

    if tagged:
        cfg['Pipelines']['default']['Quantities'] += ['jet1btagpf','jet1btag', 'jet1qgtag']#,  'jet1puidraw','jet1puidtight','jet1puidmedium', 'jet1puidloose', 'jet2puidraw', 'jet2puidtight','jet2puidmedium', 'jet2puidloose']
    return cfg

def data(cfg, **kwargs):
    cfg['InputIsData'] = True
    cfg['Processors'] = ['filter:JsonFilter']+cfg['Processors']+['producer:HltProducer','filter:HltFilter',]
    cfg['Processors'] += ['producer:NPUProducer']
    cfg['ProvideL2L3ResidualCorrections'] = True
    #cfg['ProvideL2ResidualCorrections'] = True
    cfg['Pipelines']['default']['Quantities'] += ['jet1ptl1l2l3', 'jet1res']

def mc(cfg, **kwargs):
    cfg['InputIsData'] = False
    cfg['Processors'] += [
        'producer:RecoJetGenPartonMatchingProducer',
        'producer:RecoJetGenJetMatchingProducer',
        'producer:GenParticleProducer',
        'producer:NeutrinoCounter',
        'producer:ValidZllGenJetsProducer',
        ]
    cfg['GenParticles'] = 'genParticles'
    cfg['Pipelines']['default']['Quantities'] += [
        'run','lumi','event','npu',
        'genjet1pt','genjet1eta','genjet1y','genjet1phi','uncleanedgenjet1pt','uncleanedgenjet1eta',
        'genjet2pt','genjet2eta','genjet2y','genjet2phi','uncleanedgenjet2pt','uncleanedgenjet2eta',
        'jet1flavor',
        'ngenjets','ngenjets10','ngenjets30',
        'genHT',
        'matchedgenparton1pt','matchedgenparton1flavour','matchedgenparton2pt',
        'matchedgenjet1pt','matchedgenjet1eta','matchedgenjet1phi',
        'matchedgenjet2pt','matchedgenjet2eta','matchedgenjet2phi',
        'genzpt','genzy','genzeta','genzphi','genzmass',
        'genphistareta',
        'genzlepton1pt','genzlepton1eta','genzlepton1phi',
        'genzlepton2pt','genzlepton2eta','genzlepton2phi',
        'genzfound','validgenzfound',
        'deltarzgenz',
        'ngenneutrinos',
        'x1','x2','qScale',
        'numberGeneratedEventsWeight','crossSectionPerEventWeight','generatorWeight','puWeight',
        ]

    # RecoJetGenPartonMatchingProducer Settings
    cfg['DeltaRMatchingRecoJetGenParticle'] = 0.3
    cfg['JetMatchingAlgorithm'] = 'physics' # 'algorithmic' # algorithmic or physics

    # RecoJetGenJetMatchingProducer Settings
    cfg['DeltaRMatchingRecoJetGenJet'] = 0.3

    # GenParticleProducer
    cfg['GenParticleTypes'] = ['genParticle']
    cfg['GenParticlePdgIds'] = [23] # Z
    cfg['GenParticleStatus'] = 22  # see also http://www.phy.pku.edu.cn/~qhcao/resources/CTEQ/MCTutorial/Day1.pdf
    #cfg['RecoJetMatchingGenParticleStatus'] = 1    # use pythia8 status instead of default=3
    # MC sample reweighting
    cfg['Processors'] += [
        'producer:CrossSectionWeightProducer',
        'producer:ZJetNumberGeneratedEventsWeightProducer',
        'producer:EventWeightProducer'
        ]
    cfg['EventWeight'] = 'weight'
    cfg['CrossSection'] = -1
    cfg['BaseWeight'] = 1000 # pb^-1 -> fb^-1

    cfg['GenZMassRange']= 20. # not used by ValidGenZFilter

    cfg['DeltaRRadiationJet'] = 1
    cfg['CutAlphaMax'] = 0.3
    cfg['CutBetaMax'] = 0.1
    cfg['GenJets'] = 'ak4GenJetsNoNu'
    cfg['UseKLVGenJets'] = True
    # insert Generator producer before EventWeightProducer:
    cfg['Processors'].insert(cfg['Processors'].index('producer:EventWeightProducer'), 'producer:GeneratorWeightProducer')
    cfg['Processors'].insert(cfg['Processors'].index('producer:EventWeightProducer'), 'producer:PUWeightProducer')

def _2016(cfg, **kwargs):
    cfg['Pipelines']['default']['Processors'] += ['filter:JetIDCut',] # if you want to use object-based JetID selection, use 'JetID' in cfg 
    cfg['CutJetID'] = 'loose'  # choose event-based JetID selection
    cfg['CutJetIDVersion'] = 2016
    cfg['CutJetIDFirstNJets'] = 2
    cfg['CutEtaPhiCleaningFile'] = os.path.join(configtools.getPath() , 'data/hotjets-runBCDEFGH.root') #File used for eta-phi-cleaning, must contain a TH2D called "h2jet"
    cfg['CutEtaPhiCleaningPt'] = 15 # minimum jet pt for eta-phi-cleaning
    cfg['Year'] = 2016
    cfg['Energy'] = 13
    cfg['JetIDVersion'] = 2016  # for object-based JetID
    cfg['MinPUJetID'] = -1.5
    cfg['MinZllJetDeltaRVeto'] = 0.3
    cfg['JetLeptonLowerDeltaRCut'] = 0.3 # JetID 2015 does not veto muon contribution - invalidate any jets that are likely muons; requires ZmmProducer and ValidZllJetsProducer to work
    # create empty containers to allow using references prematurely
    cfg["InputFiles"] = configtools.InputFiles()
    # data settings also used to derive values for mc
    cfg['Minbxsec'] = 69.2
    cfg['NPUFile'] = os.path.join(configtools.getPath(),'data/pileup/pumean_data2016_13TeV.txt')
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_BCDEFGH_13TeV_23Sep2016ReReco_Collisions16_JSON.txt')]
    #cfg['JsonFiles'] = configtools.RunJSON('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt')

def _2017(cfg, **kwargs):
    cfg['Pipelines']['default']['Processors'] += ['filter:JetIDCut',] # if you want to use object-based JetID selection, use 'JetID' in cfg
    cfg['CutJetID'] = 'tightlepveto'  # choose event-based JetID selection
    cfg['CutJetIDVersion'] = 2017
    cfg['CutJetIDFirstNJets'] = 2
    cfg['Year'] = 2017
    cfg['Energy'] = 13
    cfg['JetIDVersion'] = 2017  # for object-based JetID
    cfg['MinZllJetDeltaRVeto'] = 0.3
    cfg['JetLeptonLowerDeltaRCut'] = 0.3 # JetID 2015 does not veto muon contribution - invalidate any jets that are likely muons; requires ZmmProducer and ValidZllJetsProducer to work
    # create empty containers to allow using references prematurely
    cfg["InputFiles"] = configtools.InputFiles()
    # data settings also used to derive values for mc
    cfg['Minbxsec'] = 69.2
    cfg['NPUFile'] = os.path.join(configtools.getPath(), 'data/pileup/pumean_data2017_13TeV.txt')
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt')]

def data_2017(cfg, **kwargs):
    # -- modifications for JEC V10 (jun. 2018 JERC)

    # Type-I MET modification (recommended jun. 2018)
    # -> do not consider jets with pt < 75 GeV in a particular abs(eta) region
    #    when calculating Type-I MET
    cfg['EnableTypeIModification'] = True
    cfg['TypeIModExcludeJetPtMax'] = 75
    cfg['TypeIModExcludeJetAbsEtaMin'] = 2.650
    cfg['TypeIModExcludeJetAbsEtaMax'] = 3.139

    # object-based eta-phi cleaning (recommended jun. 2018)
    # -> invalidate jets according to eta-phi masks provided in a external ROOT file
    cfg['Processors'].insert(cfg['Processors'].index("producer:ZJetCorrectionsProducer") + 1, "producer:JetEtaPhiCleaner")
    cfg['JetEtaPhiCleanerFile'] = os.path.join(configtools.getPath(), "data/cleaning/jec17/data17_17Nov2017_ReReco/hotjets-17runBCDEF_addEtaPhiMask_2018-06-11.root")
    cfg['JetEtaPhiCleanerHistogramNames'] = ["h2hotfilter", "h2_additionalEtaPhiFilter"]
    cfg['JetEtaPhiCleanerHistogramValueMaxValid'] = 9.9   # >=10 means jets should be invalidated


def ee(cfg, **kwargs):
    cfg['Electrons'] = 'electrons'
    cfg['ElectronMetadata'] = 'electronMetadata'
    cfg['HltPaths']= ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ', 'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ', 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL', 'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL']
    # The order of these producers is important!
    cfg['Processors'] = [	
                            'producer:ZJetValidElectronsProducer',
                            'producer:RecoZmmProducer',
                            'producer:ZeeProducer',	
                            ]+cfg['Processors']
        
    cfg['Pipelines']['default']['Processors'] = [
        'filter:MinElectronsCountFilter',
        'filter:MaxElectronsCountFilter',
        'filter:ElectronPtCut',
        'filter:ElectronEtaCut',
        #'filter:ZFilter',
        'filter:ValidZCut',
        'filter:ZPtCut',
        'filter:ValidJetsFilter',
        'filter:LeadingJetPtCut',
        'filter:LeadingJetEtaCut',
        'filter:LeadingJetYCut',
        'filter:AlphaCut',
        'filter:BackToBackCut',
        ]
    cfg['Pipelines']['default']['Consumers'] += ['KappaElectronsConsumer',]
    
    cfg['ElectronID'] = 'tight' # OLD electron ID code: set to 'none' or 'user' if using VID (s. below)
    cfg['ElectronIsoType'] = 'none'
    cfg['ElectronIso'] = 'none'
    cfg['ElectronReco'] = 'none'

    # -- ZJetValidElectronsProducer
    cfg['ApplyElectronVID'] = False
    #cfg['ElectronVIDName'] = "Summer16-80X-V1"
    #cfg['ElectronVIDType'] = "cutbased"
    #cfg['ElectronVIDWorkingPoint'] = "tight"

    cfg['Pipelines']['default']['Quantities'] += [
        'epluspt','epluseta','eplusphi','eplusiso',
        'eminuspt', 'eminuseta', 'eminusphi', 'eminusiso',
        'e1pt', 'e1eta', 'e1phi', 
        'e1idloose', 'e1idmedium', 'e1idtight', 'e1idveto', 'e1idloose95', 'e1idmedium95', 'e1idtight95','e1idveto95',# 'e1mvanontrig', 'e1mvatrig',
        'e2pt', 'e2eta', 'e2phi', 
        'e2idloose', 'e2idmedium', 'e2idtight', 'e2idveto', 'e2idloose95', 'e2idmedium95', 'e2idtight95','e2idveto95',# 'e2mvanontrig', 'e2mvatrig',
        'nelectrons', 'validz',
        ]
    cfg['MinNElectrons'] = 2
    cfg['MaxNElectrons'] = 3
    cfg['CutElectronPtMin'] = 25.0
    cfg['CutElectronEtaMax'] = 2.4
    cfg['CutLeadingJetPtMin'] = 12.0
    cfg['CutLeadingJetEtaMax'] = 1.3
    cfg['CutLeadingJetYMax'] = 2.5
    cfg['CutBackToBack'] = 0.34
    cfg['CutAlphaMax'] = 0.3
    cfg['CutZPtMin'] = 30.0

def mcee(cfg, **kwargs):
    cfg['Pipelines']['default']['Quantities'] += [
        'ngenelectrons',
        'matchedgenelectron1pt',#'matchedgenelectron1eta','matchedgenelectron1phi',
        'matchedgenelectron2pt',#'matchedgenelectron2eta','matchedgenelectron2phi',
        'genepluspt','genepluseta','geneplusphi',
        'geneminuspt','geneminuseta','geneminusphi',
        'gene1pt','gene1eta','gene1phi',
        'gene2pt','gene2eta','gene2phi',
        #'genParticleMatchDeltaR',
    ]
    # reco-gen electron matching producer
    cfg['Processors'] += ['producer:GenZeeProducer', 'producer:RecoElectronGenParticleMatchingProducer']
    cfg['RecoElectronMatchingGenParticleStatus'] = 3
    cfg['DeltaRMatchingRecoElectronGenParticle'] = 0.3
    cfg["RecoElectronMatchingGenParticlePdgIds"] = [11, -11]
    cfg["InvalidateNonGenParticleMatchingRecoElectrons"] = False
    cfg['GenParticleTypes'] += ['genElectron']
    cfg['GenElectronStatus'] = 3
    # KappaCollectionsConsumer: dont add taus or taujets:
    cfg['BranchGenMatchedElectrons'] = True
    cfg['AddGenMatchedTaus'] = False
    cfg['AddGenMatchedTauJets'] = False
    
    # not sure about the status codes in aMCatNLO/MG5. theres usually an e+/e-
    # pair with status 1 in each event, so take this number for now
    # see also http://www.phy.pku.edu.cn/~qhcao/resources/CTEQ/MCTutorial/Day1.pdf
    #cfg['RecoElectronMatchingGenParticleStatus'] = 1
    #cfg[''] = 1
    
    cfg['Pipelines']['default']['Processors'] += [
            'filter:ValidGenZCut',
            'filter:GenZPtCut',
            ]


def mm(cfg, **kwargs):
    cfg['Muons'] = 'muons'
    cfg['HltPaths'] = ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ']
    # The order of these producers is important!
    cfg['Processors'] = [	#'producer:MuonCorrectionsProducer',
                            'producer:ValidMuonsProducer',
                            'producer:ZmmProducer', # seems to destroy GenZ
                            'producer:RecoZmmProducer',
                            ]+cfg['Processors']
    cfg['Pipelines']['default']['Processors'] = [
        'filter:ValidJetsFilter',
        'filter:LeadingJetPtCut',
        'filter:LeadingJetEtaCut',
        'filter:MinNMuonsCut',
        'filter:MaxNMuonsCut',
        'filter:MuonPtCut',
        'filter:MuonEtaCut',
        #'filter:ZFilter',
        'filter:ValidZCut', # includes Z mass cut
        'filter:ZPtCut',
        'filter:LeadingJetYCut',
        'filter:AlphaCut',
        'filter:BackToBackCut',
        ]
    cfg['Pipelines']['default']['Consumers'] += ['KappaMuonsConsumer',]
    # In case of Muon Corrections
    #cfg['ValidMuonsInput'] = "corrected"
    
    # validMuonsProducer
    cfg['MuonID'] = 'tight'
    cfg['MuonIso'] = 'tight'
    cfg['MuonIsoType'] = 'pf'
    #cfg['UseHighPtID'] = True
    
    cfg['Pipelines']['default']['Quantities'] += [
        'mupluspt', 'mupluseta', 'muplusphi', 'muplusiso',
        'muminuspt', 'muminuseta', 'muminusphi', 'muminusiso',
        'mu1pt', 'mu1eta', 'mu1phi',
        'mu1iso', 'mu1sumchpt', 'mu1sumnhet', 'mu1sumpet', 'mu1sumpupt',
        'mu2pt', 'mu2eta', 'mu2phi',
        'mu3pt', 'mu3eta', 'mu3phi',
        'nmuons', 'validz',
        'leptonSFWeight','leptonTriggerSFWeight',
        'mu1idloose','mu1idmedium','mu1idtight',
        'mu2idloose','mu2idmedium','mu2idtight',
        ]
    cfg['CutNMuonsMin'] = 2
    cfg['CutNMuonsMax'] = 3
    cfg['CutMuonPtMin'] = 20.0
    cfg['CutMuonEtaMax'] = 2.3
    cfg['CutLeadingJetPtMin'] = 12.0
    cfg['CutLeadingJetEtaMax'] = 1.3
    cfg['CutLeadingJetYMax'] = 2.5
    cfg['CutBackToBack'] = 0.34
    cfg['CutAlphaMax'] = 0.3
    cfg['CutZPtMin'] = 30.0

#Efficiency calculation
    cfg["InvalidateNonMatchingMuons"] = False
    cfg["TriggerObjects"] = "triggerObjects"
    cfg["TriggerInfos"] = "triggerObjectMetadata"
    cfg['MuonPtVariationFactor'] = 1.00
    cfg['TriggerSFRuns'] = []

###
# config fragments for combinations of two categories (data/MC+year, year+channel, ...)
###

def mcmm(cfg, **kwargs):
    cfg['Pipelines']['default']['Quantities'] += [
        'matchedgenmuon1pt',#'matchedgenmuon1eta','matchedgenmuon1phi',
        'matchedgenmuon2pt',#'matchedgenmuon2eta','matchedgenmuon2phi',
        'ngenmuons',
        'genmupluspt','genmupluseta','genmuplusphi',
        'genmuminuspt','genmuminuseta','genmuminusphi',
        'genmu1pt','genmu1eta','genmu1phi',
        'genmu2pt','genmu2eta','genmu2phi',
        ]
    cfg['Processors'].insert(cfg['Processors'].index('producer:ValidZllGenJetsProducer'), 'producer:GenZmmProducer',)
    cfg['Processors'] += [
    #        'producer:GenZmmProducer', #Use this for Status 1 muons
            #'producer:ValidGenZmmProducer', #Use this for original muons
            'producer:RecoMuonGenParticleMatchingProducer',
            ]
    cfg['Pipelines']['default']['Processors'] += [
        'filter:MinNGenMuonsCut',
        'filter:MaxNGenMuonsCut',
        'filter:GenMuonPtCut',
        'filter:GenMuonEtaCut',
        'filter:ValidGenZCut',
        'filter:GenZPtCut',
        'filter:LeadingGenJetYCut',
        ]
    cfg['RecoMuonMatchingGenParticleStatus'] = 1
    cfg['DeltaRMatchingRecoMuonGenParticle'] = 0.5 # TODO: check if lower cut is more reasonable
    cfg['GenParticleTypes'] += ['genMuon', 'genTau']
    cfg['GenMuonLowerPtCuts'] = ['27']
    cfg['GenMuonUpperAbsEtaCuts'] = ['2.3']
    cfg['GenMuonStatus'] = 1

    # for KappaMuonsConsumer
    cfg['BranchGenMatchedMuons'] = True
    cfg['AddGenMatchedTaus'] = False
    cfg['AddGenMatchedTauJets'] = False

def data_2016(cfg, **kwargs):
    cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/Summer16_07Aug2017BCD_V1_DATA/Summer16_07Aug2017BCD_V1_DATA')

def mc_2016(cfg, **kwargs):
    #cfg['PileupWeightFile'] = os.path.join(configtools.getPath(),'data/pileup/pileup_weights_BCDEFGH_13TeV_23Sep2016ReReco_Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16.root')
    cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/Summer16_07Aug2017_V1_MC/Summer16_07Aug2017_V1_MC')

def _2016mm(cfg, **kwargs):
    cfg['MuonRochesterCorrectionsFile'] = os.path.join(configtools.getPath(),'../Artus/KappaAnalysis/data/rochcorr2016')
    cfg['MuonEnergyCorrection'] = 'rochcorr2016'
    ### Get Root file from POG ### https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults ###
    cfg['LeptonIDSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/ID_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonIsoSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Iso_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonTriggerSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Trigger_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonTrackingSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016latest/Tracking_EfficienciesAndSF_BCDEFGH.root")

def _2016ee(cfg, **kwargs):
    # -- ZJetValidElectronsProducer
    cfg['ElectronID'] = "user"
    cfg['ApplyElectronVID'] = True
    cfg['ElectronVIDName'] = "Summer16-80X-V1"
    cfg['ElectronVIDType'] = "cutbased"
    cfg['ElectronVIDWorkingPoint'] = "tight"

def _2017ee(cfg, **kwargs):
    # -- ZJetValidElectronsProducer
    cfg['ElectronID'] = "user"
    cfg['ApplyElectronVID'] = True
    cfg['ElectronVIDName'] = "Fall17-94X-V1-Preliminary"
    cfg['ElectronVIDType'] = "cutbased"
    cfg['ElectronVIDWorkingPoint'] = "tight"

    # -- double electron triggers: Ele17 no longer deployed
    cfg['HltPaths']= [
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL',
    ]

def _2017mm(cfg, **kwargs):
    cfg['HltPaths'] = [
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ',
        'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ',
        # -- lowest pT unprescaled trigger for the whole of 2017
        # https://indico.cern.ch/event/682891/contributions/2810364/attachments/1570825/2477991/20171206_CMSWeek_MuonHLTReport_KPLee_v3_1.pdf
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8',
    ]

def data_2016mm(cfg, **kwargs):
    #cfg['LeptonSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016/SFData_ICHEP.root")
    #cfg['TriggerSFRuns'] = [274094,276097]
    ### Check if chosen histogram is consistent with ID & Isolation choice!
    cfg['LeptonIDSFHistogramName'] = 'MC_NUM_TightID_DEN_genTracks_PAR_eta/efficienciesDATA/histo_eta_DATA'
    cfg['LeptonIsoSFHistogramName'] = 'LooseISO_TightID_eta/efficienciesDATA/histo_eta_DATA'
    cfg['LeptonTriggerSFHistogramName'] = 'IsoMu24_OR_IsoTkMu24_EtaBins/efficienciesDATA/histo_eta_DATA'
    cfg['LeptonTrackingSFHistogramName'] = 'ratio_eff_eta3_dr030e030_corr'
    
def mc_2016mm(cfg, **kwargs):
    #cfg['LeptonSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016/SFMC_Moriond.root")
    ### Check if chosen histogram is consistent with ID & Isolation choice!
    cfg['LeptonIDSFHistogramName'] = 'MC_NUM_TightID_DEN_genTracks_PAR_eta/efficienciesMC/histo_eta_MC'
    cfg['LeptonIsoSFHistogramName'] = 'LooseISO_TightID_eta/efficienciesMC/histo_eta_MC'
    cfg['LeptonTriggerSFHistogramName'] = 'IsoMu24_OR_IsoTkMu24_EtaBins/efficienciesMC/histo_eta_MC'
    cfg['LeptonTrackingSFHistogramName'] = 'ratio_eff_eta3_dr030e030_corr'
    



