import configtools


def config():
	cfg = configtools.getConfig('mc', 2015, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
#		ekppath="/storage/a/cheidecker/cmssw807_calo_noPUJetID/Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25ns_v7/*.root",
		ekppath="/storage/a/cheidecker/cmssw807_calo_noPUJetID/test/*.root",
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc'])
	cfg['NumberGeneratedEvents'] = 28874658 #for: Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25ns_v7
#	cfg['GeneratorWeight'] =  0.0 #for: Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25ns_v7
	cfg['CrossSection'] = 6025.2  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
	return cfg
