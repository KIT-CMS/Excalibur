import configtools


def config():
	cfg = configtools.getConfig('mc', 2015, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		ekppath="/storage/a/mfischer/skims/zjet/2015-10-09/DYJetsToLL_M_50_aMCatNLO_Asympt25ns_13TeV/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/mafische/skims/MF_AnyMu_2015_746/2015-10-09/DYJetsToLL_M_50_aMCatNLO_Asympt25ns_13TeV/*.root",
	)
	cfg['TaggedJets'] = 'ak4PFJetsPuppi'
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc'])
	cfg['PileupWeightFile'] = configtools.PUWeights(cfg['JsonFiles'], cfg['InputFiles'], min_bias_xsec=cfg['Minbxsec'], weight_limits=(0, 4))
	cfg['NumberGeneratedEvents'] = 299269
	cfg['CrossSection'] = 6025.2  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
	cfg['Met'] = 'metPuppi'

	return cfg
