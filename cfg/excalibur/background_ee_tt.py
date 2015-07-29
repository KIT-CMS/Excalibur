import configtools
import mc_ee

def config():
	cfg = mc_ee.config()
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath="/storage/a/dhaitz/skims/2015-07-28_ee-backgrounds_Run2012/kappa_TTJets*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-07-28_ee-backgrounds_Run2012/kappa_TTJets*.root",
	)
	cfg['CrossSection'] = 26.75
	cfg['NumberGeneratedEvents'] = 21675970
	return cfg
