import configtools


def config():
	cfg = configtools.getConfig('data', 2015, 'mm')
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath="/storage/a/mfischer/skims/MF_AnyMu_2015_746/2015-07-24//DoubleMu_Run2015B_Jul2015_13TeV/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/mafische/skims/MF_AnyMu_2015_746/2015-07-24//DoubleMu_Run2015B_Jul2015_13TeV/*.root",
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2L3Res'])

	configtools.remove_quantities(cfg, ['jet1btag','jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])

	cfg['RC'] = False
	cfg['ProvideResidualCorrections'] = False

	cfg['CutAlphaMax'] = 0.3

	return cfg
