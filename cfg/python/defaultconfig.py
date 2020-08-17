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
        'L1Correction': 'L1FastJet',  # default L1 correction naming
        'RC': True,  # Also provide random cone offset JEC, and use for type-I, residual corrections only
        'FlavourCorrections': False,  # Calculate additional MC flavour corrections
        # ZProducer Settings
        'ZMassRange': 20.,  # maybe not default for generated jets
        'VetoMultipleZs' : False,
        # TypeIMETProducer Settings
        'Met' : 'met',  # metCHS will be selected automaticly if CHS jets are requested in TaggedJets
        'TypeIJetPtMin': 15.,
        'EnableMetPhiCorrection': False,
        'MetPhiCorrectionParameters': [], # Please set this later depending on input type
        # MPF contribution splitting
        'MPFSplittingJetPtMin': 15.,
        'JNPFJetPtMin': 15.,
        # JetRecoilProducer Settings
        'JetRecoilMinPtThreshold': 15.,  # currently not in use
        # Valid Jet Selection
        # 'ValidJetsInput': 'uncorrected',  # set to default
        'JetID' : 'none', # object-based specification, 'none' if you want to use the event-based ID filter
        'PUJetID': 'none', # choose 'none' to use the fullDiscriminant and set the cut later, OR choose working point 'loose','medium','tight'
        'PUJetIDModuleName': 'AK4PFCHSpileupJetIdEvaluator',  # choose 'pileupJetId' for KAPPA files with slimmedJets
        'JetMetadata' : 'jetMetadata',  # folder to look for jet variables in KAPPA files
        'TaggedJets' : 'ak4PFJetsCHS',  # default folder to look for saved jets in KAPPA files
        # PU
        'PileupDensity' : 'pileupDensity',  # rho, label for skim collection in KAPPA files
        # 'PackedPFCandidates': 'pfCandidates',  # please do not comment in when not available in Kappa files
        # Pipelines
        'UseObjectJetYCut' : False,  # default object-based rapidity cut
        'Pipelines': {
            'default': {
                'CorrectionLevel': '', # Overwritten by expand function, set levels in data.py or mc.py
                                        # No correction at all equals 'None', not ''
                'Consumers': [
                    'ZJetTreeConsumer',  # writes out ntuples into root file
                    'cutflow_histogram',  # writes out cutflow into root file
                    ],
                'EventWeight': 'eventWeight',  # new weight that sums up all other weights,
                #TODO: unify weight name and remove other appearances
                'Processors': [], # Overwritten/cleaned by expand function, set cuts in data.py or mc.py
                'Quantities': [
                    # General quantities
                    'npv', 'rho', 'npumean', # pileup observables
                    'weight',  # TODO: Rename and change MERLIN
                    'njets',  # 'njetsinv', 'njets30', 'njets10', # number of valid and invalid jets
                    'run', 'lumi', 'event',
                    # Z quantities
                    'zpt', 'zeta', 'zy', 'zphi', 'zmass',
                    'phistareta', 'ystar', 'yboost',
                    'zl1pt', 'zl1eta', 'zl1phi',  # leading lepton used for Z reconstruction
                    'zl2pt', 'zl2eta', 'zl2phi',  # second leading lepton used for Z reconstruction
                    # Leading jet
                    'jet1pt', 'jet1eta', 'jet1y', 'jet1phi',  # leading jet observable
                    # 'jet1chf', 'jet1nhf', 'jet1ef', 'jet1mf', 'jet1hfhf', 'jet1hfemf', 'jet1pf',
                    # particle flow energy fractions, comment in if needed for manual cross checks
                    'jet1area',  # area of jet used for cross checks
                    'jet1l1', 'jet1rc', 'jet1l2',  # leading jet corrections L1, L1RC, L2L3, TODO: change name to jet1l2l3?
                    'jet1ptraw', 'jet1ptl1',  # raw and L1 corrected leading jet pT, TODO: remove pTs and use correction factors
                    #'jet1unc',  # Leading jet uncertainty, not implemented yet
                    # Second jet
                    'jet2pt', 'jet2eta', 'jet2y', 'jet2phi',
                    # 3rd jet
                    'jet3pt', 'jet3eta', 'jet3y', 'jet3phi',
                    # MET and related
                    'mpf', 'rawmpf', 'met', 'metphi', 'rawmet', 'rawmetphi', 'sumet',  # raw = without type-1 correction, sumet = sum over all pTs
                    'mettype1vecpt', 'mettype1pt',  # vectorial and scalar difference between corrected and uncorrected met
                    # 'jetHT',  # scalar sum of all jet pTs
                    # 'jetrecoilpt', 'jetrecoilphi', 'jetrecoileta', 'jetrpf',  # recoil observables
                    #'jet1idtightlepveto', 'jet1idtight', 'jet1idloose', 'jet1puidtight', 'jet1puidmedium', 'jet1puidloose', 'jet1puidraw' # please add jet IDs only necessary ones manually
                    # 'jet2idtightlepveto', 'jet2idtight', 'jet2idloose', 'jet2puidtight', 'jet2puidmedium', 'jet2puidloose'
                    # 'jet3idtightlepveto', 'jet3idtight', 'jet3idloose',
                    #'invalidjet1pt','invalidjet1idloose','invalidjet1eta', 'invalidjet1y', 'invalidjet1phi',
                    #'invalidjet2pt','invalidjet2idloose',
                    #'invalidjet3pt','invalidjet3idloose',
                    ],
                },
            },
        # Processors
        'Processors': [
            'producer:ValidTaggedJetsProducer',  # builds jet collection
            'producer:ValidZllJetsProducer',  # applies lepton cleaning, needs to run before the 'ZJetCorrectionsProducer'
            'producer:ZJetCorrectionsProducer',  # applies correction factors
            'producer:TypeIMETProducer',  # applies type-1 correction, can run on unsorted collections
            'producer:JetSorter',  # sorts jets
            # 'producer:JetRecoilProducer',  # produces jet recoil observables, use if neccessary
            ],
        # Wire Kappa objects
        'EventMetadata' : 'eventInfo',
        'LumiMetadata' : 'lumiInfo',
        'VertexSummary': 'goodOfflinePrimaryVerticesSummary',
        'TriggerInfos': 'triggerObjectMetadata',
        'TriggerObjects': 'triggerObjects'
    }
    if tagged:
        cfg['Pipelines']['default']['Quantities'] += ['jet1btagpf','jet1btag', 'jet1qgtag']
    return cfg


def data(cfg, **kwargs):
    cfg['InputIsData'] = True
    cfg['Processors'] = ['filter:JsonFilter']+cfg['Processors']+['producer:HltProducer','filter:HltFilter',]
    cfg['Processors'] += ['producer:NPUProducer']
    cfg['ProvideL2L3ResidualCorrections'] = True
    #cfg['ProvideL2ResidualCorrections'] = True
    cfg['Pipelines']['default']['Quantities'] += ['jet1ptl1l2l3', 'jet1res']  # TODO: restructure as mentioned above

    # -- process keyword arguments

    # 'JEC': if provided, point to JEC file in ../JECDatabase
    try:
        _jec_string = kwargs['JEC']
    except KeyError:
        print " WARNING! Keyword argument `JEC` to `getBaseConfig` was not given. cfg['Jec'] must be set manually..."
    else:
        cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/{0}_DATA/{0}_DATA'.format(_jec_string))
    _jer_string = kwargs.get('JER', None)
    if _jer_string is not None:
        cfg['JER'] = os.path.join(configtools.getPath(), '../JRDatabase/textFiles/{0}_DATA/{0}_DATA'.format(_jer_string))
        cfg['JERMethod'] = "stochastic"
        cfg['JERSmearerSeed'] = 92837465
        # insert smearer and sorter after the matching producer
        cfg['Processors'].insert(cfg['Processors'].index('producer:JetSorter'), 'producer:JERSmearer',)


def mc(cfg, **kwargs):
    cfg['InputIsData'] = False
    cfg['Processors'] += [
        'producer:GenParticleProducer',
        'producer:ValidZllGenJetsProducer',
        'producer:RecoJetGenPartonMatchingProducer',
        #'producer:GenJetGenPartonMatchingProducer',
        'producer:RecoJetGenJetMatchingProducer',
        'producer:NeutrinoCounter',
        'producer:ZJetTrueGenMuonsProducer',
        #'producer:ZJetGenWeightProducer'
        ]
    cfg['GenParticles'] = 'genParticles'
    cfg['Pipelines']['default']['Quantities'] += [
        'npu',
        'genjet1pt','genjet1eta','genjet1y','genjet1phi', # generated jet observables
        'genjet2pt','genjet2eta','genjet2y','genjet2phi',
        'genjet3pt','genjet3eta','genjet3y','genjet3phi',
        'jet1flavor',  # flavor of reco jet calculated by MC info
        'ngenjets',  # 'ngenjets10','ngenjets30',
        # 'genHT',  # generator HT, sum of all out-coming particles
        'matchedgenparton1flavour',#'matchedgenparton1pt','matchedgenparton1y','matchedgenparton1phi','matchedgenparton1mass',
        'matchedgenparton2flavour',#'matchedgenparton2pt','matchedgenparton2y','matchedgenparton2phi','matchedgenparton2mass',
        'matchedgenjet1pt','matchedgenjet1eta','matchedgenjet1y','matchedgenjet1phi',  # matched gen jet observables
        'matchedgenjet2pt','matchedgenjet2eta','matchedgenjet2y','matchedgenjet2phi',
        'genzpt','genzy','genzeta','genzphi','genzmass',
        #'genparton1flavour','genparton1pt','genparton1y','genparton1phi','genparton1mass',
        # 'truezpt','truezy','truezeta','truezphi','truezmass',
        # 'truetaupluspt', 'truetauplusy', 'truetaupluseta', 'truetauplusphi', 'truetauplusmass',
        # 'truetauminuspt','truetauminusy','truetauminuseta','truetauminusphi','truetauminusmass',
        'genphistareta', 'genystar', 'genyboost', 'matchedgenystar', 'matchedgenyboost',
        'genzl1pt','genzl1eta','genzl1phi',
        'genzl2pt','genzl2eta','genzl2phi',
        # 'genzfound','validgenzfound',  # maybe required for debugging
        # 'deltarzgenz',  # calculation moved to MERLIN
        # 'ngenneutrinos',  # maybe used for background estimation
        'x1','x2','qScale',  # qScale taken from hard process saved in MC
        'numberGeneratedEventsWeight','crossSectionPerEventWeight','generatorWeight','puWeight',
        ]
    
    #lheWeightNames = ['nominal','isrDefup','isrDefdown','fsrDefup','fsrDefdown']
    #cfg['Pipelines']['default']['Quantities'] += ['genWeight_{}'.format(lheWeightName) for lheWeightName in {lheWeightNames}]

    # RecoJetGenPartonMatchingProducer Settings
    cfg['DeltaRMatchingRecoJetGenParticle'] = 0.3
    cfg['JetMatchingAlgorithm'] = 'physics' # 'algorithmic' # algorithmic or physics

    # RecoJetGenJetMatchingProducer Settings
    cfg['DeltaRMatchingRecoJetGenJet'] = 0.3  # TODO: Check if still valid

    # GenParticleProducer
    cfg['GenParticleTypes'] = ['genParticle']  # options: None, genElectrons, genMuons, genTaus
    cfg['GenParticlePdgIds'] = [23] # Z PDG-ID
    cfg['GenParticleStatus'] = 22  # PYTHIA8-status, see also http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html
    #cfg['RecoJetMatchingGenParticleStatus'] = 1    # use pythia8 status instead of default=3
    # MC sample reweighting
    cfg['Processors'] += [
        # 'producer:ZJetPartonProducer',
        'producer:CrossSectionWeightProducer',
        'producer:ZJetNumberGeneratedEventsWeightProducer',
        'producer:GeneratorWeightProducer',  # insert Generator producer before EventWeightProducer:
        'producer:PUWeightProducer',
        'producer:EventWeightProducer'
        ]
    cfg['EventWeight'] = 'weight'  # TODO: rename as mentioned above
    cfg['CrossSection'] = -1  # need to be set in individual config file
    cfg['BaseWeight'] =   1000  # pb^-1 -> fb^-1, default unit: fb^-1

    # ZJetGenWeightProducer
    cfg['GenEventInfoMetadata'] = 'genEventInfoMetadata'
    #cfg['ZJetGenWeightNames'] = lheWeightNames

    # cfg['GenZMassRange']= 20. # not used by ValidGenZFilter, TODO: Remove this and use ZMassRange
    # cfg['DeltaRRadiationJet'] = 1  # TODO: Usage?

    cfg['CutAlphaMax'] = 0.3  # TODO: Move to more general position
    cfg['CutBetaMax'] = 0.1  # TODO: Move to more general position if necessary
    cfg['GenJets'] = 'ak4GenJetsNoNu'
    cfg['UseKLVGenJets'] = True  # Need to be true! DO NOT CHANGE!

    # -- process keyword arguments

    # 'JEC': if provided, point to JEC file in ../JECDatabase
    try:
        _jec_string = kwargs['JEC']
    except KeyError:
        print " WARNING! Keyword argument `JEC` to `getBaseConfig` was not given. cfg['Jec'] must be set manually..."
    else:
        cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/{0}_MC/{0}_MC'.format(_jec_string))

    # 'JER': if provided, point to JER file in ../JRDatabase
    _jer_string = kwargs.get('JER', None)
    if _jer_string is not None:
        cfg['JER'] = os.path.join(configtools.getPath(), '../JRDatabase/textFiles/{0}_MC/{0}_MC'.format(_jer_string))
        cfg['JERMethod'] = "stochastic"  # options: "hybrid" or "stochastic"
        cfg['JERSmearerSeed'] = 92837465

        # insert smearer and sorter after the matching producer
        cfg['Processors'][cfg['Processors'].index("producer:RecoJetGenJetMatchingProducer")+1:1] = ["producer:JERSmearer", "producer:JetSorter"]


def _2016(cfg, **kwargs):
    cfg['Pipelines']['default']['Processors'] += ['filter:JetIDCut',] # if you want to use object-based JetID selection, use 'JetID' in cfg
    cfg['CutJetID'] = 'loose'  # choose event-based JetID selection
    cfg['CutJetIDVersion'] = 2016  # for event-based JetID
    cfg['CutJetIDFirstNJets'] = 2
    cfg['Year'] = 2016
    cfg['Energy'] = 13
    cfg['JetIDVersion'] = 2016  # for object-based JetID
    # cfg['PUJetID'] = 'loose'
    cfg['MinPUJetID'] = -9999
    cfg['MinZllJetDeltaRVeto'] = 0.3
    cfg['JetLeptonLowerDeltaRCut'] = 0.3 # JetID 2015 does not veto muon contribution - invalidate any jets that are likely muons; requires ZmmProducer and ValidZllJetsProducer to work
    # create empty containers to allow using references prematurely
    cfg["InputFiles"] = configtools.InputFiles()
    # data settings also used to derive values for mc
    cfg['Minbxsec'] = 69.2
    cfg['NPUFile'] = os.path.join(configtools.getPath(),'data/pileup/pumean_data2016_13TeV.txt')
    cfg['NPUSmearing'] = True
    cfg['NPUSmearingSeed'] = 1
    # TODO: Use official CERT naming
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_BCDEFGH_13TeV_23Sep2016ReReco_Collisions16_JSON.txt')]


def _2017(cfg, **kwargs):
    cfg['Pipelines']['default']['Processors'] += ['filter:JetIDCut',] # if you want to use object-based JetID selection, use 'JetID' in cfg
    cfg['CutJetID'] = 'tightlepveto'  # choose event-based JetID selection
    cfg['CutJetIDVersion'] = 2017  # for event-based JetID
    cfg['CutJetIDFirstNJets'] = 2
    cfg['Year'] = 2017
    cfg['Energy'] = 13
    cfg['JetIDVersion'] = 2017  # for object-based JetID
    cfg['MinPUJetID'] = -9999  # no PUJetID for 2017
    cfg['MinZllJetDeltaRVeto'] = 0.3
    cfg['JetLeptonLowerDeltaRCut'] = 0.3 # JetID 2015 does not veto muon contribution - invalidate any jets that are likely muons; requires ZmmProducer and ValidZllJetsProducer to work
    # create empty containers to allow using references prematurely
    cfg["InputFiles"] = configtools.InputFiles()
    # data settings also used to derive values for mc
    cfg['Minbxsec'] = 69.2
    cfg['NPUFile'] = os.path.join(configtools.getPath(), 'data/pileup/pumean_data2017_13TeV.txt')
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt')]

def _2018(cfg, **kwargs):
    _2017(cfg, **kwargs)  # user 2017 config as base
    cfg['JetIDVersion'] = 2018  # for object-based JetID
    cfg['CutJetIDVersion'] = 2018  # for event-based JetID
    cfg['Year'] = 2018
    cfg['NPUFile'] = os.path.join(configtools.getPath(), 'data/pileup/pumean_data2018_13TeV.txt')
    cfg['JsonFiles'] = [os.path.join(configtools.getPath(), 'data/json/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt')]


def data_2016(cfg, **kwargs):
    _jec_iov = kwargs['IOV']  # mandatory kwarg indicating IOV (interval of validity)
    # (for selecting the right jet eta-phi cleaning file)

    # object-based eta-phi cleaning (recommended jul. 2018)
    # -> invalidate jets according to eta-phi masks provided in a external ROOT file
    cfg['Processors'].insert(cfg['Processors'].index("producer:ZJetCorrectionsProducer") + 1, "producer:JetEtaPhiCleaner")
    cfg['JetEtaPhiCleanerFile'] = os.path.join(configtools.getPath(), "data/cleaning/jec16/data16_07Aug2017_Legacy/hotjets-run{}.root".format(_jec_iov))
    cfg['JetEtaPhiCleanerHistogramNames'] = ["h2hotfilter"]
    cfg['JetEtaPhiCleanerHistogramValueMaxValid'] = 9.9   # >=10 means jets should be invalidated


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

def data_2018(cfg, **kwargs):
    # no data customization for 2018 (yet)
    pass

def mc_2016(cfg, **kwargs):
    # TODO: move PUWeightFile here if possible
    
    # object-based eta-phi cleaning (recommended jul. 2018)
    # -> invalidate jets according to eta-phi masks provided in a external ROOT file
    cfg['Processors'].insert(cfg['Processors'].index("producer:ZJetCorrectionsProducer") + 1, "producer:JetEtaPhiCleaner")
    cfg['JetEtaPhiCleanerFile'] = os.path.join(configtools.getPath(), "data/cleaning/jec16/data16_07Aug2017_Legacy/hotjets-run{}.root".format(_jec_iov))
    cfg['JetEtaPhiCleanerHistogramNames'] = ["h2hotfilter"]
    cfg['JetEtaPhiCleanerHistogramValueMaxValid'] = 9.9   # >=10 means jets should be invalidated

def mc_2017(cfg, **kwargs):
    # TODO: move PUWeightFile here if possible

    # object-based eta-phi cleaning (recommended jun. 2018)
    # -> invalidate jets according to eta-phi masks provided in a external ROOT file
    cfg['Processors'].insert(cfg['Processors'].index("producer:ZJetCorrectionsProducer") + 1, "producer:JetEtaPhiCleaner")
    cfg['JetEtaPhiCleanerFile'] = os.path.join(configtools.getPath(), "data/cleaning/jec17/data17_17Nov2017_ReReco/hotjets-17runBCDEF_addEtaPhiMask_2018-06-11.root")
    cfg['JetEtaPhiCleanerHistogramNames'] = ["h2hotfilter", "h2_additionalEtaPhiFilter"]
    cfg['JetEtaPhiCleanerHistogramValueMaxValid'] = 9.9   # >=10 means jets should be invalidated

def mc_2018(cfg, **kwargs):
    # no MC customization for 2018 (yet)
    pass

def ee(cfg, **kwargs):
    cfg['Electrons'] = 'electrons'
    cfg['ElectronMetadata'] = 'electronMetadata'
    # The order of these producers is important!
    cfg['Processors'] = ['producer:ZJetValidElectronsProducer', 'producer:ZeeProducer',]+cfg['Processors']

    cfg['Pipelines']['default']['Processors'] = [
        'filter:MinElectronsCountFilter',
        'filter:MaxElectronsCountFilter',
        'filter:ElectronPtCut',
        'filter:ElectronEtaCut',
        ### TODO: Move to baseconfig
        # 'filter:ZFilter',  # TODO: Check what this filter does
        'filter:ValidZCut',  # includes Z mass cut
        'filter:ZPtCut',
        'filter:ValidJetsFilter',
        'filter:LeadingJetPtCut',
        'filter:LeadingJetEtaCut',
        'filter:LeadingJetYCut',
        'filter:AlphaCut',
        'filter:BackToBackCut',
        ###
        ]
    cfg['Pipelines']['default']['Consumers'] += ['KappaElectronsConsumer',]

    cfg['ElectronID'] = 'tight' # OLD electron ID code: set to 'none' or 'user' if using VID, overwritten below
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
        'e1idloose', 'e1idmedium', 'e1idtight', #'e1idveto', # 'e1mvanontrig', 'e1mvatrig',
        'e2pt', 'e2eta', 'e2phi',
        'e2idloose', 'e2idmedium', 'e2idtight', #'e2idveto', # 'e2mvanontrig', 'e2mvatrig',
        'nelectrons', 'validz',
        ]
    cfg['MinNElectrons'] = 2
    cfg['MaxNElectrons'] = 3
    cfg['CutElectronPtMin'] = 25.0
    cfg['CutElectronEtaMax'] = 2.4
    cfg['CutLeadingJetPtMin'] = 12.0
    cfg['CutLeadingJetEtaMax'] = 1.3
    cfg['CutLeadingJetYMax'] = 2.4
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
    cfg['Processors'].insert(cfg['Processors'].index('producer:ValidZllGenJetsProducer'), 'producer:GenZeeProducer',)
    cfg['Processors'] += ['producer:RecoElectronGenParticleMatchingProducer']
    cfg['RecoElectronMatchingGenParticleStatus'] = 1  # take Pythia8 status 1 as default here
    # cfg['RecoElectronMatchingGenParticleStatus'] = 3
    cfg['DeltaRMatchingRecoElectronGenParticle'] = 0.3
    cfg["RecoElectronMatchingGenParticlePdgIds"] = [11, -11]
    cfg["InvalidateNonGenParticleMatchingRecoElectrons"] = False
    cfg['GenParticleTypes'] += ['genElectron']
    cfg['GenElectronStatus'] = 1  # take Pythia8 status 1 as default here
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


def _2016ee(cfg, **kwargs):
    # -- ZJetValidElectronsProducer
    cfg['ElectronID'] = "user"
    cfg['ApplyElectronVID'] = True
    cfg['ElectronVIDName'] = "Summer16-80X-V1"
    cfg['ElectronVIDType'] = "cutbased"
    cfg['ElectronVIDWorkingPoint'] = "tight"

    # -- double electron triggers:
    cfg['HltPaths']= [
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
        'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL',
        'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL']


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

def _2018ee(cfg, **kwargs):
    _2017ee(cfg, **kwargs)  # use 2017 as base
    cfg['ElectronVIDName'] = "Fall17-94X-V1"


def data_2016ee(cfg, **kwargs):
    pass


def data_2017ee(cfg, **kwargs):
    pass


def mc_2016ee(cfg, **kwargs):
    pass


def mc_2017ee(cfg, **kwargs):
    pass


def mm(cfg, **kwargs):
    cfg['Muons'] = 'muons'
    # The order of these producers is important!
    cfg['Processors'] = [   #'producer:MuonCorrectionsProducer',
                            #'producer:PFCandidatesProducer',
                            'producer:ValidMuonsProducer',
                            'producer:RecoZmmProducer',
                            ]+cfg['Processors']
    cfg['Pipelines']['default']['Processors'] = [
        #'filter:ValidJetsFilter',
        'filter:LeadingJetPtCut',
        'filter:LeadingJetEtaCut',
        'filter:MinNMuonsCut',
        'filter:MaxNMuonsCut',
        'filter:MuonPtCut',
        'filter:MuonEtaCut',
        #'filter:ZFilter', # name has to end with 'Cut' :-P
        'filter:ValidZCut', # includes Z mass cut
        'filter:ZPtCut',
        'filter:LeadingJetYCut',
        'filter:AlphaCut',
        'filter:BackToBackCut',
        ]
    cfg['Pipelines']['default']['Consumers'] += ['KappaMuonsConsumer',]
    # In case of Muon Corrections
    #cfg['ValidMuonsInput'] = "corrected" # is this really doing something???

    # validMuonsProducer
    cfg['MuonID'] = 'tight'
    cfg['MuonIso'] = 'tight'
    cfg['MuonIsoType'] = 'pf'
    #cfg['UseHighPtID'] = True
    cfg['MaxZJetDressedMuonDeltaR'] = 0.1

    cfg['Pipelines']['default']['Quantities'] += [
        'mupluspt', 'mupluseta', 'muplusphi', 'muplusmass', 'muplusiso',
        'muminuspt', 'muminuseta', 'muminusphi', 'muminusmass', 'muminusiso',
        # 'mu1pt', 'mu1eta', 'mu1phi', 'mu1mass',
        # 'mu1iso', 'mu1sumchpt', 'mu1sumnhet', 'mu1sumpet', 'mu1sumpupt',
        # 'mu2pt', 'mu2eta', 'mu2phi', 'mu2mass',
        # 'mu3pt', 'mu3eta', 'mu3phi', 'mu3mass',
        'nmuons', # 'validz',  # check by pT of Z
        # 'leptonSFWeight','leptonTriggerSFWeight',
        # 'mu1idloose','mu1idmedium','mu1idtight',
        # 'mu2idloose','mu2idmedium','mu2idtight',
        ]
    cfg['CutNMuonsMin'] = 2
    cfg['CutNMuonsMax'] = 3  # TODO: Remove, if not too much muons in collection
    cfg['CutMuonPtMin'] = 20.0
    cfg['CutMuonEtaMax'] = 2.3
    cfg['CutLeadingJetPtMin'] = 12.0
    cfg['CutLeadingJetEtaMax'] = 1.3
    cfg['CutLeadingJetYMax'] = 2.4
    cfg['CutBackToBack'] = 0.34
    cfg['CutAlphaMax'] = 0.3
    cfg['CutZPtMin'] = 30.0

#Efficiency calculation
    cfg["InvalidateNonMatchingMuons"] = False  # TODO: Check functionality
    cfg["TriggerObjects"] = "triggerObjects"
    cfg["TriggerInfos"] = "triggerObjectMetadata"
    cfg['MuonPtVariationFactor'] = 1.00  # TODO: Check functionality
    cfg['TriggerSFRuns'] = []  # TODO: Check functionality


def mcmm(cfg, **kwargs):
    cfg['Pipelines']['default']['Quantities'] += [
        # 'matchedgenmuon1pt',#'matchedgenmuon1eta','matchedgenmuon1phi',  # TODO: change to muplus and muminus
        # 'matchedgenmuon2pt',#'matchedgenmuon2eta','matchedgenmuon2phi',
        'ngenmuons',
        'genmupluspt', 'genmupluseta', 'genmuplusphi', 'genmuplusmass',
        'genmuminuspt','genmuminuseta','genmuminusphi','genmuminusmass',
        # 'genmu1pt','genmu1eta','genmu1phi','genmu1mass',
        # 'genmu2pt','genmu2eta','genmu2phi','genmu2mass',
        ]
    cfg['Processors'].insert(cfg['Processors'].index('producer:ValidZllGenJetsProducer'), 'producer:GenZmmProducer',)
    cfg['Processors'] += [
    #        'producer:GenZmmProducer', #Use this for Status 1 muons
            #'producer:ValidGenZmmProducer', #Use this for original muons  # TODO: get working
            'producer:RecoMuonGenParticleMatchingProducer',  # TODO: Check order of producers
            ]
    cfg['Pipelines']['default']['Processors'] += [
        'filter:MinNGenMuonsCut',
        'filter:MaxNGenMuonsCut',
        'filter:GenMuonPtCut',
        'filter:GenMuonEtaCut',
        'filter:ValidGenZCut',
        'filter:GenZPtCut',
        'filter:LeadingGenJetYCut',
        'filter:LeadingGenJetPtCut',
        ]
    cfg['RecoMuonMatchingGenParticleStatus'] = 1
    cfg['DeltaRMatchingRecoMuonGenParticle'] = 0.5  # TODO: check if lower cut is more reasonable
    cfg['GenParticleTypes'] += ['genMuon', 'genTau']
    #cfg['GenMuonLowerPtCuts'] = ['27']  # TODO: Check if removable, filter already defined above
    #cfg['GenMuonUpperAbsEtaCuts'] = ['2.3']  # TODO: Check if removable, filter already defined above
    cfg['GenMuonStatus'] = 1

    # for KappaMuonsConsumer
    cfg['BranchGenMatchedMuons'] = True
    cfg['AddGenMatchedTaus'] = False
    cfg['AddGenMatchedTauJets'] = False


def _2016mm(cfg, **kwargs):
    cfg['HltPaths'] = ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ']


def _2017mm(cfg, **kwargs):
    cfg['HltPaths'] = [
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ',
        'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ',
        # -- lowest pT unprescaled trigger for the whole of 2017
        # https://indico.cern.ch/event/682891/contributions/2810364/attachments/1570825/2477991/20171206_CMSWeek_MuonHLTReport_KPLee_v3_1.pdf
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8',
    ]

def _2018mm(cfg, **kwargs):
    _2017mm(cfg, **kwargs)  # same as 2017
    cfg['Year'] = 2017  # 2018 muon ID not implemented yet -> reset to 2017 as workaround


def data_2016mm(cfg, **kwargs):
    # TODO: move activation of SFProducer to kwargs:
    # for now: activate if necessary!
    #cfg['Pipelines']['default']['Processors'] += ['producer:LeptonIDSFProducer','producer:LeptonIsoSFProducer','producer:LeptonTriggerSFProducer']#,'producer:LeptonSFProducer',]
    #cfg['Pipelines']['default']['Quantities'] += ['leptonIDSFWeight','leptonIsoSFWeight','leptonTriggerSFWeight']
    #cfg['Pipelines']['default']['Quantities'] += ['zl1IDSFWeight','zl1IsoSFWeight','zl1TriggerSFWeight','zl2IDSFWeight','zl2IsoSFWeight','zl2TriggerSFWeight']
    cfg['LeptonIDSFHistogramName'] = 'NUM_TightID_DEN_genTracks_eta_pt'
    cfg['LeptonIsoSFHistogramName'] = 'NUM_LooseRelIso_DEN_TightIDandIPCut_eta_pt'
    cfg['LeptonTriggerSFHistogramName'] = 'IsoMu24_OR_IsoTkMu24_PtEtaBins/efficienciesDATA/abseta_pt_DATA'
    ### Get Root file from POG ### information on https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults ###
    ### files from https://gitlab.cern.ch/cms-muonPOG/MuonReferenceEfficiencies/tree/master/EfficienciesStudies ###
    cfg['LeptonIDSFRootfile']      = os.path.join(configtools.getPath(),"data/scalefactors/2016/RunBCDEF_SF_ID.root")
    cfg['LeptonIsoSFRootfile']     = os.path.join(configtools.getPath(),"data/scalefactors/2016/RunBCDEF_SF_ISO.root")
    cfg['LeptonTriggerSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016/RunBCDEF_SF_Trigger.root")


def data_2017mm(cfg, **kwargs):
    pass


def mc_2016mm(cfg, **kwargs):
    #cfg['Pipelines']['default']['Processors'] += ['producer:LeptonIDSFProducer','producer:LeptonIsoSFProducer','producer:LeptonTriggerSFProducer']#,'producer:LeptonSFProducer',]
    #cfg['Pipelines']['default']['Quantities'] += ['leptonIDSFWeight','leptonIsoSFWeight','leptonTriggerSFWeight']
    #cfg['Pipelines']['default']['Quantities'] += ['zl1IDSFWeight','zl1IsoSFWeight','zl1TriggerSFWeight','zl2IDSFWeight','zl2IsoSFWeight','zl2TriggerSFWeight']
    cfg['LeptonIDSFHistogramName'] = 'MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/efficienciesMC/abseta_pt_MC'
    cfg['LeptonIsoSFHistogramName'] = 'LooseISO_TightID_pt_eta/efficienciesMC/pt_abseta_MC'
    cfg['LeptonTriggerSFHistogramName'] = 'IsoMu24_OR_IsoTkMu24_PtEtaBins/efficienciesMC/abseta_pt_MC'
    cfg['LeptonIDSFRootfile']      = os.path.join(configtools.getPath(),"data/scalefactors/2016outdated/ID_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonIsoSFRootfile']     = os.path.join(configtools.getPath(),"data/scalefactors/2016outdated/Iso_EfficienciesAndSF_BCDEF.root")
    cfg['LeptonTriggerSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016outdated/Trigger_EfficienciesAndSF_BCDEF.root")


def mc_2017mm(cfg, **kwargs):
    pass
