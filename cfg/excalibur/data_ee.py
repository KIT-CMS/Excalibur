import configtools


def config():
	cfg = configtools.getConfig('data', 2012, 'ee', tagged=False)
	configtools.changeNamingScheme(cfg)
	cfg["InputFiles"] = configtools.setInputFiles(
		#TESTFILE:
		ekppath="/storage/a/dhaitz/kappa_DYJetsToLL_M_50_madgraph_8TeV_5148.root",
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts'], ['L1L2L3', 'L1L2L3Res'])
	del cfg['Met']
	
	for processor in ['producer:HltProducer', 'filter:JsonFilter', 'filter:HltFilter']:
		if processor in cfg['Processors']:
			cfg['Processors'].remove(processor)

	configtools.remove_quantities(cfg, [
		'jet1btag','jet1qgtag',
		'met', 'metpt', 'metphi', 'sumet', 'mpf',
		"rawmpf", "rawmet", "rawmetphi"
	])

	return cfg
