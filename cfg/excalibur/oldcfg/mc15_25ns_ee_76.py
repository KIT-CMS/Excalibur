import configtools


def config():
	cfg = configtools.getConfig('mc', 2015, 'ee', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="/storage/a/wayand/cmss76x/*.root",
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc', "e1mvanontrig", "e1mvatrig", "e2mvanontrig", "e2mvatrig"])
	cfg['NumberGeneratedEvents'] = 29193937 #for: Zee_Zee_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns
#	cfg['GeneratorWeight'] =  0.65015166151 #for: Zee_Zee_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns
	cfg['CrossSection'] = 6025.2  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
	return cfg
