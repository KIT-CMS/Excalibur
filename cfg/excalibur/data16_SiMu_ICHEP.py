import configtools


def config():
	cfg = configtools.getConfig('data', 2016, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_SiMuRun2016B-PromptReco-v2/*.root",
		#ekppath='/storage/a/afriedel/zjets/data_miniAOD_singleMu_run2016D.root',
		nafpathB='/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_SiMuRun2016B-PromptReco-v2/*.root',
	        nafpathC='/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_SiMuRun2016C-PromptReco-v2/*.root',
        	nafpathD='/pnfs/desy.de/cms/tier2/store/user/tberger/Skimming/dataminiaod_BC_2016-10-24/Zll_SiMuRun2016D-PromptReco-v2/*.root',

	)
	cfg = configtools.expand(cfg, ['zcuts', 'leptoncuts'], ['None'], True)
	configtools.remove_quantities(cfg, [ 'jet1btag','jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])
	cfg['MuonID'] = 'tight'
        cfg['MuonIso'] = 'loose'
	cfg['LeptonSFRootfile'] = configtools.getPath()+"/data/scalefactors/2016/SFData_ICHEP.root"
        cfg['LeptonTriggerSFRootfile'] = configtools.getPath()+"/data/scalefactors/2016/SFTriggerData.root"
	cfg['HltPaths'] = ['HLT_IsoMu22', 'HLT_IsoTkMu22']
	#cfg['UseHighPtID'] = True
	return cfg
