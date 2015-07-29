import configtools


def config():
	cfg = configtools.getConfig('mc', 2012, 'ee', tagged=False)
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath='/storage/a/dhaitz/skims/2015-07-28_ee-mc_Run2012/kappa_DYJ*.root',
		nafpath='/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-07-28_ee-mc_Run2012/kappa_DYJ*.root'
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts'], ['L1L2L3'])

	cfg['NumberGeneratedEvents'] = 30459503
	cfg['CrossSection'] = 3503.71

	return cfg
