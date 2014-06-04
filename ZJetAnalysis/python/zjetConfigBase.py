# -*- coding: utf-8 -*-

def getZjetConfig():

	analysis='zmm'
	year=2012
	typ='mc'


	quantities = ["npv", "run",
                "metphi", "metpt",
                "nvalidelectrons", "validz",
                "zmass", "zpt", "zy"
    ]

	if typ == 'mc':
		quantities += ["puweight"]

	if not conf['InputIsData']:
		for pipeline in conf['Pipelines']:
			conf['Pipelines'][pipeline]['Quantities'] = basic_mc_quantities
			
	return conf
