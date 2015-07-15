import ZJetConfigBase as base


def config():
	cfg = base.getConfig('data', 2015, 'mm')
	cfg["InputFiles"] = base.setInputFiles(
		ekppath="/storage/a/mfischer/skims/MF_AnyMu_2015_746/recent/MIN_MU_COUNT_2-MIN_MU_PT_8.0/DoubleMu_Run2015B_Jul2015_13TeV/*.root",
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-05-18_DoubleMu_Run2012_22Jan2013_8TeV/*.root",
	)
	cfg = base.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])

	base.remove_quantities(cfg, ['jet1btag','jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])

	cfg['RC'] = False
	cfg['ProvideResidualCorrections'] = False

	cfg['CutAlphaMax'] = 0.3

	return cfg
