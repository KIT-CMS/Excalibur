import mc15Puppi


def config():
	cfg = mc15Puppi.config()
	cfg['TaggedJets'] = 'ak4PFJetsPuppiNoMu'
	cfg['Met'] = 'metPuppiNoMuNoHF'
	#cfg['MetAddMuons'] = True
	return cfg
