import configtools


def modify_config(cfg):
	"""
	Use runs from DCSONLY Json
	"""
	cfg['JsonFiles'].set_base_json("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/DCSOnly/json_DCSONLY.txt")
	if cfg['InputIsData']:
		cfg['Lumi'] = configtools.get_lumi(json_source=cfg['JsonFiles'])
	else:
		cfg['PileupWeightFile'] = configtools.get_puweights(cfg['JsonFiles'], cfg['InputFiles'], min_bias_xsec=69.0, weight_limits=(0, 4))
	return cfg
