import ZJetConfigBase as base


def config():
	cfg = base.getConfig('mc', 2015, 'mm')
	cfg["InputFiles"] = base.setInputFiles(
		ekppath="/storage/a/dhaitz/skims/2015-06-08_DYJetsToLL_M_50_madgraph_13TeV/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-06-08_DYJetsToLL_M_50_madgraph_13TeV/*.root",
	)
	cfg = base.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['L1L2L3'])
	
	for pipeline in cfg['Pipelines']:
		for tag in ['jet1btag', 'jet1qgtag']:
			cfg['Pipelines'][pipeline]['Quantities'].remove(tag)

	cfg['JetMatchingAlgorithm'] = 'algorithmic'
	cfg['CutAlphaMax'] = 0.3
	
	return cfg
