import ZJetConfigBase as base


def config():
	cfg = base.getConfig('data', 2015, 'mm')
	cfg["InputFiles"] = base.setInputFiles(
		ekppath="/storage/a/mfischer/skims/2015-07-10_MF_AnyMu_2015_746/MIN_MU_COUNT_2-MIN_MU_PT_8.0/DoubleMu_Run2015B_Jul2015_13TeV/*.root",
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-05-18_DoubleMu_Run2012_22Jan2013_8TeV/*.root",
	)
	cfg = base.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])

	base.remove_quantities(cfg, ['jet1btag','jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])

	# remove JSON filter until JSON file is released by CMS
	if 'filter:JsonFilter' in cfg['Processors']:
		cfg['Processors'].remove('filter:JsonFilter')
	print "\n\n\033[93mWARNING: NOT USING JSON FILE!!\033[0m\n\n"

	cfg['RC'] = False
	cfg['ProvideResidualCorrections'] = False

	return cfg
