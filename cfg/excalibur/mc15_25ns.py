import configtools


def config():
	cfg = configtools.getConfig('mc', 2015, 'mm', bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
<<<<<<< HEAD
		ekppath="/storage/a/mfischer/skims/zjet/2016-01-19/Zmm_Zmm_DYJetsToLL_M-50_amcatnloFXFX-pythia8_HCALDebug_25ns/*.root",
		nafpath="",
=======
		ekppath="/storage/a/mfischer/skims/zjet/2016-01-19/Zmm_Zmm_DYJetsToLL_M-50_madgraphMLM-pythia8_25ns/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/mafische/skims/MF_Zll_run2/2016-01-19/Zmm_Zmm_DYJetsToLL_M-50_madgraphMLM-pythia8_25ns/*.root",
>>>>>>> 1ba73aa651f495f609c75bb74b1c9ce26caa10ce
	)
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts', 'betacuts'], ['None', 'L1', 'L1L2L3'])
	configtools.remove_quantities(cfg, ['jet1btag', 'jet1qgtag', 'jet1rc'])
	cfg['NumberGeneratedEvents'] = 299269
	cfg['CrossSection'] = 6025.2  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
	return cfg
