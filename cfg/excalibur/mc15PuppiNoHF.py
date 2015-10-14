import configtools
import mc15Puppi


def config():
	cfg = mc15Puppi.config()
	cfg['TaggedJets'] = 'ak4PFJetsPuppi'
	cfg['Met'] = 'metPuppiNoHF'
	return cfg
