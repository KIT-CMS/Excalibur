import configtools


def config():
	cfg = configtools.getConfig('mc', 2012, 'ee', tagged=False)
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath='/storage/a/dhaitz/kappa_DY_ee.root',  # testfile
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts'], ['L1L2L3'])

	cfg['TaggedJets'] = 'AK5PFTaggedJetsCHS'

	return cfg
