import configtools


def config():
	cfg = configtools.getConfig('data', 2015, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath="/storage/a/mfischer/skims/zjet/2015_08_31/DoubleMu_Run2015C_Aug2015_13TeV/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/mafische/skims/MF_AnyMu_2015_746/2015-08-31/DoubleMu_Run2015C_Aug2015_13TeV/*.root",
	)
	cfg['RC'] = False
	cfg['ProvideResidualCorrections'] = False
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag','jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])

	cfg['CutAlphaMax'] = 0.3

	return cfg
