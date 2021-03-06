import configtools


def config():
	cfg = configtools.getConfig('data', 2016, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
#		ekppath="/storage/a/cheidecker/cmssw807_calo_freiburg/Zll_DoMuRun2016B-PromptReco-v1/*.root",
#		ekppath="/storage/a/cheidecker/cmssw807_calo_naf/Zll_DoMuRun2016B-PromptReco-v1/*.root",
#		ekppath="/storage/jbod/cheidecker/cmssw807_calo_noPUJetID/Zll_DoMuRun2016*-PromptReco-v2/*.root",
		ekppath="/storage/sg/cheidecker/cmssw807_calo_noPUJetID/Zll_DoMuRun2016*-PromptReco-v*/*.root",
		nafpathB="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/rereco_2016-11-11/Zll_DoMuRun2016B-ReReco-v3/*.root",
		nafpathC="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/rereco_2016-11-11/Zll_DoMuRun2016C-ReReco-v1/*.root",
		nafpathD="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/rereco_2016-11-11/Zll_DoMuRun2016D-ReReco-v1/*.root",
		nafpathE="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/rereco_2016-11-11/Zll_DoMuRun2016E-ReReco-v1/*.root",
		nafpathF="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/rereco_2016-11-11/Zll_DoMuRun2016F-ReReco-v1/*.root",
		nafpathG="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/rereco_2016-11-11/Zll_DoMuRun2016G-ReReco-v1/*.root",
		nafpathH="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/rereco_2016-11-11/Zll_DoMuRun2016H-ReReco-v1/*.root"		
#		ekppath="/storage/gridka-nrg/store/user/cheideck/Skimming/cmssw807_calo_noPUJetID_freiburg/Zll_DoMuRun2016B-PromptReco-v2/*.root",
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2L3Res'])
#	cfg = configtools.expand(cfg, ['finalcuts'], ['L1L2L3Res'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])
	return cfg
