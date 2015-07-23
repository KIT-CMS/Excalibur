import configtools
import mc_ee

def config():
	cfg = mc_ee.config()
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath="/storage/a/dhaitz/skims/2015-07-22_ee-backgrounds_Run2012/kappa_QCD*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-07-22_ee-backgrounds_Run2012/QCD*.root",
	)
	cfg['TaggedJets'] = 'ak5PFJetsCHS'

	# dict of cross section for the samples and respective NEvents
	qcd_samples = {
		2.89424e+08:  35040695,
		7.46765e07:   33088888,
		1.18938e+06:  34542763,
		31274.:       31697066,
		4227.67:      34611322,
		803.531:      34080562,
	}
	cfg['SampleReweighting'] = True
	cfg['SampleReweightingCrossSections'] = qcd_samples.keys()
	cfg['SampleReweightingNEvents'] = [qcd_samples[key] for key in cfg['SampleReweightingCrossSections']]

	return cfg
