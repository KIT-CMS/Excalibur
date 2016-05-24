import configtools


def config():
	cfg = configtools.getConfig('mc', 2015, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="/storage/a/mfischer/skims/zjet/2016-01-19/Zmm_Zmm_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/mafische/skims/MF_Zll_run2/2016-01-19/Zmm_Zmm_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns/*.root",
#old madgraph		ekppath="/storage/a/mfischer/skims/zjet/2016-01-19/Zmm_Zmm_DYJetsToLL_M-50_madgraphMLM-pythia8_25ns/*.root",
#old madgraph		nafpath="/pnfs/desy.de/cms/tier2/store/user/mafische/skims/MF_Zll_run2/2016-01-19/Zmm_Zmm_DYJetsToLL_M-50_madgraphMLM-pythia8_25ns/*.root",
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc'])
#	cfg['NumberGeneratedEvents'] = 9056998 #for: Zmm_Zmm_DYJetsToLL_M-50_madgraphMLM-pythia8_25ns
#	cfg['NumberGeneratedEvents'] = 29193937 #for: Zmm_Zmm_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns
	cfg['NumberGeneratedEvents'] = 121231446 #for:  /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext4-v1/AODSIM
#	cfg['GeneratorWeight'] =  0.665689483222 #for: Zmm_Zmm_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns
	cfg['CrossSection'] = 6025.2  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
	return cfg
