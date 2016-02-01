import configtools


def config():
	cfg = configtools.getConfig('mc', 2015, 'ee', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="/storage/a/mfischer/skims/zjet/2016-01-19/Zee_Zee_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns/*.root",
		nafpath="",
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc', "e1mvanontrig", "e1mvatrig", "e2mvanontrig", "e2mvatrig"])
	cfg['NumberGeneratedEvents'] = 299269
	cfg['CrossSection'] = 6025.2  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
	return cfg
