import configtools
import data12_ee

def config():
	cfg = data12_ee.config()
	cfg['Electrons'] = 'electrons'
	return cfg
