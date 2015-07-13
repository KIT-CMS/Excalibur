import ZJetConfigBase as base


def config():
	cfg = base.getConfig('mc', 2015, 'mm')
	cfg["InputFiles"] = base.setInputFiles(
		ekppath="/storage/a/mfischer/skims/2015-07-10_MF_AnyMu_2015_746/MIN_MU_COUNT_2-MIN_MU_PT_8.0/DYJetsToLL_M_50_madgraph_Asympt50ns_13TeV/*.root",
		#nafpath="/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-06-16_DYJetsToLL_M_50_madgraph_13TeV/*.root",
	)
	cfg = base.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3'])
	
	base.remove_quantities(cfg, ['jet1btag','jet1qgtag', 'jet1rc'])

	cfg['JetMatchingAlgorithm'] = 'algorithmic'
	#cfg['CutAlphaMax'] = 0.3
	cfg['DeltaRRadiationJet'] = 1
	cfg['RC'] = False # No RC JEC files available at the moment

	#remove this once AK4 is available
	print "\n\n\033[93mWARNING: USING AK5 Gen Jets!!\033[0m\n\n"
	cfg['GenJets'] = 'ak5GenJetsNoNu'

	return cfg
