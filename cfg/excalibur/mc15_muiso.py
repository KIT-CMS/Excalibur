import configtools
import mc15


def config():
	cfg = mc15.config()
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath="/storage/a/mfischer/skims/MF_AnyMu_2015_746/2015-07-24/DYJetsToLL_M_50_aMCatNLO_Asympt50ns_13TeV/*.root",
	)
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
	return cfg