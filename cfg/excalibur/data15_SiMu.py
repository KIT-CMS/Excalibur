import configtools


def config():
	cfg = configtools.getConfig('data', 2015, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="/storage/a/afriedel/freiburg/workdir-data-matched/se_output/Zll_SiMuRun2015D-16Dec2015-v2/*.root"
		#ekppath="/home/afriedel/CMSSW_7_6_4/src/Kappa/Skimming/zjet/skim76_jtb.root",
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2L3Res'])
	configtools.remove_quantities(cfg, [ 'jet1btag','jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])
	return cfg
