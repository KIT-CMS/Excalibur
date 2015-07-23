# -*- coding: utf-8 -*-

import time

import Excalibur.Plotting.harryinterface as harryinterface
import Artus.Utility.logger as logger

def jec_combination(args=None, additional_dictionary=None):
	"""function to create the root combination file for the jec group."""
	plots = []

	methoddict = {
		'ptbalance': 'PtBal',
		'mpf': 'MPF',
		'rawmpf': 'MPF-notypeI',
	}

	alpha_limits = [0.1, 0.15, 0.2, 0.3, 0.4]
	alpha_cuts = ['(alpha<{})'.format(limit) for limit in alpha_limits]
	alpha_strings = ['a'+str(int(100*limit)) for limit in alpha_limits]

	eta_borders = [0, 0.783, 1.305, 1.93, 2.5, 2.964, 3.139, 5.191]
	eta_cuts = ["({0}<=abs(jet1eta)&&abs(jet1eta)<{1})".format(*b) for b in zip(eta_borders[:-1], eta_borders[1:])]
	eta_cuts = ["(0<=abs(jet1eta)&&abs(jet1eta)<1.3)"] + eta_cuts # also include standard barrel jet selection
	eta_strings = ["eta_{0:0>2d}_{1:0>2d}".format(int(round(10*up)), int(round(10*low))) for up, low in zip(eta_borders[:-1], eta_borders[1:])]
	eta_strings = ["eta_00_13"] + eta_strings

	now = time.localtime()
	first = True
	for method in ['mpf', 'ptbalance', 'rawmpf']:
		for alphacut, alphastring in zip(alpha_cuts, alpha_strings):
			for etacut, etastring in zip(eta_cuts, eta_strings):
				for correction in ['L1L2L3']: # no L1L2L3Res available atm 
					labelsuffix = '_'.join([methoddict[method], 'CHS', alphastring, etastring, correction]) 
					d = {
						'x_expressions': ['zpt'],
						'y_expressions': [method],
						'x_bins': 'zpt',
						'analysis_modules': ['Ratio', 'ConvertToTGraphErrors'],
						'plot_modules': ['ExportRoot'],
						'tree_draw_options' : 'prof',
						'labels': ['_'.join([item, labelsuffix]) for item in ['Data', 'MC', 'Ratio']],
						'corrections': [correction],
						'filename': 'combination_ZJet_' + time.strftime("%Y-%m-%d", now),
						'file_mode': ('RECREATE' if first else 'UPDATE'),
						'weights': ['&&'.join([alphacut, etacut])]
					}
					first = False
					if additional_dictionary is not None:
						d.update(additional_dictionary)
					plots.append(d)

	harryinterface.harry_interface(plots, args + ['--max-processes', '1'])
