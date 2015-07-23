import configtools


def config():
	cfg = configtools.getConfig('mc', 2015, 'mm')
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath="/storage/a/mfischer/skims/MF_AnyMu_2015_746/recent/DYJetsToLL_M_50_aMCatNLO_Asympt50ns_13TeV/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/mafische/skims/MF_AnyMu_2015_746/2015-07-17/DYJetsToLL_M_50_aMCatNLO_Asympt50ns_13TeV/*.root",
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	
	configtools.remove_quantities(cfg, ['jet1btag','jet1qgtag', 'jet1rc'])

	cfg['JetMatchingAlgorithm'] = 'algorithmic'
	#cfg['CutAlphaMax'] = 0.3
	cfg['DeltaRRadiationJet'] = 1
	cfg['RC'] = False # No RC JEC files available at the moment

	cfg['CutAlphaMax'] = 0.3
	
	cfg['NumberGeneratedEvents'] = 299269
	cfg['CrossSection'] = 6025.2  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV

	return cfg
