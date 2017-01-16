import configtools


def config():
	cfg = configtools.getConfig('data', 2016, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_SiMuRun2016B-PromptReco-v2/*.root",
		#ekppath='/storage/a/afriedel/zjets/data_miniAOD_singleMu_run2016D.root',

	)
	cfg = configtools.expand(cfg, ['zcuts', 'leptoncuts'], ['None'], True)
	configtools.remove_quantities(cfg, [ 'jet1btag','jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])
	return cfg
