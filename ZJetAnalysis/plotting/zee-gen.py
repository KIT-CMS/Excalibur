#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ZJet.Plotting.harryZJet as harryZJet

if __name__ == '__main__':
	# some variables
	quantity = 'zmass'
	selection = '1'
	path = '/portal/ekpcms5/home/dhaitz/git/excalibur'
	#data = '/work/data_ee_corr.root'
	mc = '/store/mc_ee_powheg_corr.root'
	#mc = '/work/mc_ee_corr.root'
	l = []
	for threed in range(360):
		d = {
			'x_expressions': [quantity, "gen"+quantity, quantity, "zpt", "(zy+90)", 'genzmass'],
			'y_expressions': ["gen"+quantity, quantity, "gen"+quantity]*2,
			'files': [
				path + mc,
			],
			'weights': selection,
			'nicks': [
				'mc', '1', '2', '3', "4", "5"
			],

			'folders': ['all_AK5PFJetsCHSL1L2L3'],
			'analysis_modules': [
			#	'NormalizeToFirstHisto'
			],
		
			'x_lims': [81, 101],
			'y_lims': [81, 101],
			#'z_lims': [0, 1000],
			'x_bins': "40,81,101",
			'y_bins': "40,81,101",
			'x_label': '',
			'y_label': '',

			'n_axes_x': 3,
			'n_axes_y': 2,
			'axes': [0, 2, 1, 3, 4, 5],
			'3d': threed,
		
			'formats': ['png'],
			'filename': quantity+str(threed).zfill(3),
			#'log_level': 'debug',
			#'www': "2D",

		}
		l.append(d)
	harry_instance = harryZJet.HarryPlotterZJet(list_of_config_dicts=l, n_processes=16)

