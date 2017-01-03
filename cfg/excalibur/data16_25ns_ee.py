import configtools


def config():
	cfg = configtools.getConfig('data', 2016, 'ee', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
#		ekppath="/storage/a/wayand/data2016_nopujetid_v1/DoubleEG/crab_Zll_DoElRun2016B-PromptReco-v1/160524_222650/0000/*.root",
		ekppath="/storage/sg/cheidecker/cmssw807_calo_noPUJetID/Zll_DoElRun2016*-PromptReco-v*/*.root",
		nafpathB="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/rereco_2016-11-11/Zll_DoElRun2016B-ReReco-v3/*.root",
		nafpathC="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/rereco_2016-11-11/Zll_DoElRun2016C-ReReco-v1/*.root",
		nafpathD="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/rereco_2016-11-11/Zll_DoElRun2016D-ReReco-v1/*.root",
		nafpathE="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/rereco_2016-11-11/Zll_DoElRun2016E-ReReco-v1/*.root",
		nafpathF="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/rereco_2016-11-11/Zll_DoElRun2016F-ReReco-v1/*.root",
		nafpathG="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/rereco_2016-11-11/Zll_DoElRun2016G-ReReco-v1/*.root",
		nafpathH="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/rereco_2016-11-11/Zll_DoElRun2016H-ReReco-v1/*.root"	
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2L3Res'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])
	return cfg
