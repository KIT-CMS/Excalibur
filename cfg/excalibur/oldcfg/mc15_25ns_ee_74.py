import configtools


def config():
	cfg = configtools.getConfig('mc', 2015, 'ee', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="/storage/a/mfischer/skims/zjet/2016-01-19/Zee_Zee_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/mafische/skims/MF_Zll_run2/2016-01-19/Zee_Zee_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns/*.root"
#old madgraph		ekppath="/storage/a/mfischer/skims/zjet/2016-01-19/Zee_Zee_DYJetsToLL_M-50_madgraphMLM-pythia8_25ns/*.root",
#old madgraph		nafpath="/pnfs/desy.de/cms/tier2/store/user/mafische/skims/MF_Zll_run2/2016-01-19/Zee_Zee_DYJetsToLL_M-50_madgraphMLM-pythia8_25ns/*.root"
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc', "e1mvanontrig", "e1mvatrig", "e2mvanontrig", "e2mvatrig"])
#	cfg['NumberGeneratedEvents'] = 9056998 #for: Zee_Zee_DYJetsToLL_M-50_madgraphMLM-pythia8_25ns
	cfg['NumberGeneratedEvents'] = 29193937 #for: Zee_Zee_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns
	cfg['GeneratorWeight'] =  0.65015166151 #for: Zee_Zee_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns
	cfg['CrossSection'] = 6025.2  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
	return cfg
