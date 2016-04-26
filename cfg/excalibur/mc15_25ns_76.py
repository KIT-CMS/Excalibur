import configtools


def config():
	cfg = configtools.getConfig('mc', 2015, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="/storage/8/wayand/gc_zjets/full_lep_v5/crab_Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_25ns/results/*.root",
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts', 'betacuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc'])
#	cfg['NumberGeneratedEvents'] = 9056998 #for: Zmm_Zmm_DYJetsToLL_M-50_madgraphMLM-pythia8_25ns
#	cfg['NumberGeneratedEvents'] = 29193937 #for: Zmm_Zmm_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns
#	cfg['NumberGeneratedEvents'] = 121231446 #for:  /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext4-v1/AODSIM
#	cfg['GeneratorWeight'] =  0.665689483222 #for: Zmm_Zmm_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns
	cfg['CrossSection'] = 6025.2  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
	return cfg
