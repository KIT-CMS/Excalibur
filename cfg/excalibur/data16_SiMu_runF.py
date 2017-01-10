import configtools


def config():
	cfg = configtools.getConfig('data', 2016, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_SiMuRun2016F-PromptReco-v1/*.root",
		#ekppath='/storage/a/afriedel/zjets/data_miniAOD_singleMu_run2016D.root',

	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'leptoncuts'], ['None', 'L1L2L3', 'L1L2L3Res'])
	configtools.remove_quantities(cfg, [ 'jet1btag','jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])
	return cfg
