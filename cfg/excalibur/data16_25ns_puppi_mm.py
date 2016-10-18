import configtools


def config():
	cfg = configtools.getConfig('data', 2016, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="/storage/sg/tberger/SkimmingResults/Zll_DoMuRun2016*-PromptReco-v*/*.root",
	)
	cfg['TaggedJets'] = 'ak4PFJetsPuppi'
	cfg['Met'] = 'metPuppi'
        cfg['RC'] = False
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2L3Res'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])
	return cfg
