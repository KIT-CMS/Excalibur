import configtools
import data15

def config():
	data15Cfg = data15.config()

	cfg = configtools.getConfig('data', 2015, 'mm')
	cfg['InputFiles'] = data15Cfg['InputFiles']
	cfg['TaggedJets'] = 'ak4PFJetsPuppiNoMu'
	cfg['Met'] = 'metPuppiNoMuNoHF'
	cfg = configtools.expand(cfg, ['nocuts', 'zcuts', 'noalphanoetacuts', 'noalphacuts', 'noetacuts', 'finalcuts'], ['None', 'L1', 'L1L2L3', 'L1L2L3Res'])

	configtools.remove_quantities(cfg, ['jet1btag','jet1qgtag', 'jet1ptl1l2l3', 'jet1res', 'jet1rc'])

	cfg['DeltaRRadiationJet'] = 1
	cfg['CutAlphaMax'] = 0.3
	cfg['CutBetaMax'] = 0.1

	return cfg
