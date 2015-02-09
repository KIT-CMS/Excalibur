# -*- coding: utf-8 -*-

def ee_bkgrs():
	#path = '/portal/ekpcms5/home/dhaitz/git/excalibur'
	#mc = '/store/mc_ee_powheg_corr.root'

	l_plots = []
	for quantity, xlims in zip(['zmass', 'zpt'], [[81, 101], [30, 230]]):
		d = {
			'x_expressions': quantity,
			'x_lims': xlims,
		}
		if quantity == 'zpt':
			d['x_bins'] = "40,30,230"
		l_plots.append(d)
	return l_plots, "json/ee-bkgrs.json"
