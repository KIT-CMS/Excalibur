import configtools
import os

###
# base config
###
def getBaseConfig(tagged=True, **kwargs):
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
		#'VetoMultipleZs' : False,
		# TypeIMETProducer Settings
		'Met' : 'met', # metCHS will be selected automaticly if CHS jets are requested in TaggedJets
		'TypeIJetPtMin': 15.,
		'EnableMetPhiCorrection': False,
		'MetPhiCorrectionParameters': [], # Please set this later depending on input type
		# Valid Jet Selection	'ValidJetsInput': 'uncorrected',
		'JetID' : 'loose',#'none',#
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
					'zpt', 'zeta', 'zeta', 'zy', 'zphi', 'zmass', 'phistareta', 'zl1pt', 'zl2pt', 'zl1eta', 'zl2eta', 'zl1phi', 'zl2phi',
					# Leading jet
					'jetHT',
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
					'mettype1vecpt', 'mettype1pt',
					'jet1idloose','jet1idmedium','jet1idtight',
					'jet2idloose','jet2idmedium','jet2idtight',
					'jet3idloose','jet3idmedium','jet3idtight',
				],
			},
		},
		# Wire Kappa objects
		'EventMetadata' : 'eventInfo',
		'LumiMetadata' : 'lumiInfo',
		'VertexSummary': 'goodOfflinePrimaryVerticesSummary',
	}

	if tagged:
		cfg['Pipelines']['default']['Quantities'] += ['jet1btag', 'jet1qgtag']#, 'jet1puidraw','jet1puidtight','jet1puidmedium', 'jet1puidloose', 'jet2puidraw', 'jet2puidtight','jet2puidmedium', 'jet2puidloose']
	
	return cfg

def data(cfg, **kwargs):
	cfg['InputIsData'] = True	
	cfg['Processors'] = ['filter:JsonFilter',]+cfg['Processors']+['producer:HltProducer','filter:HltFilter',]
	cfg['Processors'] += ['producer:NPUProducer']
	cfg['ProvideL2L3ResidualCorrections'] = True
	cfg['Pipelines']['default']['Quantities'] += ['jet1ptl1l2l3', 'jet1res']
def mc(cfg, **kwargs):
	cfg['InputIsData'] = False
	cfg['Processors'] += [
		'producer:RecoJetGenPartonMatchingProducer',
		'producer:RecoJetGenJetMatchingProducer',
		'producer:GenParticleProducer',
		'producer:NeutrinoCounter',
	]
	cfg['GenParticles'] = 'genParticles'
	cfg['Pipelines']['default']['Quantities'] += [
		'npu',
		'njets10',	
		'genjet1pt','genjet1eta','genjet1phi',
		'genjet2pt','genjet2eta','genjet2phi',
		'ngenjets','ngenjets10','ngenjets30',
		'matchedgenparton1pt',	'matchedgenparton1flavour','matchedgenparton2pt',
		'matchedgenjet1pt','matchedgenjet1eta','matchedgenjet2pt',
		'genzpt','genzeta','genzphi','genzeta','genzy','genzmass',
		'genzfound','validgenzfound',
		'genzlepton1pt','genzlepton1eta','genzlepton1phi',
		'genzlepton2pt','genzlepton2eta','genzlepton2phi',
		'genphistareta',
		'deltarzgenz', 'deltarjet1genjet1', 'deltarjet2genjet2', 'deltarzl1genzl1', 'deltarzl2genzl2',
		'ngenneutrinos',
		'x1','x2',
		'qScale',		
		'genHT',
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
	cfg['GenZMassRange'] = 20.
	cfg['EventWeight'] = 'weight'
	cfg['CrossSection'] = -1
	cfg['BaseWeight'] = 1000  # pb^-1 -> fb^-1
	cfg['GenJets'] = 'ak4GenJetsNoNu'
	cfg['UseKLVGenJets'] = True
	cfg['GenParticleStatus'] = 22  # see also http://www.phy.pku.edu.cn/~qhcao/resources/CTEQ/MCTutorial/Day1.pdf
	cfg['DeltaRRadiationJet'] = 1
	cfg['CutBetaMax'] = 0.1

	cfg['Processors'].insert(cfg['Processors'].index('producer:EventWeightProducer'), 'producer:GeneratorWeightProducer')
	cfg['Pipelines']['default']['Quantities'] += ['generatorWeight']
	cfg['Processors'].insert(cfg['Processors'].index('producer:EventWeightProducer'), 'producer:PUWeightProducer')
	cfg['Pipelines']['default']['Quantities'] += ['puWeight']
	
def _2016(cfg, **kwargs):
	cfg['Year'] = 2016
	cfg['Energy'] = 13
	cfg['JetIDVersion'] = 2016
	cfg['MinZllJetDeltaRVeto'] = 0.3
	# create empty containers to allow using references prematurely
	cfg["InputFiles"] = configtools.InputFiles()
	cfg['NPUFile'] = os.path.join(configtools.getPath() , 'data/pileup/pumean_data2016_13TeV.txt')
	cfg['JsonFiles'] = os.path.join(configtools.getPath(), 'data/json/Cert_BCDEFGH_13TeV_23Sep2016ReReco_Collisions16_JSON.txt')
	
	###################### has to be checked:
	# data settings also used to derive values for mc
	cfg['JetLeptonLowerDeltaRCut'] = 0.3 # JetID 2015 does not veto muon contribution - invalidate any jets that are likely muons; requires ZmmProducer and ValidZllJetsProducer to work
	cfg['Minbxsec'] =  69.2 # or 71.3???
	#######################
	
def ee(cfg, **kwargs):
	cfg['Electrons'] = 'electrons'
	cfg['ElectronMetadata'] = 'electronMetadata'
	cfg['HltPaths']= ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ', 'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ', 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL', 'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL']
	# The order of these producers is important!
	cfg['Processors'] = [
		# electrons
		'producer:ZJetValidElectronsProducer',
		'filter:MinElectronsCountFilter',
		'filter:MaxElectronsCountFilter',
		# Z
		'producer:ZeeProducer',	
		'filter:ZFilter',
		# jets
		'producer:ValidTaggedJetsProducer',
		'producer:ValidZllJetsProducer',
		'filter:ValidJetsFilter',
		'producer:ZJetCorrectionsProducer',
		'producer:TypeIMETProducer',
		'producer:JetSorter',
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
	cfg['ElectronID'] = 'vbft95_tight'#'tight'#
	cfg['ElectronIsoType'] = 'none'
	cfg['ElectronIso'] = 'none'
	cfg['ElectronReco'] = 'none'	

	cfg['Pipelines']['default']['Quantities'] += [
		'epluspt','epluseta','eplusphi','eplusiso',
		'eminuspt', 'eminuseta', 'eminusphi', 'eminusiso',
		'e1pt', 'e1eta', 'e1phi', 
		'e1idloose', 'e1idmedium', 'e1idtight', 'e1idveto', 'e1idloose95', 'e1idmedium95', 'e1idtight95','e1idveto95',# 'e1mvanontrig', 'e1mvatrig',
		'e2pt', 'e2eta', 'e2phi', 
		'e2idloose', 'e2idmedium', 'e2idtight', 'e2idveto', 'e2idloose95', 'e2idmedium95', 'e2idtight95','e2idveto95',# 'e2mvanontrig', 'e2mvatrig',
		'nelectrons',#'deltare1gene1', 'deltare2gene2',
	]
	cfg['MinNElectrons'] = 2
	cfg['MaxNElectrons'] = 3
	cfg['CutElectronPtMin'] = 25.0
	cfg['CutElectronEtaMax'] = 2.4
	cfg['CutLeadingJetPtMin'] = 12.0
	cfg['CutLeadingJetEtaMax'] = 1.3
	cfg['CutZPtMin'] = 30.0
	cfg['CutBackToBack'] = 0.34
	cfg['CutAlphaMax'] = 0.3
	
def mcee(cfg, **kwargs):
	cfg['Pipelines']['default']['Quantities'] += [
		'ngenelectrons',
		'matchedgenelectron1pt','matchedgenelectron2pt',
		'genepluspt','genepluseta','geneplusphi',
		'geneminuspt','geneminuseta','geneminusphi',
		'genParticleMatchDeltaR',
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
#	cfg['RecoElectronMatchingGenParticleStatus'] = 1
#	cfg[''] = 1

def mm(cfg, **kwargs):
	cfg['Muons'] = 'muons'
	cfg['HltPaths'] = ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ']
	# The order of these producers is important!
	cfg['Processors'] = [
		# muons
#		'producer:MuonCorrectionsProducer',
		'producer:ValidMuonsProducer',
#		'producer:RecoZmmProducer',
		'filter:MinNMuonsCut',
		'filter:MaxNMuonsCut',
		# Z
		'producer:ZmmProducer',
		'filter:ZFilter',
		# jets
		'producer:ValidTaggedJetsProducer',
		'producer:ValidZllJetsProducer',
		'filter:ValidJetsFilter',
		'producer:ZJetCorrectionsProducer',
		'producer:TypeIMETProducer',
		'producer:JetSorter',
	]
	cfg['Pipelines']['default']['Processors'] = [
		#'filter:ValidZCut',
		'filter:MuonPtCut',
		'filter:MuonEtaCut',
		'filter:LeadingJetPtCut',
		'filter:LeadingJetEtaCut',
#		'filter:LeadingLeptonPtCut',
		'filter:AlphaCut',
		'filter:ZPtCut',
		'filter:BackToBackCut',
#		'filter:MuPlusCut',
	]
	cfg['Pipelines']['default']['Consumers'] += [
		'KappaMuonsConsumer',
	]
	cfg['MuonID'] = 'tight'
	cfg['MuonIso'] = 'tight'
	cfg['MuonIsoType'] = 'pf'
	#cfg['UseHighPtID'] = True
	
	cfg['Pipelines']['default']['Quantities'] += [
		'mupluspt', 'mupluseta', 'muplusphi', 'muplusiso',
		'muminuspt', 'muminuseta', 'muminusphi', 'muminusiso',
		'mu1pt', 'mu1eta', 'mu1phi', 'mu1iso', 'mu1sumchpt', 'mu1sumnhet', 'mu1sumpet', 'mu1sumpupt',
		'mu2pt', 'mu2eta', 'mu2phi',
		'nmuons',
		#'leptonSFWeight', 'validz',#'deltarmu1genmu1', 'deltarmu2genmu2',
	]
	cfg['CutNMuonsMin'] = 2
	cfg['CutNMuonsMax'] = 3
	cfg['CutMuonPtMin'] = 20.0
	cfg['CutMuonEtaMax'] = 2.3
	cfg['CutLeadingJetPtMin'] = 12.0
	cfg['CutLeadingJetEtaMax'] = 1.3
	cfg['CutZPtMin'] = 30.0
	cfg['CutBackToBack'] = 0.34
	cfg['CutAlphaMax'] = 0.3
#	cfg['MuonLowerPtCuts'] = ['27']
#	cfg['MuonUpperAbsEtaCuts'] = ['2.3']

#Efficiency calculation
#	cfg["InvalidateNonMatchingMuons"] = False
#	cfg["TriggerObjects"] = "triggerObjects"
#	cfg["TriggerInfos"] = "triggerObjectMetadata"

def mcmm(cfg, **kwargs):
	cfg['Pipelines']['default']['Quantities'] += [
		'matchedgenmuon1pt','matchedgenmuon2pt',
		'ngenmuons',
		'genmupluspt','genmupluseta','genmuplusphi',
		'genmuminuspt','genmuminuseta','genmuminusphi',
#		'leptonTriggerSFWeight',
		'genmu1pt','genmu1eta','genmu1phi',
		'genmu2pt','genmu2eta','genmu2phi',
	]
	cfg['Processors'] += [	#'producer:ZJetGenMuonProducer', 
							'producer:GenZmmProducer', #Use this for Status 1 muons
							#'producer:ValidGenZmmProducer', #Use this for original muons
							'producer:RecoMuonGenParticleMatchingProducer',
	]
	cfg['RecoMuonMatchingGenParticleStatus'] = 1
	cfg['DeltaRMatchingRecoMuonGenParticle'] = 0.5 # TODO: check if lower cut is more reasonable
#	cfg['Processors']+= 'producer:LeptonSFProducer',
	cfg['GenParticleTypes'] += ['genMuon', 'genTau']
	cfg['GenMuonStatus'] = 1
#	cfg['TriggerSFRuns'] = []

	# for KappaMuonsConsumer
	cfg['BranchGenMatchedMuons'] = True
	cfg['AddGenMatchedTaus'] = False
	cfg['AddGenMatchedTauJets'] = False
	
def data_2016(cfg, **kwargs):
	cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/Spring16_25nsV6_DATA/Spring16_25nsV6_DATA')
	
def mc_2016(cfg, **kwargs):
	#cfg['PileupWeightFile'] = configtools.PUWeights(cfg['JsonFiles'],  cfg['InputFiles'],pileup_json="/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt", min_bias_xsec=cfg['Minbxsec'], weight_limits=(0, 4))
	cfg['PileupWeightFile'] = os.path.join(configtools.getPath(),'data/pileup/pileup_weights_BCDEFGH_13TeV_23Sep2016ReReco_Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16.root')
	# use WIP corrections until full tarballs are available again -- MF@20160215
	cfg['Jec'] = os.path.join(configtools.getPath(), '../JECDatabase/textFiles/Spring16_25nsV6_MC/Spring16_25nsV6_MC')

#def _2016mm(cfg, **kwargs):
#	cfg['HltPaths'] = ['HLT_IsoMu24', 'HLT_IsoTkMu24']
#	cfg['MuonRochesterCorrectionsFile'] = os.path.join(configtools.getPath()+'../Artus/KappaAnalysis/data/rochcorr/RoccoR_13tev_2016.txt')
#	cfg['MuonEnergyCorrection'] = 'rochcorr2016'
#	cfg['ValidMuonsInput'] = "corrected"
#	cfg["MuonTriggerFilterNames"] = [	"HLT_IsoMu24_v2:hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09",
#										"HLT_IsoTkMu24_v3:hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09",
	#									"HLT_IsoMu22_v2:hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09",
	#									"HLT_IsoTkMu22_v2:hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09", 
	#									"HLT_IsoTkMu22_v3:hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09", 
	#									"HLT_IsoMu22_v3:hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09",
	#									"HLT_IsoTkMu22_v4:hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09",
#	]
	
#def data_2016mm(cfg, **kwargs):
#	cfg['Pipelines']['default']['Processors'] += ['producer:MuonTriggerMatchingProducer','producer:LeptonSFProducer','producer:LeptonTriggerSFProducer']
#	cfg['MuonPtVariationFactor'] = 1.00
#	cfg['LeptonSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016/SFData_ml.root")
#	cfg['LeptonTriggerSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016/SFTriggerData.root")
#	cfg['TriggerSFRuns'] = [274094,276097]
	
#def mc_2016mm(cfg, **kwargs):
#	cfg['LeptonSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016/SFMC_ICHEP.root")
#	cfg['LeptonTriggerSFRootfile'] = os.path.join(configtools.getPath(),"data/scalefactors/2016/SFTriggerMC.root")
	


