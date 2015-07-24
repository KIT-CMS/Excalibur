import configtools
import data_ee

def config():
	cfg = data_ee.config()
	cfg['Electrons'] = 'electrons'
	return cfg
