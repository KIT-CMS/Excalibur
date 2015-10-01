import configtools


def config():
	cfg = configtools.getConfig('data', 2015, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath="/storage/a/mfischer/skims/zjet/2015_09_26/DoubleMu_Run2015C_Jul2015_13TeV/*.root",
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2L3Res'])
	configtools.remove_quantities(cfg, ['jet1btag','jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])

	cfg['CutAlphaMax'] = 0.3

	return cfg
