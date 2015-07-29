import configtools


def config():
	cfg = configtools.getConfig('data', 2012, 'ee', tagged=False)
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath="/storage/a/dhaitz/skims/2015-07-28_ee-data_Run2012/kappa_*.root",
		nafpath='/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-07-28_DoubleElectron_Run2012/kappa_*.root'
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts'], ['L1L2L3Res'])
	return cfg
