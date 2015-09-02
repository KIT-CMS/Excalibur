import configtools


def config():
	cfg = configtools.getConfig('mc', 2015, 'mm')
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath="/storage/a/mfischer/skims/zjet/2015_08_31/DYJetsToLL_M_50_aMCatNLO_Asympt25ns_13TeV/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/mafische/skims/MF_AnyMu_2015_746/2015-08-31/DYJetsToLL_M_50_aMCatNLO_Asympt25ns_13TeV/*.root",
	)
	cfg['Jec'] = configtools.getPath() + '/data/jec/Summer15_25ns_preliminary/Summer15_50nsV2_MC'
	cfg['RC'] = False
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts', 'betacuts'], ['None', 'L1', 'L1L2L3'])
	
	configtools.remove_quantities(cfg, ['jet1btag','jet1qgtag', 'jet1rc'])

	cfg['JetMatchingAlgorithm'] = 'algorithmic'
	#cfg['CutAlphaMax'] = 0.3
	cfg['DeltaRRadiationJet'] = 1

	cfg['CutAlphaMax'] = 0.3
	cfg['CutBetaMax'] = 0.1

	cfg['NumberGeneratedEvents'] = 299269
	cfg['CrossSection'] = 6025.2  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV

	return cfg
