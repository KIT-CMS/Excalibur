import configtools


def config():
	cfg = configtools.getConfig('mc', 2016, 'ee', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="/storage/sg/cheidecker/cmssw807_calo_noPUJetID/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25ns_v7/*.root",
		#ekppath="/storage/jbod/tberger/Skimming/results-mc8014/cmssw8014_calo_noPUJetID/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25ns_v7/*.root",
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc']) #, "e1mvanontrig", "e1mvatrig", "e2mvanontrig", "e2mvatrig"
	cfg['NumberGeneratedEvents'] = 28696958 #for: Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25ns_v7
	cfg['GeneratorWeight'] =  0.669888076639 #for: Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25ns_v7
	cfg['CrossSection'] = 6025.2  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
	return cfg
