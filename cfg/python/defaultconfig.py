import configtools

def getBaseConfig(tagged=True, **kwargs):
	cfg = {
		# Artus General Settings
		'ProcessNEvents': -1,
		'FirstEvent': 0,
		'Processors': [],
		'InputFiles': [],  # Overwritten by (data/mc).py, excalibur.py, json_modifier.py (if run in batch mode)
		'OutputPath': 'out', # Overwritten by excalibur.py
		# ZJetCorrectionsProducer Settings
		'Jec': '', # Path for JEC data, please set this later depending on input type
		'L1Correction': 'L1FastJet',
		'RC': True,  # Also provide random cone offset JEC, and use for type-I
		'FlavourCorrections': False,  # Calculate additional MC flavour corrections
		'ProvideResidualCorrections': False,
		# ZProducer Settings
		'ZMassRange': 20.,
		# TypeIMETProducer Settings
		'Met' : 'met', # metCHS will be selected automaticly if CHS jets are requested in TaggedJets
		'JetPtMin': 10.,
		'EnableMetPhiCorrection': False,
		'MetPhiCorrectionParameters': [], # Please set this later depending on input type
		# Valid Jet Selection
		'ValidJetsInput': 'uncorrected',
		'JetID' : 'loose',
		'JetIDVersion' : "73X",
		'JetMetadata' : 'jetMetadata',
		'TaggedJets' : 'ak5PFJetsCHS',
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
					'npv', 'rho', 'weight', #'nputruth',
					'njets', 'njetsinv',  # number of valid and invalid jets
					# Z quantities
					'zpt', 'zeta', 'zeta', 'zy', 'zphi', 'zmass',
					# Leading jet
					'jet1pt', 'jet1eta', 'jet1y', 'jet1phi',
					'jet1chf', 'jet1nhf', 'jet1ef',
					'jet1mf', 'jet1hfhf', 'jet1hfemf', 'jet1pf',
					'jet1area',
					
					'jet1l1', 'jet1rc', 'jet1l2',
					'jet1ptraw', 'jet1ptl1',
					#'jet1unc',  # Leading jet uncertainty
					# Second jet
					'jet2pt', 'jet2eta', 'jet2phi',
					# 3rd jet
					'jet3pt', 'jet3eta', 'jet3phi',
					# MET and related
					'mpf', 'rawmpf', 'met', 'metphi', 'rawmet', 'rawmetphi', 'sumet',
				],
			},
		},

		# Wire Kappa objects
		'EventMetadata' : 'eventInfo',
		'LumiMetadata' : 'lumiInfo',
		'VertexSummary': 'goodOfflinePrimaryVerticesSummary',
	}
	if tagged:
		cfg['Pipelines']['default']['Quantities'] += ['jet1btag', 'jet1qgtag']
	return cfg

##
##


def data(cfg, **kwargs):
	cfg['InputIsData'] = True
	cfg['Pipelines']['default']['Quantities'] += ['run', 'event', 'lumi']
	cfg['Processors'] += [
		'filter:JsonFilter',
		'producer:HltProducer',
		'filter:HltFilter',
	]
	cfg['ProvideResidualCorrections'] = True
	cfg['Pipelines']['default']['Quantities'] += ['jet1ptl1l2l3', 'jet1res']


def mc(cfg, **kwargs):
	cfg['InputIsData'] = False
	cfg['Processors'] += [
		'producer:RecoJetGenPartonMatchingProducer',
		'producer:RecoJetGenJetMatchingProducer',
		'producer:GenParticleProducer',
	]
	cfg['GenParticles'] = 'genParticles'
	cfg['Pipelines']['default']['Quantities'] += [
		'npu',
		'npumean',
		'genjet1pt',
		'genjet1eta',
		'genjet1phi',
		'genjet2pt',
		'genjet2eta',
		'genjet2phi',
		'matchedgenparton1pt',
		'matchedgenparton1flavour',
		'matchedgenparton2pt',
		'matchedgenjet1pt',
		'matchedgenjet2pt',
		'genzpt',
		'genzeta',
		'genzphi',
		'genzeta',
		'genzy',
		'genzmass',
		'deltarzgenz',
	]

	# RecoJetGenPartonMatchingProducer Settings
	cfg['DeltaRMatchingRecoJetGenParticle'] = 0.3
	cfg['JetMatchingAlgorithm'] = 'physics' # algorithmic or physics

	# RecoJetGenJetMatchingProducer Settings
	cfg['DeltaRMatchingRecoJetGenJet'] = 0.3

	# GenParticleProducer
	cfg['GenParticleTypes'] = ['genParticle']
	cfg['GenParticlePdgIds'] = [23] # Z
	cfg['GenParticleStatus'] = 2


	# MC sample reweighting
	cfg['Processors'] += [
		'producer:CrossSectionWeightProducer',
		'producer:ZJetNumberGeneratedEventsWeightProducer',
		'producer:EventWeightProducer',
	]
	cfg['Pipelines']['default']['Quantities'] += [
		'numberGeneratedEventsWeight',
		'crossSectionPerEventWeight',
	]
	cfg['EventWeight'] = 'weight'
	cfg['CrossSection'] = -1
	cfg['BaseWeight'] = 1000

##
##


def _2011(cfg, **kwargs):
	cfg['Year'] = 2011
	cfg['Energy'] = 7


def _2012(cfg, **kwargs):
	cfg['Year'] = 2012
	cfg['Energy'] = 8
	cfg['JetIDVersion'] = 2014

def _2015(cfg, **kwargs):
	cfg['Year'] = 2015
	cfg['Energy'] = 13
	cfg['TaggedJets'] = 'ak4PFJetsCHS'
	cfg['PileupDensity'] = 'pileupDensity'


##
##


def ee(cfg, **kwargs):
	cfg['Electrons'] = 'correlectrons'
	cfg['ElectronMetadata'] = 'electronMetadata'
	cfg['Processors'] = [
		'producer:ValidElectronsProducer',
		'filter:MinElectronsCountFilter',
		'filter:MaxElectronsCountFilter',
		'producer:ValidTaggedJetsProducer',
		'filter:ValidJetsFilter',
		'producer:ZJetCorrectionsProducer',
		'producer:TypeIMETProducer',
		'producer:JetSorter',
		'producer:ZeeProducer',
		'filter:ZFilter',
		'producer:RadiationJetProducer',
	]
	cfg['ElectronID'] = 'none'
	cfg['ElectronIsoType'] = 'none'
	cfg['ElectronIso'] = 'none'
	cfg['ElectronReco'] = 'none'
	
	cfg['MinNElectrons'] = 2
	cfg['MaxNElectrons'] = 3

	cfg['CutElectronPtMin'] = 25.0
	cfg['CutElectronEtaMax'] = 2.4
	cfg['CutLeadingJetPtMin'] = 12.0
	cfg['CutLeadingJetEtaMax'] = 1.3
	cfg['CutZPtMin'] = 30.0
	cfg['CutBackToBack'] = 0.34
	cfg['CutAlphaMax'] = 0.2
	cfg['ZMassRange'] = 10

	cfg['Pipelines']['default']['Quantities'] += [
		'epluspt', 'epluseta', 'eplusphi', 'eplusiso',
		'eminuspt', 'eminuseta', 'eminusphi', 'eminusiso',
		'e1pt', 'e1eta', 'e1phi', 'e1looseid', 'e1mediumid', 'e1tightid', 'e1vetoid',
		'e1looseid95', 'e1mediumid95', 'e1tightid95', 'e1mvanontrig', 'e1mvatrig',
		'e2pt', 'e2eta', 'e2phi', 'e2looseid', 'e2mediumid', 'e2tightid', 'e2vetoid',
		'e2looseid95', 'e2mediumid95', 'e2tightid95', 'e2mvanontrig', 'e2mvatrig',
		'nelectrons',
		'njets30',
	]
	cfg['Pipelines']['default']['Processors'] = [
		'filter:ElectronPtCut',
		'filter:ElectronEtaCut',
		'filter:LeadingJetPtCut',
		'filter:LeadingJetEtaCut',
		'filter:AlphaCut',
		'filter:ZPtCut',
		'filter:BackToBackCut',
	]
	cfg['Pipelines']['default']['Consumers'] += [
		'KappaElectronsConsumer',
	]

def em(cfg, **kwargs):
	pass

def mm(cfg, **kwargs):
	cfg['Muons'] = 'muons'
	# The order of these producers is important!
	cfg['Processors'] = [
		'producer:ValidMuonsProducer',
		'filter:MinNMuonsCut',
		'filter:MaxNMuonsCut',
		#'producer:MuonCorrectionsProducer', # Is not doing anything yet
		'producer:ValidTaggedJetsProducer',
		'filter:ValidJetsFilter',
		'producer:ZJetCorrectionsProducer',
		'producer:TypeIMETProducer',
		'producer:JetSorter',
		'producer:ZmmProducer',
		'filter:ZFilter',
		'producer:RadiationJetProducer',
	]
	cfg['Pipelines']['default']['Processors'] = [
		'filter:MuonPtCut',
		'filter:MuonEtaCut',
		'filter:LeadingJetPtCut',
		'filter:LeadingJetEtaCut',
		'filter:AlphaCut',
		'filter:ZPtCut',
		'filter:BackToBackCut',
	]
	
	# ValidMuonsProducer
	cfg['MuonID'] = 'tight'
	cfg['MuonIso'] = 'tight'
	cfg['MuonIsoType'] = 'pf'
	cfg['DirectIso'] = True

	cfg['Pipelines']['default']['Quantities'] += [
		'mupluspt', 'mupluseta', 'muplusphi', 'muplusiso',
		'muminuspt', 'muminuseta', 'muminusphi', 'muminusiso',
		'mu1pt', 'mu1eta', 'mu1phi',
		'mu1iso', 'mu1sumchpt', 'mu1sumnhet', 'mu1sumpet', 'mu1sumpupt',
		'mu2pt', 'mu2eta', 'mu2phi',
		'nmuons',
		'radiationjet1pt', 'radiationjet1phi', 'radiationjet1eta',
		'radiationjet1index', 'nradiationjets'
	]

	cfg['CutMuonPtMin'] = 20.0
	cfg['CutMuonEtaMax'] = 2.3
	cfg['CutLeadingJetPtMin'] = 12.0
	cfg['CutLeadingJetEtaMax'] = 1.3
	cfg['CutZPtMin'] = 30.0
	cfg['CutBackToBack'] = 0.34
	cfg['CutAlphaMax'] = 0.2


###
###


def data_2011(cfg, **kwargs):
	pass

def data_2012(cfg, **kwargs):
	cfg['Jec'] = configtools.getPath() + '/data/jec/Winter14_V8/Winter14_V8_DATA'
	cfg['JsonFiles'] = [configtools.getPath() + '/data/json/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt']
	cfg['Lumi'] = 19.712
	cfg['MetPhiCorrectionParameters'] = [0.2661, 0.3217, -0.2251, -0.1747]

	cfg['Processors'] += ['producer:NPUProducer']
	cfg['Minbxsec'] = 68.5
	cfg['NPUFile'] = configtools.getPath() + '/data/pileup/pumean_pixelcorr_data2012.txt'
	cfg['Pipelines']['default']['Quantities'] += ['npumeandata']


def data_2015(cfg, **kwargs):
	cfg['Jec'] = configtools.getPath() + '/data/jec/Summer15_50nsV2_MC/Summer15_50nsV2_MC'
	#json file from /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV
	cfg['JsonFiles'] = [configtools.getPath() + '/data/json/Cert_246908-251883_13TeV_PromptReco_Collisions15_JSON_v2.txt']
	cfg['Lumi'] = 0.00559

def mc_2011(cfg, **kwargs):
	cfg['GenJets'] = 'AK5GenJetsNoNu'
	pass

def mc_2012(cfg, **kwargs):
	cfg['GenJets'] = 'AK5GenJetsNoNu'
	cfg['Jec'] = configtools.getPath() + '/data/jec/Winter14_V8/Winter14_V8_MC'
	cfg['MetPhiCorrectionParameters'] = [0.1166, 0.0200, 0.2764, -0.1280]
	# insert PU weight producer before EventWeightProducer:
	cfg['Processors'].insert(cfg['Processors'].index('producer:EventWeightProducer'), 'producer:PUWeightProducer')
	cfg['PileupWeightFile'] = configtools.getPath() + '/data/pileup/weights_190456-208686_8TeV_22Jan2013ReReco_madgraphPU-RD.root'
	cfg['Pipelines']['default']['Quantities'] += ['puWeight']

def mc_2015(cfg, **kwargs):
	cfg['GenJets'] = 'ak4GenJetsNoNu'
	cfg['Jec'] = configtools.getPath() + '/data/jec/Summer15_50nsV2_MC/Summer15_50nsV2_MC'

def mcee(cfg, **kwargs):
	cfg['Pipelines']['default']['Quantities'] += [
		'ngenelectrons',
		'matchedgenelectron1pt',
		'matchedgenelectron2pt',
		'ngenelectrons',
		'genepluspt',
		'genepluseta',
		'geneplusphi',
		'geneminuspt',
		'geneminuseta',
		'geneminusphi',
		'genParticleMatchDeltaR',
	]
	# reco-gen electron matching producer
	cfg['Processors'] += ['producer:RecoElectronGenParticleMatchingProducer']
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

	# electron data/mc scale factors
	if cfg['ElectronID'] is not 'none':
		cfg['Processors'] += ['producer:ElectronSFProducer']
		cfg['ElectronSFRootfilePath'] = configtools.getPath() + "/data/electron_scalefactors/"
		cfg['Pipelines']['default']['Quantities'] += ['electronSFWeight']

def mcmm(cfg, **kwargs):
	cfg['Pipelines']['default']['Quantities'] += [
		'matchedgenmuon1pt',
		'matchedgenmuon2pt',
		'ngenmuons',
		'genmupluspt',
		'genmupluseta',
		'genmuplusphi',
		'genmuminuspt',
		'genmuminuseta',
		'genmuminusphi',
	]
	cfg['Processors'] += ['producer:RecoMuonGenParticleMatchingProducer']
	cfg['RecoMuonMatchingGenParticleStatus'] = 1
	cfg['DeltaRMatchingRecoMuonGenParticle'] = 0.5 # TODO: check if lower cut is more reasonable

	cfg['GenParticleTypes'] += ['genMuon']
	cfg['GenMuonStatus'] = 1


def _2011mm(cfg, **kwargs):
	pass

def _2012mm(cfg, **kwargs):
	pass

def _2015mm(cfg, **kwargs):
	cfg['MuonID'] = 'tight'


##
##

def mc_2011mm(cfg, **kwargs):
	pass


def mc_2012ee(cfg, **kwargs):
	cfg['Processors'] += ['producer:HltProducer']
	cfg['HltPaths'] = ['HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v%d' % v for v in range(1, 30)]
	cfg['Pipelines']['default']['Quantities'] += ['hlt']


def mc_2012mm(cfg, **kwargs):
	pass


def data_2011mm(cfg, **kwargs):
	pass


def data_2012mm(cfg, **kwargs):
	cfg['HltPaths'] = ['HLT_Mu17_Mu8_v%d' % v for v in range(1, 30)]

def data_2015mm(cfg, **kwargs):
	cfg['HltPaths'] = ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v%d' % v for v in range(1, 100)]


def data_2012ee(cfg, **kwargs):
	cfg['HltPaths'] = ['HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v%d' % v for v in range(1, 30)]


def data_2012em(cfg, **kwargs):
	pass
