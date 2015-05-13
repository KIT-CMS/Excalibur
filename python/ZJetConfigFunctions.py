import ZJetConfigBase

def getBaseConfig(**kwargs):
	cfg = {
		'SkipEvents': 0,
		'EventCount': -1,
		'Processors': [],
		'InputFiles': [],  # Overwritten by (data/mc).py, excalibur.py, json_modifier.py (if run in batch mode)
		'OutputPath': 'out', # Overwritten by excalibur.py
		# ZJetCorrectionsProducer Settings
		'Jec': '', # Path for JEC data, please set this later depending on input type
		'L1Correction': 'L1FastJet',
		'RC': False,  # Also provide random cone offset JEC, and use for type-I
		'FlavourCorrections': False,  # Calculate additional MC flavour corrections
		# ZProducer Settings
		'ZMassRange': 20.,
		# TypeIMETProducer Settings
		'Met' : 'met', # metCHS will be selected automaticly if CHS jets are requested in TaggedJets
		'JetPtMin': 10.,
		'EnableMetPhiCorrection': False,
		'MetPhiCorrectionParameters': [], # Please set this later depending on input type
		# Valid Jet Selection
		'ValidJetsInput': 'uncorrected',
		'JetID' : 'tight',
		'JetIDVersion' : 2014,
		'JetMetadata' : 'jetMetadata',
		'TaggedJets' : 'AK5PFTaggedJetsCHS',
		# PU
		'PileupDensity' : 'KT6Area',
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
				'Processors': [ # Overwritten/cleaned by expand function, set cuts in data.py or mc.py
					'filter:MuonPtCut',
					'filter:MuonEtaCut',
					'filter:LeadingJetPtCut',
					'filter:LeadingJetEtaCut',
					'filter:AlphaCut',
					'filter:ZPtCut',
					'filter:BackToBackCut',
				],
				'Quantities': [
					# General quantities
					'npv', 'rho', 'weight', #'nputruth',
					'njets', 'njetsinv',  # number of valid and invalid jets
					# Z quantities
					'zpt', 'zeta', 'zy', 'zphi', 'zmass',
					# Leading jet
					'jet1pt', 'jet1eta', 'jet1y', 'jet1phi',
					'jet1chf', 'jet1nhf', 'jet1ef',
					'jet1mf', 'jet1hfhf', 'jet1hfemf', 'jet1pf',
					#'jet1unc',  # Leading jet uncertainty
					# Second jet
					'jet2pt', 'jet2eta', 'jet2phi',
					# MET and related
					'mpf', 'rawmpf', 'metpt', 'metphi', 'rawmetpt', 'rawmetphi', 'sumet',
				],
			},
		},

		# Wire Kappa objects
		'EventMetadata' : 'eventInfo',
		'LumiMetadata' : 'lumiInfo',
		'VertexSummary': 'goodOfflinePrimaryVerticesSummary',
	}
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


def mc(cfg, **kwargs):
	cfg['InputIsData'] = False
	cfg['GenJets'] = 'AK5GenJets'
	cfg['Processors'] += [
		'producer:RecoJetGenPartonMatchingProducer',
		'producer:RecoJetGenJetMatchingProducer',
		#'producer:RecoJetGenParticleMatchingProducer',
		#'producer:RecoMuonGenParticleMatchingProducer',
	]
	cfg['GenParticles'] = 'genParticles'
	cfg['Pipelines']['default']['Quantities'] += [
		'genjet1pt',
		'genjet1eta',
		'genjet1phi',
		'genjet2pt',
		'matchedgenparton1pt',
		'matchedgenparton1flavour',
		'matchedgenparton2pt',
		'matchedgenjet1pt',
		'matchedgenjet2pt',
	]

	# RecoJetGenParticleMatchingProducer Settings
	cfg['DeltaRMatchingRecoJetGenParticle'] = 0.3
	cfg['JetMatchingAlgorithm'] = 'physics' # algorithmic or physics

	# RecoJetGenJetMatchingProducer Settings
	cfg['DeltaRMatchingRecoJetGenJet'] = 0.25

##
##


def _2011(cfg, **kwargs):
	cfg['Year'] = 2011


def _2012(cfg, **kwargs):
	cfg['Year'] = 2012


##
##


def ee(cfg, **kwargs):
	pass

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
		'producer:ZProducer',
		'filter:ZFilter',
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
		'mu2pt', 'mu2eta', 'mu2phi',
		'nmuons',
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
	cfg['Jec'] = ZJetConfigBase.getPath() + '/data/jec/Winter14_V8/Winter14_V8_DATA'
	cfg['JsonFiles'] = [ZJetConfigBase.getPath() + '/data/json/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt']
	cfg['MetPhiCorrectionParameters'] = [0.2661, 0.3217, -0.2251, -0.1747]

def mc_2011(cfg, **kwargs):
	pass

def mc_2012(cfg, **kwargs):
	cfg['Jec'] = ZJetConfigBase.getPath() + '/data/jec/Winter14_V8/Winter14_V8_MC'
	cfg['MetPhiCorrectionParameters'] = [0.1166, 0.0200, 0.2764, -0.1280]


def mcee(cfg, **kwargs):
	pass


def _2011mm(cfg, **kwargs):
	pass

def _2012mm(cfg, **kwargs):
	pass


##
##

def mc_2011mm(cfg, **kwargs):
	pass


def mc_2012ee(cfg, **kwargs):
	pass


def mc_2012mm(cfg, **kwargs):
	pass


def data_2011mm(cfg, **kwargs):
	pass


def data_2012mm(cfg, **kwargs):
	cfg['HltPaths'] = ['HLT_Mu17_Mu8_v%d' % v for v in range(1, 30)]


def data_2012ee(cfg, **kwargs):
	pass


def data_2012em(cfg, **kwargs):
	pass
