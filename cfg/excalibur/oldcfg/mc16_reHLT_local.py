import configtools

def config():
	cfg = configtools.getConfig('mc', 2016, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="/storage/a/afriedel/workdir-mc2016/*.root",
		#ekppath='/home/afriedel/CMSSW_8_0_22/src/Kappa/Skimming/zjet/skim80_jtb.root',
		#ekppath="srm://dgridsrm-fzk.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/dcms/disk-only/store/user/afriedel/Skimming/mc2016/MC_DYJets_to_LL/*.root"
	)	
	cfg = configtools.expand(cfg, ['zcuts',  'leptoncuts', 'genzcuts', 'genleptoncuts', 'allleptoncuts', 'allzcuts', 'nocuts'], ['None'])
	#cfg = configtools.expand(cfg, ['allleptoncuts', 'allzcuts'], ['None'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc'])
	cfg['NumberGeneratedEvents'] = 104113466 #for:  /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext4-v1/AODSIM
	cfg['GeneratorWeight'] =  0.670104921874 #for: Zll_DYJetsToLL_M-50_amcatnloFXFX-pythia8_ext4_25ns
	cfg['CrossSection'] = 5765.4  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
	return cfg
