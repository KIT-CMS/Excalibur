import configtools


def modify_config(cfg):
	"""
	Use runs from DCSONLY Json
	"""
	cfg['JsonFiles'].set_base_json("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/DCSOnly/json_DCSONLY.txt")
	cfg['Lumi'] = configtools.get_lumi(json_source=cfg['JsonFiles'])
	return cfg
