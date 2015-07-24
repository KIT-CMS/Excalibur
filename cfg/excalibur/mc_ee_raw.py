import configtools
import mc_ee

def config():
	cfg = mc_ee.config()
	cfg['Electrons'] = 'electrons'
	return cfg
