import configtools


def config():
	cfg = configtools.getConfig('mc', 2015, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="/storage/a/wayand/cmss80x/*.root",
	)
	cfg['TaggedJets'] = 'ak4PFJetsPuppi'
	cfg['Met'] = 'metPuppi'
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts', 'betacuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc'])
	cfg['NumberGeneratedEvents'] = 29193937 #for: Zmm_Zmm_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns
#	cfg['GeneratorWeight'] =  0.665689483222 #for: Zmm_Zmm_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns
	cfg['CrossSection'] = 6025.2  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
	return cfg
