

def modify_config(cfg):
	"""
	Use runs from DCSONLY Json
	"""
	cfg['JsonFiles'].set_base_json("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/DCSOnly/json_DCSONLY.txt")
	return cfg
