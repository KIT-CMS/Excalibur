import ZJetConfigBase as base


def config():
	cfg = base.getConfig('data', 2012, 'ee')
	base.changeNamingScheme(cfg)
	cfg["InputFiles"] = base.setInputFiles(
		#TESTFILE:
		ekppath="/storage/a/dhaitz/kappa_DYJetsToLL_M_50_madgraph_8TeV_5148.root",
		#nafpath=",
	)
	cfg = base.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['L1L2L3', 'L1L2L3Res'])
	del cfg['Met']
	
	for processor in ['producer:HltProducer', 'filter:JsonFilter', 'filter:HltFilter']:
		if processor in cfg['Processors']:
			cfg['Processors'].remove(processor)

	base.remove_quantities(cfg, [
		'jet1btag','jet1qgtag',
		'met', 'metpt', 'metphi', 'sumet', 'mpf',
		"rawmpf", "rawmet", "rawmetphi"
	])

	return cfg
