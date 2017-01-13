import configtools

def modify_config(cfg):
	"""
	Add quantities from leading skim jets
	"""
	configtools.add_quantities(
		cfg,
		("skimjet1pt", "skimjet1phi", "skimjet1eta", "skimjet1validity")
	)
	return cfg
