import configtools
import mc15

import copy


def config():
	cfg = configtools.getConfig('data', 2015, 'mm')
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath="/storage/a/mfischer/skims/MF_AnyMu_2015_746/2015-07-24//DoubleMu_Run2015B_Jul2015_13TeV/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/mafische/skims/MF_AnyMu_2015_746/2015-07-24//DoubleMu_Run2015B_Jul2015_13TeV/*.root",
	)
	# move Muon and Z filters to pipelines
	cfg['Processors'].remove('filter:MinNMuonsCut')
	cfg['Processors'].remove('filter:MaxNMuonsCut')
	cfg['Processors'].remove('filter:ZFilter')
	cfg['Pipelines']['default']['Processors'] = ['filter:MinNMuonsCut', 'filter:MaxNMuonsCut', 'filter:ZFilter'] + cfg['Pipelines']['default']['Processors']
	# expand regularly
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2L3Res'])
	# create additional mode without any filters
	for pipeline in cfg['Pipelines'].keys():
		if pipeline.startswith('nocuts'):
			nofilter_pipeline = pipeline.replace('nocuts', 'nofilters')
			cfg['Pipelines'][nofilter_pipeline] = copy.deepcopy(cfg['Pipelines'][pipeline])
			for filter_name in ['filter:MinNMuonsCut', 'filter:MaxNMuonsCut', 'filter:ZFilter']:
				cfg['Pipelines'][nofilter_pipeline]['Processors'].remove(filter_name)

	configtools.remove_quantities(cfg, ['jet1btag','jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])


	cfg['CutAlphaMax'] = 0.3

	# invalid muon isolation quantities
	configtools.add_quantities(
		cfg,
		[
			"mu%s%d%s"%(mu_type, mu_idx, param)
			for mu_idx in range(1,3)
			for param in ("iso","sumchpt","sumnhet","sumpet","sumpupt","pt")
			for mu_type in ("","inv")
		]
	)
	configtools.add_quantities(cfg,["nmuons","nmuonsinv"])
	return cfg
