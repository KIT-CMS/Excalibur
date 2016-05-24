import configtools
import mc15

def config():
	mc15Cfg = mc15.config()

	cfg = configtools.getConfig('mc', 2015, 'mm')
	cfg['InputFiles'] = mc15Cfg['InputFiles']
	cfg['TaggedJets'] = 'ak4PFJetsPuppi'

	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag','jet1qgtag', 'jet1rc'])

	cfg['JetMatchingAlgorithm'] = 'algorithmic'
	cfg['DeltaRRadiationJet'] = 1
	cfg['RC'] = False # No RC JEC files available at the moment
	cfg['CutAlphaMax'] = 0.3
	cfg['CutBetaMax'] = 0.1

	cfg['NumberGeneratedEvents'] = mc15Cfg['NumberGeneratedEvents']
	cfg['CrossSection'] = mc15Cfg['CrossSection']
	cfg['Met'] = 'metPuppi'


	return cfg
