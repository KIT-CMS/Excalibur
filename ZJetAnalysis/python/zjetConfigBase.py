# -*- coding: utf-8 -*-

def getZjetConfig(conf):

	basic_mc_quantities = ["npv", "run", "puweight",
                "metphi", "metpt",
                "nvalidelectrons", "validz",
                "zmass", "zpt", "zy"
    ]

	if not conf['InputIsData']:
		for pipeline in conf['Pipelines']:
			conf['Pipelines'][pipeline]['Quantities'] = basic_mc_quantities
			
	return conf
