import configtools


def config():
	cfg = configtools.getConfig('data', 2012, 'mm')
	configtools.changeNamingScheme(cfg)
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath="/storage/a/dhaitz/skims/2015-05-18_DoubleMu_Run2012_22Jan2013_8TeV/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-05-18_DoubleMu_Run2012_22Jan2013_8TeV/*.root",
	)
	cfg['RC'] = True
	cfg['Jec'] = configtools.getPath() + '/data/jec/Winter14_V8_53X_RC/Winter14_V8_DATA'
	cfg['Processors'].remove("filter:HltFilter")
	cfg['Processors'].remove("producer:HltProducer")
	cfg['Processors'].remove("producer:TypeIMETProducer")
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['RC', 'None'])

	return cfg
