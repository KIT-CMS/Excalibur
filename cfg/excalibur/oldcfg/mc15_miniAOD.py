import configtools


def config():
	cfg = configtools.getConfig('mc', 2015, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
#failed		ekppath="/storage/8/wayand/gc_zjets/full_lep_v5/crab_Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_ext4_25ns/results/*.root",
#old mc@nlo
		ekppath="/storage/a/afriedel/workdir-mc-matched/se_output/DYJetsToLL/*.root",
#		ekppath="/home/afriedel/CMSSW_7_6_4/src/Kappa/Skimming/zjet/skim76_jtb.root"
#old mc@nlo		nafpath="/pnfs/desy.de/cms/tier2/store/user/mafische/skims/MF_Zll_run2/2016-01-19/Zmm_Zmm_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns/*.root",
#old madgraph		ekppath="/storage/a/mfischer/skims/zjet/2016-01-19/Zmm_Zmm_DYJetsToLL_M-50_madgraphMLM-pythia8_25ns/*.root",
#old madgraph		nafpath="/pnfs/desy.de/cms/tier2/store/user/mafische/skims/MF_Zll_run2/2016-01-19/Zmm_Zmm_DYJetsToLL_M-50_madgraphMLM-pythia8_25ns/*.root",
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc'])
#	cfg['NumberGeneratedEvents'] = 9056998 #for: Zmm_Zmm_DYJetsToLL_M-50_madgraphMLM-pythia8_25ns
#	cfg['NumberGeneratedEvents'] = 29193937 #for: Zmm_Zmm_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns
	cfg['NumberGeneratedEvents'] = 121212419 #for:  /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext4-v1/AODSIM
#	cfg['NumberGeneratedEvents'] = 12
	cfg['GeneratorWeight'] =  0.670201351233 #for: Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_ext4_25ns
	cfg['CrossSection'] = 5765.4  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
	return cfg
