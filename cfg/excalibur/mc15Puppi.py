import ZJetConfigBase as base
import mc15


def config():
	cfg = mc15.config()
	cfg['TaggedJets'] = 'ak4PFJetsPuppi'
	return cfg
