import configtools


def config():
	cfg = configtools.getConfig('data', 2016, 'ee', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
#		ekppath="/storage/a/cheidecker/cmssw807_calo_freiburg/Zll_DoMuRun2016B-PromptReco-v1/*.root",
#		ekppath="/storage/a/wayand/data2016_nopujetid_v1/DoubleEG/crab_Zll_DoElRun2016B-PromptReco-v1/160524_222650/0000/*.root",
#		ekppath="/storage/sg/cheidecker/cmssw807_calo_noPUJetID/Zll_DoElRun2016*-PromptReco-v2/*.root",
		ekppath="/storage/sg/tberger/SkimmingResults/Zll_DoElRun2016*-PromptReco-v*/*.root",
#		ekppath="/storage/jbod/tberger/Skimming/resultsMINIAOD/Zll_DoElRun2016G-PromptReco-v1/*.root",
	)
	cfg['TaggedJets'] = 'ak4PFJetsPuppi'
	cfg['Met'] = 'metPuppi'
	cfg['RC']= False
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2L3Res'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])
	return cfg
