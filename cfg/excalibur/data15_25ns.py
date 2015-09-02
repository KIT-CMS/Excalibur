import configtools


def config():
	cfg = configtools.getConfig('data', 2015, 'mm')
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath="/storage/a/mfischer/skims/zjet/2015_08_31/DoubleMu_Run2015C_Aug2015_13TeV/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/mafische/skims/MF_AnyMu_2015_746/2015-08-31/DoubleMu_Run2015C_Aug2015_13TeV/*.root",
	)
	cfg['Jec'] = configtools.getPath() + '/data/jec/Summer15_25ns_preliminary/Summer15_50nsV2_MC'
	cfg['RC'] = False
	cfg['ProvideResidualCorrections'] = False
	cfg['JsonFiles'] = [configtools.getPath() + '/data/json/Cert_246908-254879_13TeV_PromptReco_Collisions15_JSON.txt']
	cfg['Lumi'] = 0.0521
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag','jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])

	cfg['CutAlphaMax'] = 0.3

	return cfg
