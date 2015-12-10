import configtools
import mc12_ee

def config():
	cfg = mc12_ee.config()
	cfg['Electrons'] = 'electrons'
	return cfg
