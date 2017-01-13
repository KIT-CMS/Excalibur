import configtools

def modify_config(cfg):
	"""
	Use unprocessed skim level information only
	"""
	# No processors to look at skim level
	cfg['Processors'] = []
	# remove all pipelines that do actual processing
	for pipeline in cfg['Pipelines'].keys():
		if pipeline.startswith('nocuts'):
			cfg['Pipelines'][pipeline]['Processors'][:] = []
		else:
			del cfg['Pipelines'][pipeline]
	return cfg
