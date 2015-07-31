import configtools
import mc15


def config():
	cfg = mc15.config()
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