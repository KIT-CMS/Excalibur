import configtools


def config():
	cfg = configtools.getConfig('data', 2016, 'ee', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		#ekppath="/storage/jbod/tberger/SkimmingResults/Zll_DoElRun2016B-PromptReco-v2/*.root"
		nafpath0="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/data_reminiaod03Feb2017/Zll_DoElRun2016H-03Feb2017-ver2v1/*root",
		nafpath1="/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/data_reminiaod03Feb2017/Zll_DoElRun2016H-03Feb2017-ver3v1/*.root"
	)
	cfg['JsonFiles'] = [configtools.getPath() + '/data/json/Cert_H_13TeV_23Sep2016ReReco_Collisions16_JSON.txt']
	cfg['Jec'] = configtools.getPath() + '/data/JECDatabase/textFiles/Summer16_23Sep2016HV3_DATA/Summer16_23Sep2016HV3_DATA'
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2L3Res'])
	configtools.remove_quantities(cfg, ['jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])
	return cfg
