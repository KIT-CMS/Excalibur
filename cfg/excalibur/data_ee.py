import configtools


def config():
	cfg = configtools.getConfig('data', 2012, 'ee', tagged=False)
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath="/storage/a/dhaitz/skims/2015-07-22_DoubleElectron_Run2012/*.root",
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts'], ['L1L2L3Res'])
	return cfg
