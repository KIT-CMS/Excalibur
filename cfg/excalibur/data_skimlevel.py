import configtools


def config():
	cfg = configtools.getConfig('data', 2012, 'mm')
	cfg["InputFiles"] = configtools.setInputFiles(
		#ekppath="/storage/a/dhaitz/skims/2015-04-13_DoubleMu_Run2012_22Jan2013_8TeV/*.root",
		ekppath="/storage/a/dhaitz/skims/2015-04-13_DoubleMu_Run2012_22Jan2013_8TeV/kappa_DoubleMuParked_Run2012D_22Jan2013_8TeV_*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-04-13_DoubleMu_Run2012_22Jan2013_8TeV/*.root",
	)
	cfg['Processors'] = [] # No processors to look at skim level
	cfg['Pipelines']['default']['Processors'] = [] # No processors to look at skim level
	cfg = configtools.expand(cfg, ['nocuts'], ['None'])

	return cfg
