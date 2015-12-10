import configtools


def config():
	cfg = configtools.getConfig('data', 2012, 'mm')
	configtools.changeNamingScheme(cfg)
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath="/storage/a/dhaitz/skims/2015-05-18_DoubleMu_Run2012_22Jan2013_8TeV/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-05-18_DoubleMu_Run2012_22Jan2013_8TeV/*.root",
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['L1L2L3', 'L1L2Res', 'L1L2L3Res'])
	cfg['ProvideL2ResidualCorrections'] = True
	return cfg
